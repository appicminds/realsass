/**
 * Construction ERP: pop-up entry forms for Google Sheets.
 *
 * Install once: Extensions > Apps Script, replace everything in Code.gs with this file, Save,
 * then reload the spreadsheet. A "Forms" menu appears. Run "Forms > Set up buttons" once
 * to put a button on every entry tab.
 */

// Tabs that get a form. The form is built from the tab's header row, dropdowns and formats.
var FORM_SHEETS = [
  'Weekly Attendance', 'Worker Payments', 'Labour Advances', 'Site Expenses', 'Daily Diary',
  'Supplier Invoices', 'Purchase Orders', 'Goods Receipts', 'Requisitions',
  'Measurements', 'RA Bills', 'Receipts', 'Change Events',
  'Projects', 'Workers', 'Parties', 'Budget', 'BOQ', 'Cost Codes',
  'RFIs', 'Submittals', 'Documents', 'Quality & Punch', 'Safety', 'Lookahead', 'Leads'
];

var BTN_ADD = '__BTN_ADD__';
var BTN_ATT = '__BTN_ATT__';
var BTN_ADD_SMALL = '__BTN_ADD_SMALL__';
var BTN_ATT_SMALL = '__BTN_ATT_SMALL__';
var BTN_WEEK_SMALL = '__BTN_WEEK_SMALL__';
var BTN_PAY_SMALL = '__BTN_PAY_SMALL__';

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Forms')
    .addItem('Start new week (Weekly Attendance)', 'startNewWeek')
    .addItem('Weekly Attendance row', 'form_Weekly_Attendance')
    .addItem('Pay all balances for a week', 'payWeek')
    .addItem('Record one payment', 'form_Worker_Payments')
    .addItem('Add entry to this tab', 'openFormForActiveSheet')
    .addSeparator()
    .addItem('Labour Advance', 'form_Labour_Advances')
    .addItem('Site Expense', 'form_Site_Expenses')
    .addItem('Daily Diary', 'form_Daily_Diary')
    .addItem('Supplier Invoice', 'form_Supplier_Invoices')
    .addItem('Purchase Order line', 'form_Purchase_Orders')
    .addItem('Client Receipt', 'form_Receipts')
    .addItem('Measurement', 'form_Measurements')
    .addItem('RA Bill', 'form_RA_Bills')
    .addSeparator()
    .addItem('New Worker', 'form_Workers')
    .addItem('New Project', 'form_Projects')
    .addItem('New Client / Supplier', 'form_Parties')
    .addSeparator()
    .addItem('Set up buttons on every tab', 'setupButtons')
    .addToUi();
}

// Menu and button targets (Apps Script needs one named function per target).
function form_Weekly_Attendance() { openForm('Weekly Attendance'); }
function form_Worker_Payments() { openForm('Worker Payments'); }
function form_Labour_Advances() { openForm('Labour Advances'); }
function form_Site_Expenses() { openForm('Site Expenses'); }
function form_Daily_Diary() { openForm('Daily Diary'); }
function form_Supplier_Invoices() { openForm('Supplier Invoices'); }
function form_Purchase_Orders() { openForm('Purchase Orders'); }
function form_Goods_Receipts() { openForm('Goods Receipts'); }
function form_Requisitions() { openForm('Requisitions'); }
function form_Measurements() { openForm('Measurements'); }
function form_RA_Bills() { openForm('RA Bills'); }
function form_Receipts() { openForm('Receipts'); }
function form_Change_Events() { openForm('Change Events'); }
function form_Projects() { openForm('Projects'); }
function form_Workers() { openForm('Workers'); }
function form_Parties() { openForm('Parties'); }
function form_Budget() { openForm('Budget'); }
function form_BOQ() { openForm('BOQ'); }
function form_Cost_Codes() { openForm('Cost Codes'); }
function form_RFIs() { openForm('RFIs'); }
function form_Submittals() { openForm('Submittals'); }
function form_Documents() { openForm('Documents'); }
function form_Quality_and_Punch() { openForm('Quality & Punch'); }
function form_Safety() { openForm('Safety'); }
function form_Lookahead() { openForm('Lookahead'); }
function form_Leads() { openForm('Leads'); }

function fnName_(sheetName) {
  return 'form_' + sheetName.replace(/&/g, 'and').replace(/[^A-Za-z0-9]+/g, '_');
}

function openFormForActiveSheet() {
  var name = SpreadsheetApp.getActiveSheet().getName();
  if (FORM_SHEETS.indexOf(name) < 0) {
    SpreadsheetApp.getUi().alert('There is no form for "' + name + '". Open an entry tab such as Site Expenses first.');
    return;
  }
  openForm(name);
}


// ---------------------------------------------------------------- automatic IDs
// Registers whose first column is a running ID. The form fills in the next free number.
var ID_PREFIX = {
  'Projects': 'PRJ-', 'Workers': 'W-', 'Measurements': 'M-', 'RA Bills': 'RA-', 'Receipts': 'RC-',
  'Change Events': 'CE-', 'Requisitions': 'RQ-', 'Goods Receipts': 'GRN-', 'Supplier Invoices': 'SI-',
  'RFIs': 'RFI-', 'Submittals': 'SBM-', 'Quality & Punch': 'QC-', 'Safety': 'SF-', 'Leads': 'LD-'
};
var PARTY_PREFIX = {'Client': 'CL-', 'Supplier': 'SUP-', 'Subcontractor': 'SUB-', 'Consultant': 'CON-'};

function colValues_(sh, col) {
  var n = sh.getLastRow() - 1;
  if (n < 1) return [];
  return sh.getRange(2, col, n, 1).getDisplayValues().map(function (r) { return r[0]; }).filter(String);
}

// Next ID after the highest existing one with this prefix, keeping its zero padding (PRJ-009 -> PRJ-010).
function nextId_(values, prefix, minWidth) {
  var max = 0, width = minWidth || 3;
  var re = new RegExp('^' + prefix.replace(/[-]/g, '\\-') + '(\\d+)$');
  values.forEach(function (v) {
    var m = re.exec(String(v).trim());
    if (m) { max = Math.max(max, Number(m[1])); width = Math.max(width, m[1].length); }
  });
  var num = String(max + 1);
  while (num.length < width) num = '0' + num;
  return prefix + num;
}

function idInfo_(sheetName, sh) {
  var info = {};
  if (ID_PREFIX[sheetName]) {
    info.idValue = nextId_(colValues_(sh, 1), ID_PREFIX[sheetName], sheetName === 'RA Bills' ? 2 : 3);
  } else if (sheetName === 'Parties') {
    var ids = colValues_(sh, 1);
    info.partyNext = {};
    Object.keys(PARTY_PREFIX).forEach(function (t) { info.partyNext[t] = nextId_(ids, PARTY_PREFIX[t], 3); });
  } else if (sheetName === 'Purchase Orders') {
    var poNos = colValues_(sh, 2);
    info.poNext = nextId_(poNos, 'PO-', 3);
    info.poLines = {};
    poNos.forEach(function (p) { info.poLines[p] = (info.poLines[p] || 0) + 1; });
  }
  return info;
}


// Dropdown options for a field whose sheet dropdown points at a range.
// IDs from Projects, Parties, Workers and Cost Codes are shown with their names,
// and party lists are narrowed to clients or suppliers when the field asks for one.
var NAMED_LISTS = {'Projects': 2, 'Parties': 2, 'Workers': 2, 'Cost Codes': 2, 'Purchase Orders': 9};
function rangeOptions_(range, label) {
  var src = range.getSheet();
  var name = src.getName();
  var ids = range.getDisplayValues().map(function (r) { return r[0]; });
  if (!NAMED_LISTS[name] || range.getColumn() !== 1) return ids.map(function (v) { return {v: v, t: v}; });
  var n = ids.length;
  var names = src.getRange(range.getRow(), NAMED_LISTS[name], n, 1).getDisplayValues();
  var types = name === 'Parties' ? src.getRange(range.getRow(), 3, n, 1).getDisplayValues() : null;
  var want = null;
  if (types) {
    if (/client/i.test(label)) want = ['Client'];
    else if (/contractor/i.test(label)) want = ['Subcontractor'];
    else if (/supplier/i.test(label)) want = ['Supplier', 'Subcontractor'];
  }
  var out = [];
  for (var i = 0; i < n; i++) {
    if (!ids[i]) continue;
    if (want && types[i][0] && want.indexOf(types[i][0]) < 0) continue;
    out.push({v: ids[i], t: names[i][0] ? ids[i] + '  -  ' + names[i][0] : ids[i]});
  }
  return out;
}

// ---------------------------------------------------------------- generic form
function getFormSpec(sheetName) {
  var sh = SpreadsheetApp.getActive().getSheetByName(sheetName);
  if (!sh) throw new Error('Tab not found: ' + sheetName);
  var lastCol = sh.getLastColumn();
  var headers = sh.getRange(1, 1, 1, lastCol).getValues()[0];
  var probe = sh.getRange(2, 1, 1, lastCol);
  var formulas = probe.getFormulas()[0];
  var formats = probe.getNumberFormats()[0];
  var rules = probe.getDataValidations()[0];
  var fields = [];
  for (var c = 0; c < lastCol; c++) {
    var h = String(headers[c] || '').trim();
    if (!h || /\(auto\)$/.test(h) || formulas[c]) continue;
    var f = {col: c + 1, label: h, type: 'text', options: null};
    var fmt = String(formats[c] || '');
    if (/yy|dd/.test(fmt)) f.type = 'date';
    else if (/%/.test(fmt)) f.type = 'percent';
    else if (/0/.test(fmt) && fmt !== '@') f.type = 'number';
    var rule = rules[c];
    if (rule) {
      var t = rule.getCriteriaType();
      var args = rule.getCriteriaValues();
      var opts = [];
      if (t === SpreadsheetApp.DataValidationCriteria.VALUE_IN_RANGE) {
        opts = rangeOptions_(args[0], h);
      } else if (t === SpreadsheetApp.DataValidationCriteria.VALUE_IN_LIST) {
        opts = args[0].map(function (v) { return {v: v, t: v}; });
      }
      var seen = {};
      opts = opts.filter(function (o) { if (o.v === '' || seen[o.v]) return false; seen[o.v] = 1; return true; });
      if (opts.length) { f.type = 'list'; f.options = opts; }
    }
    fields.push(f);
  }
  if (fields.length) fields[0].required = true;
  var spec = {sheet: sheetName, fields: fields};
  var info = idInfo_(sheetName, sh);
  Object.keys(info).forEach(function (k) { spec[k] = info[k]; });
  return spec;
}

function firstEmptyRow_(sh) {
  var last = Math.max(sh.getLastRow(), 2);
  var colA = sh.getRange(2, 1, last - 1, 1).getValues();
  for (var i = 0; i < colA.length; i++) {
    if (colA[i][0] === '' || colA[i][0] === null) return i + 2;
  }
  return last + 1;
}

function toCell_(v, type) {
  if (v === '' || v === null || v === undefined) return '';
  if (type === 'date') return String(v);  // yyyy-mm-dd text; Sheets turns it into a date in the sheet's time zone
  if (type === 'number') return Number(v);
  if (type === 'percent') return Number(v) / 100;
  return v;
}

function saveFormRow(sheetName, values) {
  var lock = LockService.getDocumentLock();
  lock.waitLock(20000);
  try {
    var spec = getFormSpec(sheetName);
    var sh = SpreadsheetApp.getActive().getSheetByName(sheetName);
    var first = spec.fields[0];
    var used = colValues_(sh, 1);
    // A running ID that someone else just used: take the next free one instead of saving a duplicate.
    if (ID_PREFIX[sheetName] && used.indexOf(String(values[first.col])) >= 0) values[first.col] = spec.idValue;
    if (!values[first.col]) throw new Error('"' + first.label + '" is required.');
    if ((sheetName === 'Parties' || sheetName === 'Purchase Orders' || sheetName === 'Workers' || sheetName === 'Projects')
        && used.indexOf(String(values[first.col])) >= 0) {
      throw new Error('"' + values[first.col] + '" already exists. Change it, or close and open the form again for a new number.');
    }
    var row = firstEmptyRow_(sh);
    spec.fields.forEach(function (f) {
      var v = toCell_(values[f.col], f.type);
      if (v !== '') sh.getRange(row, f.col).setValue(v);
    });
    SpreadsheetApp.flush();
    var check = '';
    var headers = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
    var ci = headers.indexOf('Check (auto)');
    if (ci >= 0) check = sh.getRange(row, ci + 1).getDisplayValue();
    return {row: row, check: check, id: values[first.col], spec: getFormSpec(sheetName)};
  } finally {
    lock.releaseLock();
  }
}

function openForm(sheetName) {
  var spec = getFormSpec(sheetName);
  var t = HtmlService.createTemplate(FORM_HTML);
  t.spec = JSON.stringify(spec);
  t.today = sheetName === 'Weekly Attendance' ? nextThursday_()
      : Utilities.formatDate(new Date(), SpreadsheetApp.getActive().getSpreadsheetTimeZone(), 'yyyy-MM-dd');
  var html = t.evaluate().setWidth(520).setHeight(620);
  SpreadsheetApp.getUi().showModalDialog(html, sheetName);
}

var STYLE =
  '<style>' +
  'body{font-family:Arial,sans-serif;font-size:14px;margin:0;padding:12px;color:#222}' +
  'label{display:block;font-weight:bold;margin:10px 0 4px}' +
  'input,select,textarea{width:100%;box-sizing:border-box;padding:8px;font-size:14px;border:1px solid #bbb;border-radius:6px}' +
  '.req{color:#c00}' +
  '.bar{position:sticky;bottom:0;background:#fff;padding:10px 0;display:flex;gap:8px}' +
  'button{flex:1;padding:12px;font-size:15px;border:0;border-radius:6px;cursor:pointer}' +
  '.save{background:#0f5e5e;color:#fff}.more{background:#38761d;color:#fff}.close{background:#ddd}' +
  '#msg{margin-top:8px;padding:8px;border-radius:6px;display:none}' +
  '.ok{background:#d9ead3}.err{background:#f4cccc}' +
  'table{width:100%;border-collapse:collapse}td,th{padding:4px;border-bottom:1px solid #eee;text-align:left}' +
  'td select,td input{padding:5px}' +
  '</style>';

var FORM_HTML =
  '<!DOCTYPE html><html><head><base target="_top">' + STYLE + '</head><body>' +
  '<form id="f" onsubmit="return false"></form>' +
  '<div id="msg"></div>' +
  '<div class="bar"><button class="save" onclick="send(false)">Save and close</button>' +
  '<button class="more" onclick="send(true)">Save and add another</button>' +
  '<button class="close" onclick="google.script.host.close()">Cancel</button></div>' +
  '<script>' +
  'var spec=<?!= spec ?>;var today="<?= today ?>";' +
  'function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})}' +
  'function build(){var h="";spec.fields.forEach(function(f){' +
  'h+="<label>"+esc(f.label)+(f.required?" <span class=req>*</span>":"")+"</label>";' +
  'var id="c"+f.col;' +
  'if(f.type=="list"){h+="<select id="+id+"><option value=\'\'></option>";f.options.forEach(function(o){h+="<option value=\'"+esc(o.v).replace(/\'/g,"&#39;")+"\'>"+esc(o.t)+"</option>"});h+="</select>"}' +
  'else if(f.type=="date"){h+="<input type=date id="+id+(f.required||/^Date/.test(f.label)?" value="+today:"")+">"}' +
  'else if(f.type=="number"||f.type=="percent"){h+="<input type=number step=any id="+id+(f.type=="percent"?" placeholder=\'e.g. 5 for 5%\'":"")+">"}' +
  'else if(/description|notes|question|response|work done|blockers/i.test(f.label)){h+="<textarea rows=2 id="+id+"></textarea>"}' +
  'else{h+="<input id="+id+">"}});document.getElementById("f").innerHTML=h;wire();}' +
  'function fld(re){for(var i=0;i<spec.fields.length;i++){if(re.test(spec.fields[i].label))return document.getElementById("c"+spec.fields[i].col)}return null}' +
  'var idEl=null;function setIds(){idEl=document.getElementById("c"+spec.fields[0].col);' +
  'if(spec.idValue){idEl.value=spec.idValue}' +
  'if(spec.partyNext){var t=fld(/^Type$/);if(t&&spec.partyNext[t.value])idEl.value=spec.partyNext[t.value]}' +
  'if(spec.poNext){var po=fld(/^PO no/);if(po){if(!po.value)po.value=spec.poNext;idEl.value=po.value+"-"+((spec.poLines[po.value]||0)+1)}}}' +
  'function wire(){var t=fld(/^Type$/);if(t&&spec.partyNext)t.onchange=setIds;var po=fld(/^PO no/);if(po&&spec.poNext)po.oninput=setIds;' +
  'var first=spec.fields[0];if(spec.idValue||spec.partyNext||spec.poNext){var l=document.querySelectorAll("label")[0];l.innerHTML+=" <small style=\\"font-weight:normal;color:#666\\">(filled in for you)</small>"}setIds()}' +
  'function send(again){var v={};spec.fields.forEach(function(f){v[f.col]=document.getElementById("c"+f.col).value});' +
  'var m=document.getElementById("msg");m.style.display="block";m.className="";m.textContent="Saving...";' +
  'google.script.run.withSuccessHandler(function(r){' +
  'if(again){m.className=r.check?"err":"ok";m.textContent="Saved in row "+r.row+(r.check?". Check: "+r.check:".");' +
  'spec.fields.forEach(function(f){var e=document.getElementById("c"+f.col);if(f.type!="date"&&!/project|status|shift|cost code|marked by|approved by|^type$|^po no|^supplier/i.test(f.label))e.value=""});' +
  'if(r.spec){spec.idValue=r.spec.idValue;spec.partyNext=r.spec.partyNext;spec.poNext=r.spec.poNext;spec.poLines=r.spec.poLines;setIds()}}' +
  'else{google.script.host.close()}})' +
  '.withFailureHandler(function(e){m.className="err";m.textContent=e.message}).saveFormRow(spec.sheet,v);}' +
  'build();' +
  '</script></body></html>';



// Runs by itself whenever someone edits the sheet.
// Weekly Attendance: picking a worker fills an empty Week ending with the coming Thursday
// and an empty Main project with the worker's usual project.
// Worker Payments: picking a worker fills an empty Date paid with today and Week ending with the latest Thursday.
function onEdit(e) {
  try {
    var sh = e.range.getSheet();
    var name = sh.getName();
    if (e.range.getRow() < 2) return;
    var headers = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
    var cWorker = headers.indexOf('Worker') + 1;
    if (!cWorker || e.range.getColumn() > cWorker || e.range.getLastColumn() < cWorker) return;
    var tz = e.source.getSpreadsheetTimeZone();
    var iso = Number(Utilities.formatDate(new Date(), tz, 'u'));  // 1 = Monday ... 7 = Sunday
    var day = 86400000, now = new Date().getTime();
    var nextThu = Utilities.formatDate(new Date(now + ((4 - iso + 7) % 7) * day), tz, 'yyyy-MM-dd');
    var lastThu = Utilities.formatDate(new Date(now - ((iso - 4 + 7) % 7) * day), tz, 'yyyy-MM-dd');
    for (var r = e.range.getRow(); r <= e.range.getLastRow(); r++) {
      var worker = sh.getRange(r, cWorker).getValue();
      if (!worker) continue;
      if (name === 'Weekly Attendance') {
        if (sh.getRange(r, 1).getValue() === '') sh.getRange(r, 1).setValue(nextThu);
        var cProj = headers.indexOf('Main project') + 1;
        if (cProj && sh.getRange(r, cProj).getValue() === '') {
          var w = e.source.getSheetByName('Workers');
          var wv = w.getRange(1, 1, w.getLastRow(), w.getLastColumn()).getDisplayValues();
          var iN = wv[0].indexOf('Name'), iP = wv[0].indexOf('Usual project');
          for (var k = 1; k < wv.length; k++) {
            if (wv[k][iN] === worker && wv[k][iP]) { sh.getRange(r, cProj).setValue(wv[k][iP]); break; }
          }
        }
      } else if (name === 'Worker Payments') {
        if (sh.getRange(r, 1).getValue() === '') sh.getRange(r, 1).setValue(Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd'));
        if (sh.getRange(r, 2).getValue() === '') sh.getRange(r, 2).setValue(lastThu);
      }
    }
  } catch (err) {
    // never block typing because of a helper error
  }
}

// ---------------------------------------------------------------- weekly attendance
// Weeks run Friday to Thursday; wages are paid on Thursday.
function nextThursday_() {
  var tz = SpreadsheetApp.getActive().getSpreadsheetTimeZone();
  var now = new Date();
  var iso = Number(Utilities.formatDate(now, tz, 'u'));  // 1 = Monday ... 7 = Sunday
  var add = (4 - iso + 7) % 7;                            // days until Thursday (0 if today is Thursday)
  return Utilities.formatDate(new Date(now.getTime() + add * 86400000), tz, 'yyyy-MM-dd');
}

function startNewWeek() {
  var ss = SpreadsheetApp.getActive();
  var ui = SpreadsheetApp.getUi();
  var def = nextThursday_();
  var ans = ui.prompt('Start new week', 'Week ending on Thursday (yyyy-mm-dd). Leave blank for ' + def + '.', ui.ButtonSet.OK_CANCEL);
  if (ans.getSelectedButton() !== ui.Button.OK) return;
  var thu = String(ans.getResponseText() || '').trim() || def;
  var p = thu.split('-');
  var dt = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
  if (p.length !== 3 || isNaN(dt.getTime()) || dt.getDay() !== 4) {
    ui.alert('"' + thu + '" is not a Thursday. Type the date like ' + def + '.');
    return;
  }
  var sh = ss.getSheetByName('Weekly Attendance');
  var last = Math.max(sh.getLastRow(), 2);
  var have = {};
  sh.getRange(2, 1, last - 1, 2).getDisplayValues().forEach(function (r) {
    if (r[0].slice(-10) === thu) have[r[1]] = true;
  });
  var w = ss.getSheetByName('Workers');
  var wv = w.getRange(1, 1, Math.max(w.getLastRow(), 2), w.getLastColumn()).getDisplayValues();
  var h = wv[0], iId = h.indexOf('Worker ID'), iName = h.indexOf('Name'), iProj = h.indexOf('Usual project'), iAct = h.indexOf('Active');
  var dates = [], names = [], projects = [];
  for (var r = 1; r < wv.length; r++) {
    var id = wv[r][iId];
    if (!id || !wv[r][iName] || have[id] || (iAct >= 0 && wv[r][iAct] === 'No')) continue;
    dates.push([thu]);
    names.push([wv[r][iName]]);
    projects.push([iProj >= 0 ? wv[r][iProj] : '']);
  }
  if (!dates.length) { ui.alert('Every active worker already has a row for the week ending ' + thu + '.'); return; }
  var row = firstEmptyRow_(sh);
  // column B (Worker ID) is a formula; write the date (A), worker name (C) and main project (E)
  sh.getRange(row, 1, dates.length, 1).setValues(dates);
  sh.getRange(row, 3, names.length, 1).setValues(names);
  sh.getRange(row, 5, projects.length, 1).setValues(projects);
  var ids = dates;
  sh.activate();
  sh.setActiveRange(sh.getRange(row, 8));
  ss.toast(ids.length + ' workers added for the week ending ' + thu + '. Mark P, H, A or L for each day.', 'New week', 8);
}


// Record a payment for every worker who still has a balance for one week (asks which Thursday).
function payWeek() {
  var ss = SpreadsheetApp.getActive();
  var ui = SpreadsheetApp.getUi();
  var def = nextThursday_();
  var ans = ui.prompt('Pay all', 'Pay every balance for the week ending on Thursday (yyyy-mm-dd). Leave blank for ' + def + '.', ui.ButtonSet.OK_CANCEL);
  if (ans.getSelectedButton() !== ui.Button.OK) return;
  var thu = String(ans.getResponseText() || '').trim() || def;
  var project = '';
  var sh = ss.getSheetByName('Weekly Attendance');
  var h = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  var iName = h.indexOf('Worker'), iProj = h.indexOf('Main project'), iBal = h.indexOf('Balance to pay (PKR) (auto)');
  if (iName < 0 || iBal < 0) { ui.alert('Weekly Attendance columns not found.'); return; }
  var last = Math.max(sh.getLastRow(), 2);
  var disp = sh.getRange(2, 1, last - 1, sh.getLastColumn()).getDisplayValues();
  var vals = sh.getRange(2, iBal + 1, last - 1, 1).getValues();
  var rows = [], total = 0;
  for (var i = 0; i < disp.length; i++) {
    if (disp[i][0].slice(-10) !== thu) continue;
    if (project && disp[i][iProj] !== project) continue;
    var bal = Number(vals[i][0]) || 0;
    if (bal <= 0) continue;
    rows.push([disp[i][iName], bal]);
    total += bal;
  }
  if (!rows.length) { ui.alert('Nothing to pay for the week ending ' + thu + (project ? ' on ' + project : '') + '.'); return; }
  var ok = ui.alert('Pay all', 'Record payment for ' + rows.length + ' workers, total PKR ' + total.toLocaleString() +
                    ', for the week ending ' + thu + '?', ui.ButtonSet.YES_NO);
  if (ok !== ui.Button.YES) return;
  var tz = ss.getSpreadsheetTimeZone();
  var today = Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd');
  var pay = ss.getSheetByName('Worker Payments');
  var row = firstEmptyRow_(pay);
  pay.getRange(row, 1, rows.length, 3).setValues(rows.map(function (r) { return [today, thu, r[0]]; }));
  pay.getRange(row, 5, rows.length, 2).setValues(rows.map(function (r) { return [r[1], 'Cash']; }));
  ss.toast(rows.length + ' payments recorded (PKR ' + total.toLocaleString() + '). Change the Mode on Worker Payments if any were by bank.', 'Paid', 8);
}

// ---------------------------------------------------------------- bulk attendance
function getAttendanceData() {
  var ss = SpreadsheetApp.getActive();
  var w = ss.getSheetByName('Workers');
  var wv = w.getRange(1, 1, Math.max(w.getLastRow(), 2), w.getLastColumn()).getDisplayValues();
  var h = wv[0];
  var iId = h.indexOf('Worker ID'), iName = h.indexOf('Name'), iTrade = h.indexOf('Trade'),
      iProj = h.indexOf('Usual project'), iAct = h.indexOf('Active');
  var workers = [];
  for (var r = 1; r < wv.length; r++) {
    if (!wv[r][iId]) continue;
    if (iAct >= 0 && wv[r][iAct] === 'No') continue;
    workers.push({id: wv[r][iId], name: wv[r][iName], trade: wv[r][iTrade], project: iProj >= 0 ? wv[r][iProj] : ''});
  }
  var p = ss.getSheetByName('Projects');
  var projects = p.getRange(2, 1, Math.max(p.getLastRow() - 1, 1), 2).getDisplayValues()
    .filter(function (r) { return r[0]; })
    .map(function (r) { return {v: r[0], t: r[1] ? r[0] + '  -  ' + r[1] : r[0]}; });
  var cc = ss.getSheetByName('Cost Codes');
  var codes = cc.getRange(2, 1, Math.max(cc.getLastRow() - 1, 1), 1).getDisplayValues()
    .map(function (r) { return r[0]; }).filter(String);
  return {workers: workers, projects: projects, codes: codes,
          today: Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd')};
}

function saveAttendance(payload) {
  var lock = LockService.getDocumentLock();
  lock.waitLock(30000);
  try {
    var sh = SpreadsheetApp.getActive().getSheetByName('Labour Attendance');
    var h = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
    function col(name) { var i = h.indexOf(name); if (i < 0) throw new Error('Column missing: ' + name); return i + 1; }
    var cDate = col('Date'), cProj = col('Project'), cW = col('Worker'), cSt = col('Status'), cSh = col('Shift'),
        cHrs = col('Hours worked (blank = full day)'), cOt = col('Overtime hours'), cWork = col('Work / location'),
        cCode = col('Cost code'), cBy = col('Marked by');
    if (!payload.date || !payload.project) throw new Error('Pick a date and a project.');
    var date = payload.date;  // yyyy-mm-dd text; Sheets turns it into a date
    // existing rows for that date + shift, to avoid duplicates
    var last = Math.max(sh.getLastRow(), 2);
    var data = sh.getRange(2, 1, last - 1, Math.max(cW, cSh)).getDisplayValues();
    var existing = {};
    data.forEach(function (r) {
      if (r[cDate - 1] === date && r[cSh - 1] === payload.shift) existing[r[cW - 1]] = true;
    });
    var saved = 0, skipped = [];
    var row = firstEmptyRow_(sh);
    payload.rows.forEach(function (x) {
      if (!x.status) return;
      if (existing[x.name]) { skipped.push(x.name); return; }
      while (sh.getRange(row, 1).getValue() !== '') row++;
      sh.getRange(row, cDate).setValue(date);
      sh.getRange(row, cProj).setValue(payload.project);
      sh.getRange(row, cW).setValue(x.name);
      sh.getRange(row, cSt).setValue(x.status);
      sh.getRange(row, cSh).setValue(payload.shift);
      if (x.hours !== '') sh.getRange(row, cHrs).setValue(Number(x.hours));
      if (x.ot !== '') sh.getRange(row, cOt).setValue(Number(x.ot));
      if (payload.work) sh.getRange(row, cWork).setValue(payload.work);
      if (payload.code) sh.getRange(row, cCode).setValue(payload.code);
      if (payload.by) sh.getRange(row, cBy).setValue(payload.by);
      row++; saved++;
    });
    return {saved: saved, skipped: skipped};
  } finally {
    lock.releaseLock();
  }
}

function openAttendanceForm() {
  var t = HtmlService.createTemplate(ATT_HTML);
  t.data = JSON.stringify(getAttendanceData());
  SpreadsheetApp.getUi().showModalDialog(t.evaluate().setWidth(760).setHeight(640), 'Mark attendance');
}

var ATT_HTML =
  '<!DOCTYPE html><html><head><base target="_top">' + STYLE + '</head><body>' +
  '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">' +
  '<div><label>Date</label><input type=date id=date></div>' +
  '<div><label>Project <span class=req>*</span></label><select id=proj onchange="filter()"></select></div>' +
  '<div><label>Shift</label><select id=shift><option>Day</option><option>Night</option></select></div>' +
  '<div><label>Work / location</label><input id=work></div>' +
  '<div><label>Cost code</label><select id=code></select></div>' +
  '<div><label>Marked by</label><input id=by></div></div>' +
  '<label><input type=checkbox id=all style="width:auto" onchange="filter()"> Show workers from all projects</label>' +
  '<div style="margin:6px 0">Set everyone to: <a href="#" onclick="return setAll(\'Present\')">Present</a> | ' +
  '<a href="#" onclick="return setAll(\'Absent\')">Absent</a> | <a href="#" onclick="return setAll(\'\')">Not on site</a></div>' +
  '<table><thead><tr><th>Worker</th><th>Trade</th><th>Status</th><th>Hours (blank = full day)</th><th>Overtime hrs</th></tr></thead><tbody id=tb></tbody></table>' +
  '<div id="msg"></div>' +
  '<div class="bar"><button class="save" onclick="send()">Save attendance</button>' +
  '<button class="close" onclick="google.script.host.close()">Close</button></div>' +
  '<script>' +
  'var d=<?!= data ?>;' +
  'function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})}' +
  'document.getElementById("date").value=d.today;' +
  'document.getElementById("proj").innerHTML=d.projects.map(function(p){return"<option value=\'"+esc(p.v)+"\'>"+esc(p.t)+"</option>"}).join("");' +
  'document.getElementById("code").innerHTML="<option></option>"+d.codes.map(function(p){return"<option"+(/LAB/.test(p)?" selected":"")+">"+esc(p)+"</option>"}).join("");' +
  'function filter(){var p=document.getElementById("proj").value,all=document.getElementById("all").checked,h="";' +
  'd.workers.forEach(function(w,i){if(!all&&w.project&&w.project!=p)return;' +
  'h+="<tr><td>"+esc(w.id)+" "+esc(w.name)+"</td><td>"+esc(w.trade)+"</td><td><select data-i="+i+" class=st>"+' +
  '["Present","Half day","Absent","Leave",""].map(function(s){return"<option value=\'"+s+"\'>"+(s||"Not on site")+"</option>"}).join("")+' +
  '"</select></td><td><input type=number step=any class=hr data-i="+i+"></td><td><input type=number step=any class=ot data-i="+i+"></td></tr>"});' +
  'document.getElementById("tb").innerHTML=h||"<tr><td colspan=5>No active workers for this project. Add them on the Workers tab.</td></tr>";}' +
  'function setAll(s){document.querySelectorAll(".st").forEach(function(e){e.value=s});return false}' +
  'function send(){var rows=[];document.querySelectorAll(".st").forEach(function(e){var i=e.getAttribute("data-i");' +
  'rows.push({id:d.workers[i].id,name:d.workers[i].name,status:e.value,hours:document.querySelector(".hr[data-i=\'"+i+"\']").value,ot:document.querySelector(".ot[data-i=\'"+i+"\']").value})});' +
  'var m=document.getElementById("msg");m.style.display="block";m.className="";m.textContent="Saving...";' +
  'google.script.run.withSuccessHandler(function(r){m.className=r.skipped.length?"err":"ok";' +
  'm.textContent="Saved "+r.saved+" workers."+(r.skipped.length?" Already marked for this date and shift, not saved again: "+r.skipped.join(", "):"");})' +
  '.withFailureHandler(function(e){m.className="err";m.textContent=e.message})' +
  '.saveAttendance({date:document.getElementById("date").value,project:document.getElementById("proj").value,shift:document.getElementById("shift").value,' +
  'work:document.getElementById("work").value,code:document.getElementById("code").value,by:document.getElementById("by").value,rows:rows});}' +
  'filter();' +
  '</script></body></html>';

// ---------------------------------------------------------------- buttons
function setupButtons() {
  var ss = SpreadsheetApp.getActive();
  var add = Utilities.newBlob(Utilities.base64Decode(BTN_ADD), 'image/png', 'add.png');
  var att = Utilities.newBlob(Utilities.base64Decode(BTN_ATT), 'image/png', 'att.png');
  var addS = Utilities.newBlob(Utilities.base64Decode(BTN_ADD_SMALL), 'image/png', 'add_s.png');
  var attS = Utilities.newBlob(Utilities.base64Decode(BTN_ATT_SMALL), 'image/png', 'att_s.png');
  var weekS = Utilities.newBlob(Utilities.base64Decode(BTN_WEEK_SMALL), 'image/png', 'week_s.png');
  var payS = Utilities.newBlob(Utilities.base64Decode(BTN_PAY_SMALL), 'image/png', 'pay_s.png');
  var wpay = ss.getSheetByName('Weekly Pay');
  if (wpay) removeButtons_(wpay);
  FORM_SHEETS.forEach(function (name) {
    var sh = ss.getSheetByName(name);
    if (!sh) return;
    removeButtons_(sh);
    // Make the header row taller, push header text to the top, and put the button under it in A1
    // (row 1 and column A are frozen, so the button stays visible while scrolling).
    sh.setRowHeight(1, 92);
    sh.getRange(1, 1, 1, sh.getLastColumn()).setVerticalAlignment('top');
    var w = Math.max(60, Math.min(sh.getColumnWidth(1) - 6, 96));
    sh.insertImage(addS, 1, 1, 3, 58).setWidth(w).setHeight(30).assignScript(fnName_(name));
    if (name === 'Labour Attendance') {
      sh.insertImage(attS, 2, 1, 3, 58).setWidth(96).setHeight(30).assignScript('openAttendanceForm');
    }
    if (name === 'Weekly Attendance') {
      sh.insertImage(weekS, 2, 1, 3, 58).setWidth(76).setHeight(30).assignScript('startNewWeek');
      sh.insertImage(payS, 3, 1, 3, 58).setWidth(76).setHeight(30).assignScript('payWeek');
    }
  });
  var home = ss.getSheetByName('Home');
  if (home) {
    removeButtons_(home);
    var values = home.getRange(1, 1, home.getLastRow(), 1).getDisplayValues();
    for (var r = 0; r < values.length; r++) {
      var label = values[r][0];
      if (FORM_SHEETS.indexOf(label) >= 0) {
        // sits exactly over the green "+ Add" mock button in column C
        home.insertImage(addS, 3, r + 1, 2, 2).setWidth(106).setHeight(26).assignScript(fnName_(label));
        if (label === 'Weekly Attendance') {
          // over the "New week" mock button in column D
          home.insertImage(weekS, 4, r + 1, 2, 2).setWidth(106).setHeight(26).assignScript('startNewWeek');
        }
      }
    }
  }
  try {
  SpreadsheetApp.getUi().alert('Buttons added: a green + Add button in the top-left corner of every entry tab, and next to each name on Home. Click one to open its form. (Buttons work on a computer; on the phone app use the Forms menu instead.)');
  } catch (e) {
    Logger.log('Buttons added.');  // run from the script editor: no pop-up there
  }
}

function removeButtons_(sh) {
  sh.getImages().forEach(function (img) {
    var s = '';
    try { s = img.getScript(); } catch (e) {}
    if (s && (s.indexOf('form_') === 0 || s === 'openAttendanceForm' || s === 'startNewWeek' || s === 'payWeek')) img.remove();
  });
}

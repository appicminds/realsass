/**
 * Construction ERP: pop-up entry forms for Google Sheets.
 *
 * Install once: Extensions > Apps Script, replace everything in Code.gs with this file, Save,
 * then reload the spreadsheet. A "Forms" menu appears. Run "Forms > Set up buttons" once
 * to put a button on every entry tab.
 */

// Tabs that get a form. The form is built from the tab's header row, dropdowns and formats.
var FORM_SHEETS = [
  'Labour Attendance', 'Labour Advances', 'Site Expenses', 'Daily Diary',
  'Supplier Invoices', 'Purchase Orders', 'Goods Receipts', 'Requisitions',
  'Measurements', 'RA Bills', 'Receipts', 'Change Events',
  'Projects', 'Workers', 'Parties', 'Budget', 'BOQ', 'Cost Codes',
  'RFIs', 'Submittals', 'Documents', 'Quality & Punch', 'Safety', 'Lookahead', 'Leads'
];

var BTN_ADD = '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';
var BTN_ATT = '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';
var BTN_ADD_SMALL = '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';
var BTN_ATT_SMALL = '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';

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Forms')
    .addItem('Mark attendance for all workers', 'openAttendanceForm')
    .addItem('Add entry to this tab', 'openFormForActiveSheet')
    .addSeparator()
    .addItem('Labour Attendance (one worker)', 'form_Labour_Attendance')
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
function form_Labour_Attendance() { openForm('Labour Attendance'); }
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
        opts = args[0].getDisplayValues().map(function (r) { return r[0]; });
      } else if (t === SpreadsheetApp.DataValidationCriteria.VALUE_IN_LIST) {
        opts = args[0];
      }
      opts = opts.filter(function (v, i, a) { return v !== '' && a.indexOf(v) === i; });
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
  t.today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
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
  'if(f.type=="list"){h+="<select id="+id+"><option value=\'\'></option>";f.options.forEach(function(o){h+="<option>"+esc(o)+"</option>"});h+="</select>"}' +
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
  var projects = p.getRange(2, 1, Math.max(p.getLastRow() - 1, 1), 1).getDisplayValues()
    .map(function (r) { return r[0]; }).filter(String);
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
    var cDate = col('Date'), cProj = col('Project'), cW = col('Worker ID'), cSt = col('Status'), cSh = col('Shift'),
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
      if (existing[x.id]) { skipped.push(x.id); return; }
      while (sh.getRange(row, 1).getValue() !== '') row++;
      sh.getRange(row, cDate).setValue(date);
      sh.getRange(row, cProj).setValue(payload.project);
      sh.getRange(row, cW).setValue(x.id);
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
  'document.getElementById("proj").innerHTML=d.projects.map(function(p){return"<option>"+esc(p)+"</option>"}).join("");' +
  'document.getElementById("code").innerHTML="<option></option>"+d.codes.map(function(p){return"<option"+(/LAB/.test(p)?" selected":"")+">"+esc(p)+"</option>"}).join("");' +
  'function filter(){var p=document.getElementById("proj").value,all=document.getElementById("all").checked,h="";' +
  'd.workers.forEach(function(w,i){if(!all&&w.project&&w.project!=p)return;' +
  'h+="<tr><td>"+esc(w.id)+" "+esc(w.name)+"</td><td>"+esc(w.trade)+"</td><td><select data-i="+i+" class=st>"+' +
  '["Present","Half day","Absent","Leave",""].map(function(s){return"<option value=\'"+s+"\'>"+(s||"Not on site")+"</option>"}).join("")+' +
  '"</select></td><td><input type=number step=any class=hr data-i="+i+"></td><td><input type=number step=any class=ot data-i="+i+"></td></tr>"});' +
  'document.getElementById("tb").innerHTML=h||"<tr><td colspan=5>No active workers for this project. Add them on the Workers tab.</td></tr>";}' +
  'function setAll(s){document.querySelectorAll(".st").forEach(function(e){e.value=s});return false}' +
  'function send(){var rows=[];document.querySelectorAll(".st").forEach(function(e){var i=e.getAttribute("data-i");' +
  'rows.push({id:d.workers[i].id,status:e.value,hours:document.querySelector(".hr[data-i=\'"+i+"\']").value,ot:document.querySelector(".ot[data-i=\'"+i+"\']").value})});' +
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
        if (label === 'Labour Attendance') {
          // over the "Mark all" mock button in column D
          home.insertImage(attS, 4, r + 1, 2, 2).setWidth(106).setHeight(26).assignScript('openAttendanceForm');
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
    if (s && (s.indexOf('form_') === 0 || s === 'openAttendanceForm')) img.remove();
  });
}

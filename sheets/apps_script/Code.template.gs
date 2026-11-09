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

var BTN_ADD = '__BTN_ADD__';
var BTN_ATT = '__BTN_ATT__';
var BTN_ADD_SMALL = '__BTN_ADD_SMALL__';
var BTN_ATT_SMALL = '__BTN_ATT_SMALL__';

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
  return {sheet: sheetName, fields: fields};
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
    if (!values[first.col]) throw new Error('"' + first.label + '" is required.');
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
    return {row: row, check: check};
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
  'else{h+="<input id="+id+">"}});document.getElementById("f").innerHTML=h;}' +
  'function send(again){var v={};spec.fields.forEach(function(f){v[f.col]=document.getElementById("c"+f.col).value});' +
  'var m=document.getElementById("msg");m.style.display="block";m.className="";m.textContent="Saving...";' +
  'google.script.run.withSuccessHandler(function(r){' +
  'if(again){m.className=r.check?"err":"ok";m.textContent="Saved in row "+r.row+(r.check?". Check: "+r.check:".");' +
  'spec.fields.forEach(function(f){var e=document.getElementById("c"+f.col);if(f.type!="date"&&!/project|status|shift|cost code|marked by|approved by/i.test(f.label))e.value=""});}' +
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
  SpreadsheetApp.getUi().alert('Buttons added: a green + Add button in the top-left corner of every entry tab, and next to each name on Home. Click one to open its form. (Buttons work on a computer; on the phone app use the Forms menu instead.)');
}

function removeButtons_(sh) {
  sh.getImages().forEach(function (img) {
    var s = '';
    try { s = img.getScript(); } catch (e) {}
    if (s && (s.indexOf('form_') === 0 || s === 'openAttendanceForm')) img.remove();
  });
}

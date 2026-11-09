"""Simplify the live imported Google Sheet: Home menu, new dashboards, wage sheet, tab order, hide optional tabs."""
import json, os
import gsheets_build as G

IDS = {"Start Here":1565499533,"Settings":1216117854,"Dashboard":812202400,"Cost Report":1284418966,"Projects":512098071,
"Parties":564131143,"Cost Codes":1227193772,"Workers":1022380620,"Budget":1329686148,"BOQ":1917578204,"Measurements":18671061,
"RA Bills":1648194044,"Receipts":171379148,"Change Events":1195555969,"Requisitions":470621369,"Purchase Orders":63008746,
"Goods Receipts":1325789671,"Supplier Invoices":206623624,"Labour Attendance":606947768,"Labour Advances":876217068,
"Site Expenses":443976919,"Daily Diary":1374454966,"RFIs":1328562888,"Submittals":766801891,"Documents":1329972102,
"Quality & Punch":257993529,"Safety":1677903727,"Lookahead":1390022330,"Leads":1382324273,"Lists":219353797}
NEW = {"Home":2001,"Main Dashboard":2002,"Project Dashboard":2003,"Wage Sheet":2004}
G.SHEET_ID.clear(); G.SHEET_ID.update(IDS); G.SHEET_ID.update(NEW)

VISIBLE = ["Home","Main Dashboard","Project Dashboard","Wage Sheet","Labour Attendance","Labour Advances","Site Expenses",
           "Daily Diary","Supplier Invoices","Purchase Orders","RA Bills","Receipts","Measurements","Projects","Workers",
           "Parties","Budget","BOQ","Change Events","Cost Codes","Settings","Start Here"]
HIDDEN = ["Requisitions","Goods Receipts","RFIs","Submittals","Documents","Quality & Punch","Safety","Lookahead","Leads","Lists"]
RED, GREEN, GOLD, TEAL, NAVY, GREY = "C00000","38761D","B45F06","0F5E5E","1F3864","999999"
COLOR = {"Home":RED,"Main Dashboard":RED,"Project Dashboard":RED,"Wage Sheet":RED,
         "Labour Attendance":GREEN,"Labour Advances":GREEN,"Site Expenses":GREEN,"Daily Diary":GREEN,
         "Supplier Invoices":GOLD,"Purchase Orders":GOLD,"RA Bills":GOLD,"Receipts":GOLD,"Measurements":GOLD,
         "Projects":NAVY,"Workers":NAVY,"Parties":NAVY,"Budget":NAVY,"BOQ":NAVY,"Change Events":NAVY,"Cost Codes":NAVY,
         "Settings":GREY,"Start Here":GREY}

def structure():
    reqs = []
    for nm, sid in NEW.items():
        reqs.append({"addSheet":{"properties":{"sheetId":sid,"title":nm,"gridProperties":{"rowCount":520 if nm=="Wage Sheet" else 120,"columnCount":30}}}})
    reqs.append({"deleteSheet":{"sheetId":IDS["Dashboard"]}})
    reqs.append({"deleteSheet":{"sheetId":IDS["Cost Report"]}})
    for i, nm in enumerate(VISIBLE + HIDDEN):
        sid = G.SHEET_ID[nm]
        props = {"sheetId":sid,"index":i,"hidden":nm in HIDDEN}
        fields = "index,hidden"
        if nm in COLOR:
            props["tabColorStyle"] = {"rgbColor":G.rgb(COLOR[nm])}; fields += ",tabColorStyle"
        if nm == "Start Here":
            props["title"] = "Help"; fields += ",title"
        reqs.append({"updateSheetProperties":{"properties":props,"fields":fields}})
    reqs.append({"updateSpreadsheetProperties":{"properties":{"title":"Construction ERP","timeZone":"Asia/Karachi"},"fields":"title,timeZone"}})
    return reqs

def link(nm, label=None):
    return f'=HYPERLINK("#gid={G.SHEET_ID[nm]}","{label or nm}")'

def home():
    sid = NEW["Home"]
    groups = [
      ("Every day (site)", GREEN, [("Labour Attendance","Mark each worker Present, Half day, Absent or Leave"),
                                   ("Site Expenses","Petty cash and small site payments"),
                                   ("Daily Diary","What work was done today, with photos link"),
                                   ("Labour Advances","Cash advance given to a worker, or taken back from wages")]),
      ("Money (office)", GOLD, [("Supplier Invoices","Bills from suppliers and subcontractors"),
                                ("Purchase Orders","Orders placed with suppliers"),
                                ("Measurements","Work measured for client billing"),
                                ("RA Bills","Running bills sent to the client"),
                                ("Receipts","Payments received from the client")]),
      ("Reports", RED, [("Main Dashboard","All projects on one screen"),
                        ("Project Dashboard","One project in detail: pick it in cell B2"),
                        ("Wage Sheet","Monthly wages for each mason and labourer: pick the month in B2")]),
      ("Setup (once)", NAVY, [("Projects","Add each project with contract value"),
                              ("Workers","Add each mason, helper, carpenter etc. with daily rate"),
                              ("Parties","Clients and suppliers"),
                              ("Budget","Budget for each project by cost code"),
                              ("BOQ","Contract bill of quantities and rates"),
                              ("Change Events","Extra work and client variations"),
                              ("Cost Codes","Your cost heads"),
                              ("Settings","Working hours per day and overtime rate"),
                              ("Start Here","Full help and definitions")]),
    ]
    rows = [["Construction ERP", None, None], ["Click a blue name to open that page.", None, None], [None, None, None]]
    fmts = []
    for title, color, items in groups:
        fmts.append((len(rows), color))
        rows.append([title, None, None])
        for nm, desc in items:
            rows.append([link(nm, "Help" if nm == "Start Here" else nm), desc, None])
        rows.append([None, None, None])
    rows.append(["Optional tabs (RFIs, Submittals, Documents, Quality & Punch, Safety, Lookahead, Leads, Requisitions, Goods Receipts) are hidden. To show one: View > Hidden sheets.", None, None])
    reqs = [G.rows_req(sid, 0, 0, rows),
            G.fmt_req(sid, 0, 1, 0, 1, bold=True, size=20, fg=NAVY),
            G.fmt_req(sid, 1, 2, 0, 1, italic=True, fg="595959"),
            G.fmt_req(sid, 3, len(rows), 0, 1, bold=True, size=12),
            G.fmt_req(sid, 3, len(rows), 1, 2, size=11, fg="404040"),
            G.fmt_req(sid, len(rows)-1, len(rows), 0, 1, italic=True, bold=False, size=10, fg="595959"),
            {"mergeCells":{"range":G.grid(sid, len(rows)-1, len(rows), 0, 2),"mergeType":"MERGE_ALL"}},
            G.fmt_req(sid, len(rows)-1, len(rows), 0, 2, wrap="WRAP"),
            {"updateDimensionProperties":{"range":{"sheetId":sid,"dimension":"ROWS","startIndex":3,"endIndex":len(rows)},"properties":{"pixelSize":30},"fields":"pixelSize"}},
            {"updateSheetProperties":{"properties":{"sheetId":sid,"gridProperties":{"hideGridlines":True}},"fields":"gridProperties.hideGridlines"}}]
    for r, color in fmts:
        reqs.append(G.fmt_req(sid, r, r+1, 0, 2, bold=True, size=13, fg="FFFFFF", bg=color, valign="MIDDLE"))
    reqs += G.widths(sid, [30, 70])
    return reqs

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_requests")
    os.makedirs(out, exist_ok=True)
    steps = {"1_structure":structure(),"2_main_dashboard":G.main_dashboard(),"3_project_dashboard":G.project_dashboard(),
             "4_wage_sheet":G.wage_sheet(),"5_home":home()}
    for k, v in steps.items():
        s = json.dumps(v, separators=(",",":"))
        open(os.path.join(out, k+".json"),"w").write(s)
        print(k, len(v), len(s))

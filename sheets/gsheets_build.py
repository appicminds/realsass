"""Generate Google Sheets batchUpdate requests for the Construction ERP workbook.

Writes one JSON file per step into sheets/gsheets_requests/. Each file is the `requests`
array for a spreadsheets.batchUpdate call (or a values payload for the text tabs).
Run:  python3 sheets/gsheets_build.py
"""
import json
import os
import datetime as dt

import build_workbook as B
from build_workbook import SPECS, LETTERS, LISTS, LIST_COL, ROWS, X, lookup
from openpyxl.utils import get_column_letter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsheets_requests")
os.makedirs(OUT, exist_ok=True)

PROJ_ROWS = 100
TAB_ORDER = (["Start Here", "Main Dashboard", "Project Dashboard", "Wage Sheet", "Settings", "Projects", "Parties",
              "Cost Codes", "Workers", "Labour Attendance", "Labour Advances", "Budget", "BOQ", "Measurements",
              "RA Bills", "Receipts", "Change Events", "Requisitions", "Purchase Orders", "Goods Receipts",
              "Supplier Invoices", "Site Expenses", "Daily Diary", "RFIs", "Submittals", "Documents",
              "Quality & Punch", "Safety", "Lookahead", "Leads", "Lists"])
SHEET_ID = {name: (0 if i == 0 else 1000 + i) for i, name in enumerate(TAB_ORDER)}


def rgb(h):
    h = h.lstrip("#")
    return {"red": round(int(h[0:2], 16) / 255, 3), "green": round(int(h[2:4], 16) / 255, 3), "blue": round(int(h[4:6], 16) / 255, 3)}


NAVY, TEAL, GREY, AUTO_BG, RED_BG, RED_FG, YELLOW, TOTAL_BG = (
    "1F3864", "0F5E5E", "D9D9D9", "F2F2F2", "F4CCCC", "990000", "FFF2CC", "DDEBF7")
FMT = {B.MONEY: {"type": "NUMBER", "pattern": '#,##0;[Red](#,##0);"-"'},
       B.QTY: {"type": "NUMBER", "pattern": '#,##0.00;[Red](#,##0.00);"-"'},
       B.PCT: {"type": "PERCENT", "pattern": '0.0%;(0.0%);"-"'},
       B.DATE: {"type": "DATE", "pattern": "yyyy-mm-dd"},
       B.INT: {"type": "NUMBER", "pattern": '#,##0;(#,##0);"-"'},
       "@": {"type": "TEXT"}}


def grid(sid, r0, r1, c0, c1):
    g = {"sheetId": sid, "startRowIndex": r0, "startColumnIndex": c0, "endColumnIndex": c1}
    if r1 is not None:
        g["endRowIndex"] = r1
    return g


def fmt_req(sid, r0, r1, c0, c1, bold=None, italic=None, fg=None, bg=None, size=None, number=None, wrap=None,
            halign=None, valign=None):
    f, fields = {}, []
    tf = {}
    if bold is not None:
        tf["bold"] = bold; fields.append("userEnteredFormat.textFormat.bold")
    if italic is not None:
        tf["italic"] = italic; fields.append("userEnteredFormat.textFormat.italic")
    if fg:
        tf["foregroundColorStyle"] = {"rgbColor": rgb(fg)}; fields.append("userEnteredFormat.textFormat.foregroundColorStyle")
    if size:
        tf["fontSize"] = size; fields.append("userEnteredFormat.textFormat.fontSize")
    if tf:
        f["textFormat"] = tf
    if bg:
        f["backgroundColorStyle"] = {"rgbColor": rgb(bg)}; fields.append("userEnteredFormat.backgroundColorStyle")
    if number:
        f["numberFormat"] = FMT[number]; fields.append("userEnteredFormat.numberFormat")
    if wrap:
        f["wrapStrategy"] = wrap; fields.append("userEnteredFormat.wrapStrategy")
    if halign:
        f["horizontalAlignment"] = halign; fields.append("userEnteredFormat.horizontalAlignment")
    if valign:
        f["verticalAlignment"] = valign; fields.append("userEnteredFormat.verticalAlignment")
    return {"repeatCell": {"range": grid(sid, r0, r1, c0, c1), "cell": {"userEnteredFormat": f}, "fields": ",".join(fields)}}


def serial(d):
    return (d - dt.date(1899, 12, 30)).days


def val(v):
    if isinstance(v, str) and v.startswith("="):
        return {"userEnteredValue": {"formulaValue": v}}
    if isinstance(v, str):
        return {"userEnteredValue": {"stringValue": v}}
    if isinstance(v, (dt.date,)):
        return {"userEnteredValue": {"numberValue": serial(v)}}
    if v is None:
        return {}
    return {"userEnteredValue": {"numberValue": v}}


def rows_req(sid, r0, c0, rows):
    return {"updateCells": {"rows": [{"values": [val(v) for v in row]} for row in rows],
                            "fields": "userEnteredValue", "start": {"sheetId": sid, "rowIndex": r0, "columnIndex": c0}}}


def widths(sid, ws):
    reqs, i = [], 0
    while i < len(ws):
        j = i
        while j + 1 < len(ws) and ws[j + 1] == ws[i]:
            j += 1
        reqs.append({"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": i, "endIndex": j + 1},
                                                   "properties": {"pixelSize": int(ws[i] * 7.5)}, "fields": "pixelSize"}})
        i = j + 1
    return reqs


def dv_req(sid, c, formula, r0=1, r1=ROWS + 1):
    return {"setDataValidation": {"range": grid(sid, r0, r1, c, c + 1), "rule": {
        "condition": {"type": "ONE_OF_RANGE", "values": [{"userEnteredValue": formula}]},
        "showCustomUi": True, "strict": False}}}


def flag_req(sid, c, r0=1, r1=ROWS + 1, formula=None):
    L = get_column_letter(c + 1)
    return {"addConditionalFormatRule": {"index": 0, "rule": {
        "ranges": [grid(sid, r0, r1, c, c + 1)],
        "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": formula or f"=LEN({L}{r0 + 1})>0"}]},
                        "format": {"backgroundColorStyle": {"rgbColor": rgb(RED_BG)},
                                   "textFormat": {"bold": True, "foregroundColorStyle": {"rgbColor": rgb(RED_FG)}}}}}}}


def header_reqs(sid, headers, autos, fill=NAVY, row=0):
    reqs = [rows_req(sid, row, 0, [headers]),
            fmt_req(sid, row, row + 1, 0, len(headers), bold=True, fg="FFFFFF", bg=fill, wrap="WRAP",
                    halign="CENTER", valign="MIDDLE")]
    for i, a in enumerate(autos):
        if a:
            reqs.append(fmt_req(sid, row, row + 1, i, i + 1, italic=True, fg="000000", bg=GREY))
    reqs.append({"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "ROWS", "startIndex": row, "endIndex": row + 1},
                                               "properties": {"pixelSize": 54}, "fields": "pixelSize"}})
    return reqs


def lst_range(name):
    c = LIST_COL[name]
    return f"=Lists!${c}$2:${c}$60"


def register(name):
    spec = SPECS[name]
    cols = spec["cols"]
    sid = SHEET_ID[name]
    L = LETTERS[name]
    c = lambda k: L[k]
    n = len(cols)
    reqs = header_reqs(sid, [cd["header"] + (" (auto)" if cd["kind"] == "auto" else "") for cd in cols],
                       [cd["kind"] == "auto" for cd in cols])
    examples = spec.get("example") or []
    if examples and not isinstance(examples[0], list):
        examples = [examples]
    row2 = []
    for i, cd in enumerate(cols):
        if cd["kind"] == "auto":
            row2.append(cd["f"](2, c))
        else:
            row2.append(examples[0][i] if examples and i < len(examples[0]) else None)
    reqs.append(rows_req(sid, 1, 0, [row2]))
    # copy formulas down, one request per auto column
    for i, cd in enumerate(cols):
        if cd["kind"] == "auto":
            reqs.append({"copyPaste": {"source": grid(sid, 1, 2, i, i + 1), "destination": grid(sid, 2, ROWS + 1, i, i + 1),
                                       "pasteType": "PASTE_FORMULA"}})
            reqs.append(fmt_req(sid, 1, ROWS + 1, i, i + 1, bg=AUTO_BG))
        if cd.get("fmt"):
            reqs.append(fmt_req(sid, 1, ROWS + 1, i, i + 1, number=cd["fmt"]))
        if cd.get("dv"):
            reqs.append(dv_req(sid, i, cd["dv"]))
        if cd.get("flag"):
            reqs.append(flag_req(sid, i))
    for ri, ex in enumerate(examples[1:], start=2):
        reqs.append(rows_req(sid, ri, 0, [[None if cols[i]["kind"] == "auto" else v for i, v in enumerate(ex)]]))
    if examples and name != "Cost Codes":
        reqs.append(fmt_req(sid, 1, 1 + len(examples), 0, n, italic=True, fg="7F7F7F"))
    reqs += widths(sid, [cd["width"] for cd in cols])
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {
        "frozenRowCount": 1, "frozenColumnCount": 0 if name == "Cost Codes" else 1}}, "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}})
    reqs.append({"setBasicFilter": {"filter": {"range": grid(sid, 0, ROWS + 1, 0, n)}}})
    return reqs


# ------------------------------------------------------------------ Lists, Settings
def lists_tab():
    sid = SHEET_ID["Lists"]
    names = list(LISTS)
    reqs = header_reqs(sid, names, [False] * len(names), fill="595959")
    maxlen = max(len(v) for v in LISTS.values())
    rows = [[LISTS[nm][j] if j < len(LISTS[nm]) else None for nm in names] for j in range(maxlen)]
    reqs.append(rows_req(sid, 1, 0, rows))
    reqs += widths(sid, [20] * len(names))
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 1}},
                                           "fields": "gridProperties.frozenRowCount"}})
    return reqs


def settings_tab():
    sid = SHEET_ID["Settings"]
    reqs = header_reqs(sid, ["Setting", "Value", "Used by"], [False] * 3)
    reqs.append(rows_req(sid, 1, 0, [
        ["Company name", "Your company", "Report headings"],
        ["Standard hours per day", 8, "Attendance: hours worked / standard hours = days counted"],
        ["Overtime multiplier", 1.5, "Attendance: overtime pay = daily rate / standard hours x OT hours x multiplier"],
        ["Currency", "PKR", "All amounts"]]))
    reqs.append(fmt_req(sid, 1, 5, 1, 2, fg="0000FF", bg=YELLOW))
    reqs += widths(sid, [30, 16, 70])
    return reqs


# ------------------------------------------------------------------ Main Dashboard
def main_dashboard():
    sid = SHEET_ID["Main Dashboard"]
    P = LETTERS["Projects"]
    first = 4  # 1-based data row

    def pj(k, r):
        return f"Projects!${P[k]}{r - 2}"

    month_start = "EOMONTH(TODAY(),-1)+1"
    cols = [
        ("Project", 11, None, lambda r: f'=IF(Projects!$A{r - 2}="","",Projects!$A{r - 2})'),
        ("Project name", 26, None, lambda r: f'=IF($A{r}="","",Projects!$B{r - 2})'),
        ("Status", 10, None, lambda r: f'=IF($A{r}="","",{pj("status", r)})'),
        ("Signed contract", 14, B.MONEY, lambda r: f'=IF($A{r}="","",N({pj("contract", r)}))'),
        ("Approved variations", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Change Events","approved_var")},{X("Change Events","project")},$A{r}))'),
        ("Revised contract", 14, B.MONEY, lambda r: f'=IF($A{r}="","",D{r}+E{r})'),
        ("Current budget", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Budget","current")},{X("Budget","project")},$A{r}))'),
        ("Actual cost A", 14, B.MONEY, lambda r: (f'=IF($A{r}="","",SUMIFS({X("Supplier Invoices","amount")},{X("Supplier Invoices","project")},$A{r},{X("Supplier Invoices","status")},"<>Draft")'
                                                 f'+SUMIFS({X("Labour Attendance","cost")},{X("Labour Attendance","project")},$A{r})+SUMIFS({X("Site Expenses","amount")},{X("Site Expenses","project")},$A{r}))')),
        ("Committed C", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Purchase Orders","open")},{X("Purchase Orders","project")},$A{r}))'),
        ("Uncommitted U", 14, B.MONEY, lambda r: f'=IF($A{r}="","",IF({pj("u", r)}="","Missing",{pj("u", r)}))'),
        ("EAC = A+C+U", 14, B.MONEY, lambda r: f'=IF($A{r}="","",IF(J{r}="Missing","Incomplete",H{r}+I{r}+J{r}))'),
        ("Forecast variance", 14, B.MONEY, lambda r: f'=IF($A{r}="","",IF(K{r}="Incomplete","Incomplete",G{r}-K{r}))'),
        ("Forecast margin", 14, B.MONEY, lambda r: f'=IF($A{r}="","",IF(K{r}="Incomplete","Incomplete",F{r}-K{r}))'),
        ("Margin %", 10, B.PCT, lambda r: f'=IF(OR($A{r}="",K{r}="Incomplete"),"",IF(F{r}=0,0,M{r}/F{r}))'),
        ("Verified, not billed", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Measurements","value")},{X("Measurements","project")},$A{r},{X("Measurements","bill")},""))'),
        ("Billed net", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","net")},{X("RA Bills","project")},$A{r},{X("RA Bills","status")},"<>Draft",{X("RA Bills","status")},"<>Rejected"))'),
        ("Received", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Receipts","amount")},{X("Receipts","project")},$A{r})+SUMIFS({X("Receipts","wht")},{X("Receipts","project")},$A{r}))'),
        ("Receivable", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","outstanding")},{X("RA Bills","project")},$A{r}))'),
        ("Overdue receivable", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","outstanding")},{X("RA Bills","project")},$A{r},{X("RA Bills","overdue")},">0"))'),
        ("Retention held", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","ret")},{X("RA Bills","project")},$A{r},{X("RA Bills","status")},"<>Draft",{X("RA Bills","status")},"<>Rejected"))'),
        ("Payables due", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Supplier Invoices","balance")},{X("Supplier Invoices","project")},$A{r}))'),
        ("Pending claims", 14, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Change Events","pending")},{X("Change Events","project")},$A{r}))'),
        ("Workers present today", 11, B.INT, lambda r: f'=IF($A{r}="","",COUNTIFS({X("Labour Attendance","project")},$A{r},{X("Labour Attendance","date")},TODAY(),{X("Labour Attendance","days")},">0"))'),
        ("Man-days this month", 11, B.QTY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Labour Attendance","days")},{X("Labour Attendance","project")},$A{r},{X("Labour Attendance","date")},">="&{month_start},{X("Labour Attendance","date")},"<="&EOMONTH(TODAY(),0)))'),
        ("Labour cost this month", 13, B.MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Labour Attendance","cost")},{X("Labour Attendance","project")},$A{r},{X("Labour Attendance","date")},">="&{month_start},{X("Labour Attendance","date")},"<="&EOMONTH(TODAY(),0)))'),
        ("Open items needing action", 12, B.INT, lambda r: (f'=IF($A{r}="","",COUNTIFS({X("Change Events","project")},$A{r},{X("Change Events","check")},"?*")'
                                                           f'+COUNTIFS({X("RFIs","project")},$A{r},{X("RFIs","check")},"?*")+COUNTIFS({X("Submittals","project")},$A{r},{X("Submittals","check")},"?*")'
                                                           f'+COUNTIFS({X("Quality & Punch","project")},$A{r},{X("Quality & Punch","check")},"?*")+COUNTIFS({X("Safety","project")},$A{r},{X("Safety","check")},"?*")'
                                                           f'+COUNTIFS({X("Lookahead","project")},$A{r},{X("Lookahead","ready")},"?*"))')),
        ("Critical punch open", 10, B.INT, lambda r: f'=IF($A{r}="","",COUNTIFS({X("Quality & Punch","project")},$A{r},{X("Quality & Punch","check")},"Blocks handover"))'),
    ]
    n = len(cols)
    reqs = [rows_req(sid, 0, 0, [["Main dashboard: all projects (PKR)", None, None, None, "As of", "=TODAY()"]]),
            fmt_req(sid, 0, 1, 0, 1, bold=True, size=14, fg=NAVY),
            fmt_req(sid, 0, 1, 4, 5, bold=True),
            fmt_req(sid, 0, 1, 5, 6, number=B.DATE, bold=True)]
    reqs += header_reqs(sid, [h for h, _, _, _ in cols], [False] * n, fill=TEAL, row=2)
    reqs.append(rows_req(sid, first - 1, 0, [[f(first) for _, _, _, f in cols]]))
    reqs.append({"copyPaste": {"source": grid(sid, first - 1, first, 0, n),
                               "destination": grid(sid, first, first - 1 + PROJ_ROWS, 0, n), "pasteType": "PASTE_FORMULA"}})
    totals = ["All projects"] + [None] * (n - 1)
    skip = {"Uncommitted U", "EAC = A+C+U", "Forecast variance", "Forecast margin", "Margin %"}
    for i, (h, _, fm, _) in enumerate(cols):
        if fm:
            reqs.append(fmt_req(sid, 1, first - 1 + PROJ_ROWS, i, i + 1, number=fm))
        if i >= 3 and fm and h not in skip:
            Lc = get_column_letter(i + 1)
            totals[i] = f"=SUM({Lc}{first}:{Lc}{first + PROJ_ROWS - 1})"
    totals[9] = "Forecast totals need U on every project"
    reqs.append(rows_req(sid, 1, 0, [totals]))
    reqs.append(fmt_req(sid, 1, 2, 0, n, bold=True, bg=TOTAL_BG))
    reqs.append(fmt_req(sid, 1, 2, 9, 10, italic=True, wrap="WRAP"))
    reqs += widths(sid, [w for _, w, _, _ in cols])
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 3, "frozenColumnCount": 2}},
                                           "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}})
    last = first + PROJ_ROWS - 1
    oi = [h for h, *_ in cols].index("Open items needing action")
    reqs.append(flag_req(sid, oi, first - 1, last, formula=f"=N({get_column_letter(oi + 1)}{first})>0"))
    reqs.append(flag_req(sid, oi + 1, first - 1, last, formula=f"=N({get_column_letter(oi + 2)}{first})>0"))
    reqs.append({"addConditionalFormatRule": {"index": 0, "rule": {"ranges": [grid(sid, first - 1, last, 9, 13)],
        "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": f'=OR(J{first}="Missing",J{first}="Incomplete")'}]},
                        "format": {"backgroundColorStyle": {"rgbColor": rgb(YELLOW)}}}}}})
    return reqs


# ------------------------------------------------------------------ Project Dashboard
def project_dashboard():
    sid = SHEET_ID["Project Dashboard"]
    P = "$B$2"
    MS = "$H$2"
    ME = "EOMONTH($H$2,0)"

    def pv(k):
        return lookup("Projects", "id", k, P, "0")

    A = (f'SUMIFS({X("Supplier Invoices","amount")},{X("Supplier Invoices","project")},{P},{X("Supplier Invoices","status")},"<>Draft")'
         f'+SUMIFS({X("Labour Attendance","cost")},{X("Labour Attendance","project")},{P})+SUMIFS({X("Site Expenses","amount")},{X("Site Expenses","project")},{P})')
    contract = [
        ("Signed contract", f"={pv('contract')}", B.MONEY),
        ("Approved variations", f'=SUMIFS({X("Change Events","approved_var")},{X("Change Events","project")},{P})', B.MONEY),
        ("Revised contract value", "=B5+B6", B.MONEY),
        ("Current approved budget", f'=SUMIFS({X("Budget","current")},{X("Budget","project")},{P})', B.MONEY),
        ("Actual cost A", "=" + A, B.MONEY),
        ("Committed cost C", f'=SUMIFS({X("Purchase Orders","open")},{X("Purchase Orders","project")},{P})', B.MONEY),
        ("Uncommitted cost U", f'=IF({lookup("Projects","id","u",P)}="","Missing",{lookup("Projects","id","u",P)})', B.MONEY),
        ("EAC = A + C + U", '=IF(B11="Missing","Incomplete",B9+B10+B11)', B.MONEY),
        ("Forecast variance (budget - EAC)", '=IF(B12="Incomplete","Incomplete",B8-B12)', B.MONEY),
        ("Forecast margin (contract - EAC)", '=IF(B12="Incomplete","Incomplete",B7-B12)', B.MONEY),
        ("Forecast margin %", '=IF(OR(B14="Incomplete",B7=0),"",B14/B7)', B.PCT),
    ]
    billing = [
        ("Verified work not yet billed", f'=SUMIFS({X("Measurements","value")},{X("Measurements","project")},{P},{X("Measurements","bill")},"")', B.MONEY),
        ("Billed net (certified bills)", f'=SUMIFS({X("RA Bills","net")},{X("RA Bills","project")},{P},{X("RA Bills","status")},"<>Draft",{X("RA Bills","status")},"<>Rejected")', B.MONEY),
        ("Received from client", f'=SUMIFS({X("Receipts","amount")},{X("Receipts","project")},{P})+SUMIFS({X("Receipts","wht")},{X("Receipts","project")},{P})', B.MONEY),
        ("Receivable outstanding", f'=SUMIFS({X("RA Bills","outstanding")},{X("RA Bills","project")},{P})', B.MONEY),
        ("Overdue receivable", f'=SUMIFS({X("RA Bills","outstanding")},{X("RA Bills","project")},{P},{X("RA Bills","overdue")},">0")', B.MONEY),
        ("Retention held by client", f'=SUMIFS({X("RA Bills","ret")},{X("RA Bills","project")},{P},{X("RA Bills","status")},"<>Draft",{X("RA Bills","status")},"<>Rejected")', B.MONEY),
        ("Supplier payables due", f'=SUMIFS({X("Supplier Invoices","balance")},{X("Supplier Invoices","project")},{P})', B.MONEY),
        ("Pending claims (not revenue)", f'=SUMIFS({X("Change Events","pending")},{X("Change Events","project")},{P})', B.MONEY),
        ("Disputed or rejected claims", f'=SUMIFS({X("Change Events","disputed")},{X("Change Events","project")},{P})', B.MONEY),
        ("Site expenses not settled", f'=SUMIFS({X("Site Expenses","amount")},{X("Site Expenses","project")},{P},{X("Site Expenses","settled")},"<>Yes")', B.MONEY),
    ]

    def cnt(sheet, key, crit='"?*"'):
        return f'COUNTIFS({X(sheet,"project")},{P},{X(sheet,key)},{crit})'
    alerts = [
        ("Change events needing notice", "=" + cnt("Change Events", "check"), B.INT),
        ("RFIs overdue", "=" + cnt("RFIs", "check"), B.INT),
        ("Submittals overdue or blocked", "=" + cnt("Submittals", "check"), B.INT),
        ("Critical punch items open", "=" + cnt("Quality & Punch", "check", '"Blocks handover"'), B.INT),
        ("Quality items overdue", "=" + cnt("Quality & Punch", "check", '"Overdue"'), B.INT),
        ("Safety actions overdue", "=" + cnt("Safety", "check"), B.INT),
        ("Lookahead activities not ready or late", "=" + cnt("Lookahead", "ready"), B.INT),
        ("Supplier invoices with checks", "=" + cnt("Supplier Invoices", "check"), B.INT),
        ("Measurements with checks", "=" + cnt("Measurements", "check"), B.INT),
        ("Attendance rows with checks", "=" + cnt("Labour Attendance", "check"), B.INT),
    ]
    LA = lambda k: X("Labour Attendance", k)
    labour = [
        ("Workers present today", f'=COUNTIFS({LA("project")},{P},{LA("date")},TODAY(),{LA("days")},">0")', B.INT),
        ("Absent today", f'=COUNTIFS({LA("project")},{P},{LA("date")},TODAY(),{LA("status")},"Absent")', B.INT),
        ("Man-days in month", f'=SUMIFS({LA("days")},{LA("project")},{P},{LA("date")},">="&{MS},{LA("date")},"<="&{ME})', B.QTY),
        ("Overtime hours in month", f'=SUMIFS({LA("ot")},{LA("project")},{P},{LA("date")},">="&{MS},{LA("date")},"<="&{ME})', B.QTY),
        ("Labour cost in month", f'=SUMIFS({LA("cost")},{LA("project")},{P},{LA("date")},">="&{MS},{LA("date")},"<="&{ME})', B.MONEY),
        ("Labour cost to date", f'=SUMIFS({LA("cost")},{LA("project")},{P})', B.MONEY),
        ("Worker advances given (project)", f'=SUMIFS({X("Labour Advances","amount")},{X("Labour Advances","project")},{P},{X("Labour Advances","type")},"Advance given")-SUMIFS({X("Labour Advances","amount")},{X("Labour Advances","project")},{P},{X("Labour Advances","type")},"Recovered from wages")', B.MONEY),
    ]
    reqs = [rows_req(sid, 0, 0, [["Project dashboard (PKR)", None, None, None, None, None, "As of", "=TODAY()"]]),
            rows_req(sid, 1, 0, [["Project", "PRJ-001", f'=IFERROR(INDEX(Projects!$B:$B,MATCH($B$2,Projects!$A:$A,0)),"Pick a project in B2")',
                                  None, None, None, "Labour month (first day)", "=EOMONTH(TODAY(),-1)+1"]]),
            fmt_req(sid, 0, 1, 0, 1, bold=True, size=14, fg=NAVY),
            fmt_req(sid, 1, 2, 0, 1, bold=True),
            fmt_req(sid, 1, 2, 1, 2, bold=True, fg="0000FF", bg=YELLOW),
            fmt_req(sid, 1, 2, 7, 8, bold=True, fg="0000FF", bg=YELLOW, number=B.DATE),
            fmt_req(sid, 0, 1, 7, 8, number=B.DATE, bold=True),
            fmt_req(sid, 1, 2, 2, 3, bold=True, italic=True),
            fmt_req(sid, 0, 2, 6, 7, bold=True),
            dv_req(sid, 1, B.PROJECTS, 1, 2)]

    def block(r0, c0, title, items):
        out = [rows_req(sid, r0, c0, [[title, None]]),
               fmt_req(sid, r0, r0 + 1, c0, c0 + 2, bold=True, fg="FFFFFF", bg=TEAL)]
        out.append(rows_req(sid, r0 + 1, c0, [[lab, f] for lab, f, _ in items]))
        for k, (_, _, fm) in enumerate(items):
            out.append(fmt_req(sid, r0 + 1 + k, r0 + 2 + k, c0 + 1, c0 + 2, number=fm, bold=True))
        return out
    # rows are 0-based here: title at row index 3 -> sheet row 4, items from row 5
    reqs += block(3, 0, "Contract and forecast", contract)
    reqs += block(3, 3, "Billing and cash", billing)
    reqs += block(3, 6, "Alerts (open items)", alerts)
    reqs.append(flag_req(sid, 7, 4, 4 + len(alerts), formula="=N(H5)>0"))
    reqs += block(17, 0, "Labour in selected month", labour)

    # Headcount by trade, D18:G34
    tr_col = LIST_COL["Trade"]
    reqs.append(rows_req(sid, 17, 3, [["Trade", "Present today", "Man-days in month", "Cost in month"]]))
    reqs.append(fmt_req(sid, 17, 18, 3, 7, bold=True, fg="FFFFFF", bg=TEAL, wrap="WRAP"))
    trade_rows = []
    for k in range(1):
        r = 19 + k
        lr = 2 + k
        trade_rows.append([f'=IF(Lists!${tr_col}{lr}="","",Lists!${tr_col}{lr})',
                           f'=IF($D{r}="","",COUNTIFS({LA("project")},{P},{LA("trade")},$D{r},{LA("date")},TODAY(),{LA("days")},">0"))',
                           f'=IF($D{r}="","",SUMIFS({LA("days")},{LA("project")},{P},{LA("trade")},$D{r},{LA("date")},">="&{MS},{LA("date")},"<="&{ME}))',
                           f'=IF($D{r}="","",SUMIFS({LA("cost")},{LA("project")},{P},{LA("trade")},$D{r},{LA("date")},">="&{MS},{LA("date")},"<="&{ME}))'])
    reqs.append(rows_req(sid, 18, 3, trade_rows))
    reqs.append({"copyPaste": {"source": grid(sid, 18, 19, 3, 7), "destination": grid(sid, 19, 38, 3, 7), "pasteType": "PASTE_FORMULA"}})
    reqs.append(fmt_req(sid, 18, 38, 4, 5, number=B.INT))
    reqs.append(fmt_req(sid, 18, 38, 5, 6, number=B.QTY))
    reqs.append(fmt_req(sid, 18, 38, 6, 7, number=B.MONEY))

    # Cost by cost code, A41:F
    r0 = 40
    reqs.append(rows_req(sid, r0, 0, [["Cost code", "Current budget", "Actual cost A", "Committed C", "Budget left after A and C", "% of budget used"]]))
    reqs.append(fmt_req(sid, r0, r0 + 1, 0, 6, bold=True, fg="FFFFFF", bg=TEAL, wrap="WRAP"))
    cc_rows = []
    for k in range(1):
        r = r0 + 2 + k
        cr = 2 + k
        cc_rows.append([f"=IF('Cost Codes'!$A{cr}=\"\",\"\",'Cost Codes'!$A{cr}&\"  \"&'Cost Codes'!$B{cr})",
                        f'=IF($A{r}="","",SUMIFS({X("Budget","current")},{X("Budget","project")},{P},{X("Budget","code")},\'Cost Codes\'!$A{cr}))',
                        (f'=IF($A{r}="","",SUMIFS({X("Supplier Invoices","amount")},{X("Supplier Invoices","project")},{P},{X("Supplier Invoices","code")},\'Cost Codes\'!$A{cr},{X("Supplier Invoices","status")},"<>Draft")'
                         f'+SUMIFS({LA("cost")},{LA("project")},{P},{LA("code")},\'Cost Codes\'!$A{cr})+SUMIFS({X("Site Expenses","amount")},{X("Site Expenses","project")},{P},{X("Site Expenses","code")},\'Cost Codes\'!$A{cr}))'),
                        f'=IF($A{r}="","",SUMIFS({X("Purchase Orders","open")},{X("Purchase Orders","project")},{P},{X("Purchase Orders","code")},\'Cost Codes\'!$A{cr}))',
                        f'=IF($A{r}="","",B{r}-C{r}-D{r})',
                        f'=IF($A{r}="","",IF(B{r}=0,0,(C{r}+D{r})/B{r}))'])
    reqs.append(rows_req(sid, r0 + 1, 0, cc_rows))
    reqs.append({"copyPaste": {"source": grid(sid, r0 + 1, r0 + 2, 0, 6), "destination": grid(sid, r0 + 2, r0 + 41, 0, 6), "pasteType": "PASTE_FORMULA"}})
    reqs.append(fmt_req(sid, r0 + 1, r0 + 41, 1, 5, number=B.MONEY))
    reqs.append(fmt_req(sid, r0 + 1, r0 + 41, 5, 6, number=B.PCT))
    reqs.append({"addConditionalFormatRule": {"index": 0, "rule": {"ranges": [grid(sid, r0 + 1, r0 + 41, 5, 6)],
        "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": f"=N(F{r0 + 2})>1"}]},
                        "format": {"backgroundColorStyle": {"rgbColor": rgb(RED_BG)}, "textFormat": {"bold": True, "foregroundColorStyle": {"rgbColor": rgb(RED_FG)}}}}}}})
    reqs += widths(sid, [34, 16, 4, 32, 15, 15, 34, 15])
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 2}},
                                           "fields": "gridProperties.frozenRowCount"}})
    return reqs


# ------------------------------------------------------------------ Wage Sheet
def wage_sheet():
    sid = SHEET_ID["Wage Sheet"]
    LA = lambda k: X("Labour Attendance", k)
    ADV = lambda k: X("Labour Advances", k)
    W = LETTERS["Workers"]
    MS, ME = "$B$2", "EOMONTH($B$2,0)"
    PRJ = 'IF($B$3="","*",$B$3)'
    first = 6

    def att(r, extra):
        return f'COUNTIFS({LA("worker")},$A{r},{LA("project")},{PRJ},{LA("date")},">="&{MS},{LA("date")},"<="&{ME}{extra})'

    def sm(col, r, extra=""):
        return f'SUMIFS({LA(col)},{LA("worker")},$A{r},{LA("project")},{PRJ},{LA("date")},">="&{MS},{LA("date")},"<="&{ME}{extra})'

    def adv(r, typ):
        return f'SUMIFS({ADV("amount")},{ADV("worker")},$A{r},{ADV("type")},"{typ}",{ADV("date")},">="&{MS},{ADV("date")},"<="&{ME})'
    cols = [
        ("Worker ID", 11, None, lambda r: f'=IF(Workers!$A{r - 4}="","",Workers!$A{r - 4})'),
        ("Name", 22, None, lambda r: f'=IF($A{r}="","",Workers!${W["name"]}{r - 4})'),
        ("Trade", 16, None, lambda r: f'=IF($A{r}="","",Workers!${W["trade"]}{r - 4})'),
        ("Daily rate", 11, B.MONEY, lambda r: f'=IF($A{r}="","",Workers!${W["rate"]}{r - 4})'),
        ("Present", 9, B.INT, lambda r: f'=IF($A{r}="","",{att(r, f",{LA("status")},\"Present\"")})'),
        ("Half days", 9, B.INT, lambda r: f'=IF($A{r}="","",{att(r, f",{LA("status")},\"Half day\"")})'),
        ("Absent", 9, B.INT, lambda r: f'=IF($A{r}="","",{att(r, f",{LA("status")},\"Absent\"")})'),
        ("Leave", 9, B.INT, lambda r: f'=IF($A{r}="","",{att(r, f",{LA("status")},\"Leave\"")})'),
        ("Days counted", 10, B.QTY, lambda r: f'=IF($A{r}="","",{sm("days", r)})'),
        ("Overtime hours", 10, B.QTY, lambda r: f'=IF($A{r}="","",{sm("ot", r)})'),
        ("Wages earned", 13, B.MONEY, lambda r: f'=IF($A{r}="","",{sm("cost", r)})'),
        ("Advance given this month", 13, B.MONEY, lambda r: f'=IF($A{r}="","",{adv(r, "Advance given")})'),
        ("Recovered this month", 13, B.MONEY, lambda r: f'=IF($A{r}="","",{adv(r, "Recovered from wages")})'),
        ("Net payable", 13, B.MONEY, lambda r: f'=IF($A{r}="","",K{r}-M{r})'),
        ("Advance balance (all time)", 13, B.MONEY, lambda r: f'=IF($A{r}="","",Workers!${W["adv_bal"]}{r - 4})'),
        ("Paid on", 11, B.DATE, None),
        ("Signature / thumb", 16, None, None),
    ]
    n = len(cols)
    reqs = [rows_req(sid, 0, 0, [["Monthly wage sheet (PKR)"]]),
            rows_req(sid, 1, 0, [["Month (first day)", "=EOMONTH(TODAY(),-1)+1", '="to "&TEXT(EOMONTH(B2,0),"yyyy-mm-dd")']]),
            rows_req(sid, 2, 0, [["Project (blank = all)", None, "Wages come from Labour Attendance; recoveries from Labour Advances."]]),
            fmt_req(sid, 0, 1, 0, 1, bold=True, size=14, fg=NAVY),
            fmt_req(sid, 1, 3, 0, 1, bold=True),
            fmt_req(sid, 1, 3, 1, 2, bold=True, fg="0000FF", bg=YELLOW),
            fmt_req(sid, 1, 2, 1, 2, number=B.DATE),
            fmt_req(sid, 1, 3, 2, 3, italic=True, fg="595959"),
            dv_req(sid, 1, B.PROJECTS, 2, 3)]
    reqs += header_reqs(sid, [h for h, *_ in cols], [False] * n, fill=TEAL, row=4)
    reqs.append(rows_req(sid, first - 1, 0, [[f(first) if f else None for _, _, _, f in cols]]))
    reqs.append({"copyPaste": {"source": grid(sid, first - 1, first, 0, 15),
                               "destination": grid(sid, first, first - 1 + ROWS, 0, 15), "pasteType": "PASTE_FORMULA"}})
    totals = ["Total"] + [None] * (n - 1)
    for i, (h, _, fm, f) in enumerate(cols):
        if fm:
            reqs.append(fmt_req(sid, 3, first - 1 + ROWS, i, i + 1, number=fm))
        if f and i >= 4 and h != "Advance balance (all time)" and fm != B.DATE:
            Lc = get_column_letter(i + 1)
            totals[i] = f"=SUM({Lc}{first}:{Lc}{first + ROWS - 1})"
    reqs.append(rows_req(sid, 3, 0, [totals]))
    reqs.append(fmt_req(sid, 3, 4, 0, n, bold=True, bg=TOTAL_BG))
    reqs += widths(sid, [w for _, w, _, _ in cols])
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 5, "frozenColumnCount": 2}},
                                           "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}})
    return reqs


# ------------------------------------------------------------------ Start Here
def start_here():
    sid = SHEET_ID["Start Here"]
    rows = [["Construction ERP", None],
            ["Built from the Construction Intelligence Platform PRD v4 (R1 core). Amounts in PKR excluding recoverable tax.", None],
            [None, None],
            ["How the tabs are marked", None],
            ["Dark blue header", "You type in this column. Many columns have dropdowns."],
            ["Grey header, (auto)", "Formula column. Do not type here; it fills in once the row's first column has a value."],
            ["Grey italic row", "Example row showing the expected format. Delete it (right-click the row number, Delete row) when you start."],
            ["Red cell", "Something needs attention: duplicate, overdue, missing approval or over a limit."],
            [None, None],
            ["Daily routine", None],
            ["Site supervisor", "Labour Attendance (one row per worker per day: Present, Half day, Absent or Leave), Daily Diary, Goods Receipts, Site Expenses, Quality & Punch, Safety."],
            ["Storekeeper / procurement", "Requisitions, Purchase Orders (one row per PO line), Goods Receipts."],
            ["Accountant", "Supplier Invoices, Receipts, Labour Advances, month-end Wage Sheet."],
            ["QS", "Measurements (cumulative quantities, set Status = Verified and the RA bill no.), RA Bills, Change Events, BOQ."],
            ["PM / owner", "Main Dashboard for all projects, Project Dashboard for one project. Update U (remaining uncommitted cost) on Projects monthly."],
            [None, None],
            ["First-time setup", None],
            ["1. Settings, Lists", "Check standard hours and overtime multiplier. Add your own trades, units or statuses at the bottom of any Lists column."],
            ["2. Cost Codes", "Replace the starter codes with your own."],
            ["3. Parties, Workers", "Add clients, suppliers and every mason, labourer and other worker with trade and daily rate."],
            ["4. Projects", "One row per project with contract value, retention, advance recovery and payment terms."],
            ["5. Budget, BOQ", "Approved budget by cost code; contract BOQ lines with Status = Approved. Add approved variations as new BOQ lines (version VO-01 etc.)."],
            [None, None],
            ["Key definitions", None],
            ["Actual cost A", "Supplier invoices (not Draft) + labour attendance cost + site expenses."],
            ["Committed cost C", "Approved PO amounts not yet invoiced."],
            ["Uncommitted cost U", "PM/QS estimate of remaining cost not in A or C. Left blank, the forecast shows Incomplete instead of zero."],
            ["EAC", "A + C + U. Forecast margin = revised contract - EAC. Forecast variance = current budget - EAC."],
            ["Revised contract", "Signed contract + approved variations. Pending claims are excluded."],
            ["RA bill net", "Gross certified work - retention (capped) - advance recovery (up to advance received) - other deductions."],
            ["Labour cost", "Daily rate x days counted (Present = 1 or hours / standard hours, Half day = 0.5) + overtime hours / standard hours x rate x multiplier."],
            ["Wage sheet net payable", "Wages earned in the month - advances recovered in the month."],
            [None, None],
            ["Limits", f"Each register has formulas for {ROWS} rows; to add more, copy the last row and paste below. Use Data > Protect sheets and ranges to lock approved BOQ lines, closed months and formula columns."],
            ]
    reqs = [rows_req(sid, 0, 0, rows),
            fmt_req(sid, 0, len(rows), 0, 2, wrap="WRAP", valign="TOP"),
            fmt_req(sid, 0, 1, 0, 1, bold=True, size=18, fg=NAVY),
            fmt_req(sid, 1, 2, 0, 1, italic=True, fg="595959"),
            {"mergeCells": {"range": grid(sid, 1, 2, 0, 2), "mergeType": "MERGE_ALL"}},
            fmt_req(sid, 4, len(rows), 0, 1, bold=True),
            fmt_req(sid, 4, 5, 0, 1, bg=NAVY, fg="FFFFFF"),
            fmt_req(sid, 5, 6, 0, 1, bg=GREY, italic=True),
            fmt_req(sid, 6, 7, 0, 1, italic=True, fg="7F7F7F", bold=False),
            fmt_req(sid, 7, 8, 0, 1, bg=RED_BG, fg=RED_FG)]
    for i, row in enumerate(rows):
        if row[1] is None and row[0] and i > 1:
            reqs.append(fmt_req(sid, i, i + 1, 0, 1, bold=True, size=12, fg=TEAL))
    reqs += widths(sid, [28, 110])
    return reqs


def setup():
    reqs = [{"updateSheetProperties": {"properties": {"sheetId": 0, "title": "Start Here", "tabColorStyle": {"rgbColor": rgb("C00000")}},
                                       "fields": "title,tabColorStyle"}}]
    for i, name in enumerate(TAB_ORDER[1:], start=1):
        color = "C00000" if i < 5 else ("595959" if name == "Lists" else SPECS[name]["tab_color"])
        cols = 40 if name == "Lists" else 30
        reqs.append({"addSheet": {"properties": {"sheetId": SHEET_ID[name], "title": name, "index": i,
                                                 "gridProperties": {"rowCount": ROWS + 20 if name not in ("Project Dashboard", "Main Dashboard", "Lists", "Settings") else 120, "columnCount": cols},
                                                 "tabColorStyle": {"rgbColor": rgb(color)}}}})
    reqs.append({"updateSpreadsheetProperties": {"properties": {"locale": "en_GB", "timeZone": "Asia/Karachi"},
                                                 "fields": "locale,timeZone"}})
    return reqs


if __name__ == "__main__":
    steps = {"00_setup": setup(), "01_lists": lists_tab(), "02_settings": settings_tab()}
    k = 3
    for name in TAB_ORDER:
        if name in SPECS:
            steps[f"{k:02d}_{name.replace(' ', '_').replace('&', 'and')}"] = register(name)
            k += 1
    steps[f"{k:02d}_main_dashboard"] = main_dashboard(); k += 1
    steps[f"{k:02d}_project_dashboard"] = project_dashboard(); k += 1
    steps[f"{k:02d}_wage_sheet"] = wage_sheet(); k += 1
    steps[f"{k:02d}_start_here"] = start_here()
    for nm, reqs in steps.items():
        s = json.dumps(reqs, separators=(",", ":"))
        open(os.path.join(OUT, nm + ".json"), "w").write(s)
        print(f"{nm:30s} {len(reqs):4d} requests {len(s):7d} bytes")

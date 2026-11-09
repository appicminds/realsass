"""Worker Payments log; Weekly Attendance gets Paid / Balance / Paid on; Weekly Pay shows them; Wage Sheet hidden."""
import json, os
import gsheets_build as G
import build_workbook as B

PAY, WA, WP, WS, HOME = 2009, 2005, 2006, 2004, 2001
NP = 1000
R = []
# 1. Payments tab
R.append({"addSheet": {"properties": {"sheetId": PAY, "title": "Worker Payments", "index": 8,
                                      "gridProperties": {"rowCount": NP + 20, "columnCount": 12},
                                      "tabColorStyle": {"rgbColor": G.rgb("38761D")}}}})
cols = [("Date paid", 12, "in", B.DATE), ("Week ending (Thu)", 13, "in", "WEEK"), ("Worker", 18, "in", None),
        ("Worker ID (auto)", 10, "auto", None), ("Amount paid (PKR)", 13, "in", B.MONEY), ("Mode", 12, "in", None),
        ("Paid by", 12, "in", None), ("Notes", 22, "in", None), ("Net pay for that week (auto)", 13, "auto", B.MONEY),
        ("Check (auto)", 26, "auto", None)]
R += G.header_reqs(PAY, [c[0] for c in cols], [c[2] == "auto" for c in cols])
reg = lambda c: f"'Weekly Attendance'!${c}$2:${c}$501"
f2 = [None, None, None,
      '=IF(C2="","",IFERROR(INDEX(Workers!$A:$A,MATCH(C2,Workers!$B:$B,0)),""))',
      None, None, None, None,
      f'=IF(OR(C2="",B2=""),"",SUMIFS({reg("V")},{reg("B")},D2,{reg("A")},B2))',
      (f'=IF(C2="","",IF(D2="","Worker not found",IF(WEEKDAY(B2)<>5,"Week ending must be a Thursday",'
       f'IF(COUNTIFS({reg("B")},D2,{reg("A")},B2)=0,"No attendance row for this week",'
       f'IF(SUMIFS($E$2:$E${NP},$D$2:$D${NP},D2,$B$2:$B${NP},B2)>I2,"Paid more than net pay","")))))')]
ex = [B.D(2026, 11, 26), B.D(2026, 11, 26), "Usman But", None, 5000, "Cash", "A. Khan", "Example row, delete when you start"]
R.append(G.rows_req(PAY, 1, 0, [[f if f else (ex[i] if i < len(ex) else None) for i, f in enumerate(f2)]]))
for i, (h, w, k, fm) in enumerate(cols):
    if k == "auto":
        R.append({"copyPaste": {"source": G.grid(PAY, 1, 2, i, i + 1), "destination": G.grid(PAY, 2, NP, i, i + 1), "pasteType": "PASTE_FORMULA"}})
        R.append(G.fmt_req(PAY, 1, NP, i, i + 1, bg=G.AUTO_BG))
        R.append({"addProtectedRange": {"protectedRange": {"range": G.grid(PAY, 1, NP, i, i + 1), "description": "Auto formula column", "warningOnly": True}}})
    if fm == "WEEK":
        R.append({"repeatCell": {"range": G.grid(PAY, 1, NP, i, i + 1), "cell": {"userEnteredFormat": {"numberFormat": {"type": "DATE", "pattern": "ddd yyyy-mm-dd"}}}, "fields": "userEnteredFormat.numberFormat"}})
    elif fm:
        R.append(G.fmt_req(PAY, 1, NP, i, i + 1, number=fm))
R.append(G.fmt_req(PAY, 1, 2, 0, len(cols), italic=True, fg="7F7F7F"))
R.append(G.fmt_req(PAY, 1, NP, 4, 5, bold=True))
R.append(G.dv_req(PAY, 2, "=Workers!$B$2:$B$501", 1, NP))
R.append(G.dv_req(PAY, 5, B.lst("Payment mode"), 1, NP))
R.append({"setDataValidation": {"range": G.grid(PAY, 1, NP, 0, 2), "rule": {"condition": {"type": "DATE_IS_VALID"}, "showCustomUi": True, "strict": False}}})
R.append(G.flag_req(PAY, 9, 1, NP))
R += G.widths(PAY, [c[1] for c in cols])
R.append({"updateSheetProperties": {"properties": {"sheetId": PAY, "gridProperties": {"frozenRowCount": 1}}, "fields": "gridProperties.frozenRowCount"}})
R.append({"setBasicFilter": {"filter": {"range": G.grid(PAY, 0, NP, 0, len(cols))}}})

# 2. Weekly Attendance: insert Paid + Balance after Net pay (V); old Paid on (now Y) becomes automatic
R.append({"insertDimension": {"range": {"sheetId": WA, "dimension": "COLUMNS", "startIndex": 22, "endIndex": 24}, "inheritFromBefore": True}})
pay = lambda c: f"'Worker Payments'!${c}$2:${c}${NP}"
R.append(G.rows_req(WA, 0, 22, [["Paid (PKR) (auto)", "Balance to pay (PKR) (auto)", "Paid on (auto)"]]))
R.append(G.rows_req(WA, 1, 22, [[f'=IF($A2="","",SUMIFS({pay("E")},{pay("D")},B2,{pay("B")},A2))',
                                 '=IF($A2="","",V2-W2)',
                                 f'=IF(OR($A2="",N(W2)=0),"",MAXIFS({pay("A")},{pay("D")},B2,{pay("B")},A2))']]))
R.append({"copyPaste": {"source": G.grid(WA, 1, 2, 22, 25), "destination": G.grid(WA, 2, 501, 22, 25), "pasteType": "PASTE_FORMULA"}})
R.append({"repeatCell": {"range": G.grid(WA, 0, 1, 22, 25), "cell": {"userEnteredFormat": {
    "textFormat": {"bold": True, "italic": True, "foregroundColorStyle": {"rgbColor": G.rgb("000000")}},
    "backgroundColorStyle": {"rgbColor": G.rgb("D9D9D9")}}},
    "fields": "userEnteredFormat.textFormat.bold,userEnteredFormat.textFormat.italic,userEnteredFormat.textFormat.foregroundColorStyle,userEnteredFormat.backgroundColorStyle"}})
R.append(G.fmt_req(WA, 1, 501, 22, 24, bg=G.AUTO_BG, number=B.MONEY, bold=True))
R.append({"repeatCell": {"range": G.grid(WA, 1, 501, 24, 25), "cell": {"userEnteredFormat": {
    "backgroundColorStyle": {"rgbColor": G.rgb("F2F2F2")}, "numberFormat": {"type": "DATE", "pattern": "yyyy-mm-dd"}}},
    "fields": "userEnteredFormat.backgroundColorStyle,userEnteredFormat.numberFormat"}})
R.append({"setDataValidation": {"range": G.grid(WA, 1, 501, 22, 25)}})
R.append({"addProtectedRange": {"protectedRange": {"range": G.grid(WA, 1, 501, 22, 25), "description": "Auto formula column", "warningOnly": True}}})
R.append({"addConditionalFormatRule": {"index": 0, "rule": {"ranges": [G.grid(WA, 1, 501, 23, 24)],
    "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": "=AND(N(X2)>0,$A2<TODAY())"}]},
                    "format": {"backgroundColorStyle": {"rgbColor": G.rgb("FCE5CD")}, "textFormat": {"foregroundColorStyle": {"rgbColor": G.rgb("B45F06")}}}}}}})
R += G.widths(WA, [0] * 22 + [12, 12, 11])[22:] if False else [
    {"updateDimensionProperties": {"range": {"sheetId": WA, "dimension": "COLUMNS", "startIndex": 22, "endIndex": 25}, "properties": {"pixelSize": 95}, "fields": "pixelSize"}}]

# 3. Weekly Pay: rebuild the table with Paid / Balance / Paid on
pick = ["B", "C", "D", "E", "G", "H", "I", "J", "K", "L", "M", "N", "S", "T", "U", "V", "W", "X", "Y", "Z"]
heads = ["Worker ID", "Worker", "Trade", "Main project", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "OT hrs",
         "Days to pay", "Wages", "Advance deducted", "Net pay", "Paid", "Balance", "Paid on", "Notes"]
arr = "{" + ",".join(reg(c) for c in pick) + "}"
filt = (f'=IFERROR(SORT(FILTER({arr},{reg("A")}=$B$2,IF($B$3="",{reg("A")}<>"",{reg("E")}=$B$3)),2,TRUE),"No attendance rows for this week")')
R.append({"updateCells": {"range": G.grid(WP, 3, 200, 0, 20), "fields": "userEnteredValue"}})
R.append(G.rows_req(WP, 3, 0, [["Total"] + [None] * 11 + [f"=SUM({c}6:{c}200)" for c in "MNOPQR"], heads, [filt]]))
R.append(G.rows_req(WP, 2, 2, [["Mark days on Weekly Attendance. Record payments on Worker Payments, or click Pay all to pay every balance for this week."]]))
R.append(G.fmt_req(WP, 3, 4, 0, 20, bold=True, bg=G.TOTAL_BG))
R.append(G.fmt_req(WP, 4, 5, 0, 20, bold=True, fg="FFFFFF", bg="38761D", wrap="WRAP", halign="CENTER", valign="MIDDLE"))
R.append(G.fmt_req(WP, 3, 200, 11, 13, number=B.QTY))
R.append(G.fmt_req(WP, 3, 200, 13, 18, number=B.MONEY))
R.append(G.fmt_req(WP, 5, 200, 15, 18, bold=True))
R.append(G.fmt_req(WP, 5, 200, 15, 16, bg="D9EAD3"))
R.append(G.fmt_req(WP, 5, 200, 16, 17, bg="FFFFFF"))
R.append(G.fmt_req(WP, 5, 200, 18, 19, number=B.DATE))
R.append({"addConditionalFormatRule": {"index": 0, "rule": {"ranges": [G.grid(WP, 5, 200, 17, 18)],
    "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": "=N(R6)>0"}]},
                    "format": {"backgroundColorStyle": {"rgbColor": G.rgb("FCE5CD")}, "textFormat": {"foregroundColorStyle": {"rgbColor": G.rgb("B45F06")}}}}}}})
R.append({"addConditionalFormatRule": {"index": 0, "rule": {"ranges": [G.grid(WP, 5, 200, 17, 18)],
    "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": "=AND(B6<>\"\",N(R6)=0,N(P6)>0)"}]},
                    "format": {"backgroundColorStyle": {"rgbColor": G.rgb("D9EAD3")}}}}}})
R += [{"updateDimensionProperties": {"range": {"sheetId": WP, "dimension": "COLUMNS", "startIndex": a, "endIndex": b}, "properties": {"pixelSize": px}, "fields": "pixelSize"}}
      for a, b, px in ((0, 1, 150), (1, 2, 135), (13, 18, 95), (18, 19, 90), (19, 20, 160))]

# 4. Worker Card: add Paid and Balance
pick = ["A", "E", "G", "H", "I", "J", "K", "L", "M", "N", "S", "T", "U", "V", "W", "X", "Y"]
heads = ["Week ending", "Main project", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "OT hrs", "Days to pay",
         "Wages", "Advance deducted", "Net pay", "Paid", "Balance", "Paid on"]
arr = "{" + ",".join(reg(c) for c in pick) + "}"
filt = (f'=IFERROR(SORT(FILTER({arr},{reg("C")}=$B$2,{reg("A")}>=$B$3,{reg("A")}<=EOMONTH($B$3,0)),1,TRUE),"No weeks for this worker in this month")')
WC = 2007
R.append({"updateCells": {"range": G.grid(WC, 3, 60, 0, 17), "fields": "userEnteredValue"}})
R.append(G.rows_req(WC, 3, 0, [["Month total"] + [None] * 8 + [f"=SUM({c}6:{c}60)" for c in "JKLMNOP"], heads, [filt]]))
R.append(G.fmt_req(WC, 3, 4, 0, 17, bold=True, bg=G.TOTAL_BG))
R.append(G.fmt_req(WC, 4, 5, 0, 17, bold=True, fg="FFFFFF", bg="38761D", wrap="WRAP", halign="CENTER", valign="MIDDLE"))
R.append(G.fmt_req(WC, 3, 60, 11, 16, number=B.MONEY))
R.append(G.fmt_req(WC, 5, 60, 16, 17, number=B.DATE))
R.append({"updateDimensionProperties": {"range": {"sheetId": WC, "dimension": "COLUMNS", "startIndex": 14, "endIndex": 17}, "properties": {"pixelSize": 90}, "fields": "pixelSize"}})

# 5. Hide the Wage Sheet; Home link points to Worker Payments instead
R.append({"updateSheetProperties": {"properties": {"sheetId": WS, "hidden": True}, "fields": "hidden"}})
R.append(G.rows_req(HOME, 19, 0, [['=HYPERLINK("#gid=2009","Worker Payments")',
                                   "Record each payment to a worker (date, week, amount). Weekly Attendance and Weekly Pay update by themselves.",
                                   "+ Add"]]))
R.append({"updateCells": {"rows": [{"values": [{"note": "Script: form_Worker_Payments"}]}], "fields": "note", "start": {"sheetId": HOME, "rowIndex": 19, "columnIndex": 2}}})
R.append({"repeatCell": {"range": G.grid(HOME, 19, 20, 2, 3), "cell": {"userEnteredFormat": {
    "backgroundColorStyle": {"rgbColor": G.rgb("38761D")}, "textFormat": {"bold": True, "foregroundColorStyle": {"rgbColor": G.rgb("FFFFFF")}},
    "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"}},
    "fields": "userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat.bold,userEnteredFormat.textFormat.foregroundColorStyle,userEnteredFormat.horizontalAlignment,userEnteredFormat.verticalAlignment"}})

if __name__ == "__main__":
    s = json.dumps(R)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_requests", "15_payments.json"), "w").write(s)
    print(len(R), len(s))

"""Weekly attendance register (Fri-Thu, paid Thursday) for the live sheet, plus Weekly Pay and Worker Card views,
and the dashboard / wage sheet / advance formulas that read from it."""
import json, os
import gsheets_build as G
from simplify_live import IDS, NEW
import build_workbook as B

WA_ID, PAY_ID, CARD_ID = 2005, 2006, 2007
WA = "'Weekly Attendance'!"
N = 501  # last data row
DAYS = ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"]
DAYCOLS = ["G", "H", "I", "J", "K", "L", "M"]
COLS = [  # header, width, kind, fmt
    ("Week ending (Thu)", 13, "in", B.DATE), ("Worker ID", 10, "in", None), ("Name", 18, "auto", None),
    ("Trade", 14, "auto", None), ("Main project", 12, "in", None), ("Daily rate (PKR)", 11, "auto", B.MONEY),
] + [(d, 9, "in", None) for d in DAYS] + [
    ("Overtime hours", 9, "in", B.QTY), ("Full days", 8, "auto", B.QTY), ("Half days", 8, "auto", B.QTY),
    ("Absent", 8, "auto", B.QTY), ("Leave", 8, "auto", B.QTY), ("Days to pay", 9, "auto", B.QTY),
    ("Wages (PKR)", 12, "auto", B.MONEY), ("Advance deducted (PKR)", 12, "in", B.MONEY),
    ("Net pay (PKR)", 12, "auto", B.MONEY), ("Paid on", 11, "in", B.DATE), ("Notes / signature", 18, "in", None),
    ("Check", 24, "auto", None)]


def rng(c):
    return f"{WA}${c}$2:${c}${N}"


def row_formulas(r):
    g = f"G{r}:M{r}"
    return [None, None,
            f'=IF($A{r}="","",IFERROR(INDEX(Workers!$B:$B,MATCH(B{r},Workers!$A:$A,0)),""))',
            f'=IF($A{r}="","",IFERROR(INDEX(Workers!$C:$C,MATCH(B{r},Workers!$A:$A,0)),""))',
            None,
            f'=IF($A{r}="","",IFERROR(INDEX(Workers!$E:$E,MATCH(B{r},Workers!$A:$A,0)),0))'] + [None] * 7 + [
        None,
        f'=IF($A{r}="","",COUNTIF({g},"?*")-COUNTIF({g},"H")-COUNTIF({g},"H *")-COUNTIF({g},"A")-COUNTIF({g},"L"))',
        f'=IF($A{r}="","",COUNTIF({g},"H")+COUNTIF({g},"H *"))',
        f'=IF($A{r}="","",COUNTIF({g},"A"))',
        f'=IF($A{r}="","",COUNTIF({g},"L"))',
        f'=IF($A{r}="","",O{r}+0.5*P{r})',
        f'=IF($A{r}="","",F{r}*(S{r}+N(N{r})/Settings!$B$3*Settings!$B$4))',
        None,
        f'=IF($A{r}="","",T{r}-N(U{r}))',
        None, None,
        (f'=IF($A{r}="","",IF(WEEKDAY(A{r})<>5,"Week ending must be a Thursday",'
         f'IF(COUNTIFS($A$2:$A${N},A{r},$B$2:$B${N},B{r})>1,"Worker twice in this week",'
         f'IF(AND(E{r}="",COUNTIF({g},"P")+COUNTIF({g},"H")>0),"Main project missing",'
         f'IF(COUNTA({g})=0,"No days marked","")))))')]


# ---------- shared formula pieces for other tabs (p = project cell, mask = extra SUMPRODUCT factor) ----------
def day_weight(c, p):
    x, e = rng(c), rng("E")
    return f'(({x}="P")+0.5*({x}="H"))*({e}={p})+({x}={p})+0.5*({x}="H "&{p})'


def all_days(p):
    return "+".join(f"({day_weight(c, p)})" for c in DAYCOLS)


def mask_month(ms, me):
    return f"({rng('A')}>={ms})*({rng('A')}<={me})"


MASK_ALL = f"({rng('A')}<>\"\")"


def wk_mandays(p, mask):
    return f"SUMPRODUCT({mask}*({all_days(p)}))"


def wk_cost(p, mask):
    return (f"(SUMPRODUCT({mask}*{rng('F')}*({all_days(p)}))"
            f"+SUMPRODUCT({mask}*({rng('E')}={p})*{rng('F')}*{rng("N")})/Settings!$B$3*Settings!$B$4)")


def wk_ot(p, mask):
    return f"SUMPRODUCT({mask}*({rng('E')}={p})*{rng("N")})"


TODAY_WK = "(TODAY()+MOD(5-WEEKDAY(TODAY()),7))"
TODAY_COL = "CHOOSE(7-MOD(5-WEEKDAY(TODAY()),7)," + ",".join(rng(c) for c in DAYCOLS) + ")"


def wk_present_today(p, extra="1"):
    x, e = TODAY_COL, rng("E")
    return (f"SUMPRODUCT(({rng('A')}={TODAY_WK})*{extra}*((({x}=\"P\")+({x}=\"H\"))*({e}={p})+({x}={p})+({x}=\"H \"&{p})))")


def wk_absent_today(p):
    x = TODAY_COL
    return f"SUMPRODUCT(({rng('A')}={TODAY_WK})*({rng('E')}={p})*({x}=\"A\"))"


def build():
    out = {}
    # 1. structure: new tabs, Lists day-code list, Settings labour cost code
    reqs = []
    for sid, title, rows in ((WA_ID, "Weekly Attendance", 520), (PAY_ID, "Weekly Pay", 200), (CARD_ID, "Worker Card", 200)):
        reqs.append({"addSheet": {"properties": {"sheetId": sid, "title": title, "index": 4,
                                                 "gridProperties": {"rowCount": rows, "columnCount": 30},
                                                 "tabColorStyle": {"rgbColor": G.rgb("38761D" if sid == WA_ID else "C00000")}}}})
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": IDS["Lists"], "gridProperties": {"rowCount": 400, "columnCount": 40}},
                                           "fields": "gridProperties.rowCount,gridProperties.columnCount"}})
    reqs.append(G.rows_req(IDS["Lists"], 0, 34, [["Day code (auto)"], [
        '={"P";"H";"A";"L";FILTER(Projects!$A$2:$A$501,Projects!$A$2:$A$501<>"");'
        'ARRAYFORMULA("H "&FILTER(Projects!$A$2:$A$501,Projects!$A$2:$A$501<>""))}']]))
    reqs.append(G.rows_req(IDS["Settings"], 5, 0, [["Labour cost code (Weekly Attendance)", "06-LAB",
                                                    "Weekly attendance wages are charged to this cost code"]]))
    reqs.append(G.fmt_req(IDS["Settings"], 5, 6, 1, 2, fg="0000FF", bg="FFF2CC"))
    out["8_weekly_structure"] = reqs

    # 2. Weekly Attendance tab
    sid = WA_ID
    reqs = G.header_reqs(sid, [h + (" (auto)" if k == "auto" else "") for h, _, k, _ in COLS], [k == "auto" for _, _, k, _ in COLS])
    ex = ["2026-11-26", "W-001", None, None, "PRJ-001", None, "", "P", "P", "H", "P", "A", "P", 2,
          None, None, None, None, None, None, 2000, None, None, "Example row, delete when you start", None]
    row2 = [f if f else (ex[i] if ex[i] not in (None, "") else None) for i, f in enumerate(row_formulas(2))]
    row2[0] = B.D(2026, 11, 26)
    reqs.append(G.rows_req(sid, 1, 0, [row2]))
    for i, (h, w, k, fm) in enumerate(COLS):
        if k == "auto":
            reqs.append({"copyPaste": {"source": G.grid(sid, 1, 2, i, i + 1), "destination": G.grid(sid, 2, N, i, i + 1), "pasteType": "PASTE_FORMULA"}})
            reqs.append(G.fmt_req(sid, 1, N, i, i + 1, bg=G.AUTO_BG))
        if fm:
            reqs.append(G.fmt_req(sid, 1, N, i, i + 1, number=fm))
    reqs.append(G.fmt_req(sid, 1, 2, 0, len(COLS), italic=True, fg="7F7F7F"))
    reqs.append(G.fmt_req(sid, 1, N, 6, 13, halign="CENTER", bold=True))
    reqs.append(G.fmt_req(sid, 0, 1, 6, 13, bg="38761D"))
    reqs.append(G.fmt_req(sid, 1, N, 21, 22, bold=True))
    reqs.append(G.dv_req(sid, 1, "='Workers'!$A$2:$A$501", 1, N))
    reqs.append(G.dv_req(sid, 4, "='Projects'!$A$2:$A$501", 1, N))
    reqs.append({"setDataValidation": {"range": G.grid(sid, 1, N, 6, 13), "rule": {
        "condition": {"type": "ONE_OF_RANGE", "values": [{"userEnteredValue": "=Lists!$AI$2:$AI$400"}]}, "showCustomUi": True, "strict": False}}})
    reqs.append({"setDataValidation": {"range": G.grid(sid, 1, N, 0, 1), "rule": {
        "condition": {"type": "DATE_IS_VALID"}, "showCustomUi": True, "strict": False}}})

    def cf(formula, bg, fg=None, rngs=None):
        fmt = {"backgroundColorStyle": {"rgbColor": G.rgb(bg)}}
        if fg:
            fmt["textFormat"] = {"foregroundColorStyle": {"rgbColor": G.rgb(fg)}}
        return {"addConditionalFormatRule": {"index": 0, "rule": {"ranges": rngs or [G.grid(sid, 1, N, 6, 13)],
                "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": formula}]}, "format": fmt}}}}
    reqs += [cf('=G2="P"', "D9EAD3", "274E13"), cf('=OR(G2="H",LEFT(G2,2)="H ")', "FFF2CC", "7F6000"),
             cf('=G2="A"', "F4CCCC", "990000"), cf('=G2="L"', "E0E0E0", "595959"),
             cf('=AND(LEN(G2)>1,LEFT(G2,2)<>"H ")', "CFE2F3", "1F3864")]
    reqs.append(G.flag_req(sid, 24, 1, N))
    reqs += G.widths(sid, [w for _, w, _, _ in COLS])
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 3}},
                                           "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}})
    reqs.append({"setBasicFilter": {"filter": {"range": G.grid(sid, 0, N, 0, len(COLS))}}})
    reqs.append({"addProtectedRange": {"protectedRange": {"range": G.grid(sid, 1, N, 2, 4), "description": "Auto formula column", "warningOnly": True}}})
    reqs.append({"addProtectedRange": {"protectedRange": {"range": G.grid(sid, 1, N, 5, 6), "description": "Auto formula column", "warningOnly": True}}})
    reqs.append({"addProtectedRange": {"protectedRange": {"range": G.grid(sid, 1, N, 14, 20), "description": "Auto formula column", "warningOnly": True}}})
    reqs.append({"addProtectedRange": {"protectedRange": {"range": G.grid(sid, 1, N, 21, 22), "description": "Auto formula column", "warningOnly": True}}})
    reqs.append({"addProtectedRange": {"protectedRange": {"range": G.grid(sid, 1, N, 24, 25), "description": "Auto formula column", "warningOnly": True}}})
    out["9_weekly_tab"] = reqs

    # 3. Weekly Pay tab
    sid = PAY_ID
    pick = ["B", "C", "D", "E"] + DAYCOLS + ["N", "S", "T", "U", "V", "W", "X"]
    heads = ["Worker ID", "Name", "Trade", "Main project"] + DAYS + ["OT hrs", "Days to pay", "Wages", "Advance deducted", "Net pay", "Paid on", "Signature / notes"]
    arr = "{" + ",".join(rng(c) for c in pick) + "}"
    filt = (f'=IFERROR(SORT(FILTER({arr},{rng("A")}=$B$2,IF($B$3="",{rng("A")}<>"",{rng("E")}=$B$3)),2,TRUE),"No attendance rows for this week")')
    reqs = [G.rows_req(sid, 0, 0, [["Weekly pay sheet (PKR)"],
                                   ["Pay day (Thursday)", "=TODAY()+MOD(5-WEEKDAY(TODAY()),7)", '=IF(WEEKDAY(B2)<>5,"Pick a Thursday","Week "&TEXT(B2-6,"ddd d mmm")&" to "&TEXT(B2,"ddd d mmm yyyy"))'],
                                   ["Project (blank = all)", None, "Mark days on Weekly Attendance. This page only shows them."],
                                   ["Total", None, None, None, None, None, None, None, None, None, None,
                                    "=SUM(L6:L200)", "=SUM(M6:M200)", "=SUM(N6:N200)", "=SUM(O6:O200)", "=SUM(P6:P200)"],
                                   heads, [filt]]),
            G.fmt_req(sid, 0, 1, 0, 1, bold=True, size=14, fg=G.NAVY),
            G.fmt_req(sid, 1, 3, 0, 1, bold=True),
            G.fmt_req(sid, 1, 3, 1, 2, bold=True, fg="0000FF", bg="FFF2CC", number=B.DATE),
            G.fmt_req(sid, 1, 3, 2, 3, italic=True, fg="595959"),
            G.dv_req(sid, 1, "='Projects'!$A$2:$A$501", 2, 3),
            G.fmt_req(sid, 3, 4, 0, len(heads), bold=True, bg=G.TOTAL_BG),
            G.fmt_req(sid, 4, 5, 0, len(heads), bold=True, fg="FFFFFF", bg="38761D", wrap="WRAP", halign="CENTER", valign="MIDDLE"),
            G.fmt_req(sid, 5, 200, 4, 11, halign="CENTER", bold=True),
            G.fmt_req(sid, 3, 200, 11, 13, number=B.QTY),
            G.fmt_req(sid, 3, 200, 13, 16, number=B.MONEY),
            G.fmt_req(sid, 5, 200, 15, 16, bold=True, bg="D9EAD3"),
            G.fmt_req(sid, 5, 200, 16, 17, number=B.DATE)]
    reqs += G.widths(sid, [22, 18, 14, 12] + [7] * 7 + [8, 9, 11, 11, 11, 11, 22])
    reqs.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 5, "frozenColumnCount": 2}},
                                           "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}})
    out["10_weekly_pay"] = reqs

    # 4. Worker Card tab
    sid = CARD_ID
    pick = ["A", "E"] + DAYCOLS + ["N", "S", "T", "U", "V", "W"]
    heads = ["Week ending", "Main project"] + DAYS + ["OT hrs", "Days to pay", "Wages", "Advance deducted", "Net pay", "Paid on"]
    arr = "{" + ",".join(rng(c) for c in pick) + "}"
    filt = (f'=IFERROR(SORT(FILTER({arr},{rng("B")}=$B$2,{rng("A")}>=$B$3,{rng("A")}<=EOMONTH($B$3,0)),1,TRUE),"No weeks for this worker in this month")')
    reqs = [G.rows_req(sid, 0, 0, [["Worker card"],
                                   ["Worker", "W-001", '=IFERROR(INDEX(Workers!$B:$B,MATCH(B2,Workers!$A:$A,0))&"  ("&INDEX(Workers!$C:$C,MATCH(B2,Workers!$A:$A,0))&", "&TEXT(INDEX(Workers!$E:$E,MATCH(B2,Workers!$A:$A,0)),"#,##0")&" per day)","Pick a worker")'],
                                   ["Month (first day)", "=EOMONTH(TODAY(),-1)+1", "Weeks are counted in the month of their Thursday pay day."],
                                   ["Month total", None, None, None, None, None, None, None, None,
                                    "=SUM(J6:J60)", "=SUM(K6:K60)", "=SUM(L6:L60)", "=SUM(M6:M60)", "=SUM(N6:N60)", None],
                                   heads, [filt]]),
            G.rows_req(sid, 1, 9, [["Advance balance now", f"=IFERROR(INDEX(Workers!$L:$L,MATCH(B2,Workers!$A:$A,0)),0)"]]),
            G.rows_req(sid, 2, 9, [["Absent days in month", f'=SUMIFS({rng("Q")},{rng("B")},$B$2,{rng("A")},">="&$B$3,{rng("A")},"<="&EOMONTH($B$3,0))']]),
            G.fmt_req(sid, 0, 1, 0, 1, bold=True, size=14, fg=G.NAVY),
            G.fmt_req(sid, 1, 3, 0, 1, bold=True),
            G.fmt_req(sid, 1, 3, 1, 2, bold=True, fg="0000FF", bg="FFF2CC"),
            G.fmt_req(sid, 2, 3, 1, 2, number=B.DATE),
            G.fmt_req(sid, 1, 2, 2, 3, bold=True, size=12),
            G.fmt_req(sid, 2, 3, 2, 3, italic=True, fg="595959"),
            G.fmt_req(sid, 1, 3, 9, 10, bold=True),
            G.fmt_req(sid, 1, 3, 10, 11, bold=True, number=B.MONEY),
            G.dv_req(sid, 1, "='Workers'!$A$2:$A$501", 1, 2),
            G.fmt_req(sid, 3, 4, 0, len(heads), bold=True, bg=G.TOTAL_BG),
            G.fmt_req(sid, 4, 5, 0, len(heads), bold=True, fg="FFFFFF", bg="38761D", wrap="WRAP", halign="CENTER", valign="MIDDLE"),
            G.fmt_req(sid, 5, 60, 0, 1, number=B.DATE),
            G.fmt_req(sid, 5, 60, 2, 9, halign="CENTER", bold=True),
            G.fmt_req(sid, 3, 60, 9, 11, number=B.QTY),
            G.fmt_req(sid, 3, 60, 11, 14, number=B.MONEY),
            G.fmt_req(sid, 5, 60, 14, 15, number=B.DATE)]
    for formula, bg in (('=C6="P"', "D9EAD3"), ('=OR(C6="H",LEFT(C6,2)="H ")', "FFF2CC"), ('=C6="A"', "F4CCCC"), ('=C6="L"', "E0E0E0")):
        reqs.append({"addConditionalFormatRule": {"index": 0, "rule": {"ranges": [G.grid(sid, 5, 60, 2, 9)],
                     "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": formula}]},
                                     "format": {"backgroundColorStyle": {"rgbColor": G.rgb(bg)}}}}}})
    reqs += G.widths(sid, [17, 13] + [7] * 7 + [18, 12, 11, 11, 11, 11])
    out["11_worker_card"] = reqs
    return out


if __name__ == "__main__":
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_requests")
    for k, v in build().items():
        s = json.dumps(v, separators=(",", ":"))
        open(os.path.join(d, k + ".json"), "w").write(s)
        print(k, len(v), len(s))


def integration():
    """Formulas that add the weekly register to Workers, dashboards and the monthly wage sheet."""
    MS, ME = "EOMONTH(TODAY(),-1)+1", "EOMONTH(TODAY(),0)"
    f = {}
    f["workers_L2"] = ('=IF($A2="","",SUMIFS(\'Labour Advances\'!$E:$E,\'Labour Advances\'!$B:$B,A2,\'Labour Advances\'!$D:$D,"Advance given")'
                       '-SUMIFS(\'Labour Advances\'!$E:$E,\'Labour Advances\'!$B:$B,A2,\'Labour Advances\'!$D:$D,"Recovered from wages")'
                       f'-SUMIFS({rng("U")},{rng("B")},A2))')
    p = "$A4"
    f["main_H4"] = ('=IF($A4="","",SUMIFS(\'Supplier Invoices\'!$J:$J,\'Supplier Invoices\'!$G:$G,$A4,\'Supplier Invoices\'!$M:$M,"<>Draft")'
                    '+SUMIFS(\'Labour Attendance\'!$O:$O,\'Labour Attendance\'!$B:$B,$A4)+SUMIFS(\'Site Expenses\'!$F:$F,\'Site Expenses\'!$B:$B,$A4)'
                    f'+{wk_cost(p, MASK_ALL)})')
    f["main_W4"] = (f'=IF($A4="","",COUNTIFS(\'Labour Attendance\'!$B:$B,$A4,\'Labour Attendance\'!$A:$A,TODAY(),\'Labour Attendance\'!$N:$N,">0")'
                    f'+{wk_present_today(p)})')
    f["main_X4"] = (f'=IF($A4="","",SUMIFS(\'Labour Attendance\'!$N:$N,\'Labour Attendance\'!$B:$B,$A4,\'Labour Attendance\'!$A:$A,">="&{MS},\'Labour Attendance\'!$A:$A,"<="&{ME})'
                    f'+{wk_mandays(p, mask_month(MS, ME))})')
    f["main_Y4"] = (f'=IF($A4="","",SUMIFS(\'Labour Attendance\'!$O:$O,\'Labour Attendance\'!$B:$B,$A4,\'Labour Attendance\'!$A:$A,">="&{MS},\'Labour Attendance\'!$A:$A,"<="&{ME})'
                    f'+{wk_cost(p, mask_month(MS, ME))})')
    P, PMS, PME = "$B$2", "$H$2", "EOMONTH($H$2,0)"
    LA = "'Labour Attendance'!"
    f["pd_B9"] = ("=SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$B$2,'Supplier Invoices'!$M:$M,\"<>Draft\")"
                  "+SUMIFS('Labour Attendance'!$O:$O,'Labour Attendance'!$B:$B,$B$2)+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$B$2)"
                  f"+{wk_cost(P, MASK_ALL)}")
    f["pd_B19"] = f"=COUNTIFS({LA}$B:$B,$B$2,{LA}$A:$A,TODAY(),{LA}$N:$N,\">0\")+{wk_present_today(P)}"
    f["pd_B20"] = f"=COUNTIFS({LA}$B:$B,$B$2,{LA}$A:$A,TODAY(),{LA}$F:$F,\"Absent\")+{wk_absent_today(P)}"
    f["pd_B21"] = f"=SUMIFS({LA}$N:$N,{LA}$B:$B,$B$2,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+{wk_mandays(P, mask_month(PMS, PME))}"
    f["pd_B22"] = f"=SUMIFS({LA}$I:$I,{LA}$B:$B,$B$2,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+{wk_ot(P, mask_month(PMS, PME))}"
    f["pd_B23"] = f"=SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+{wk_cost(P, mask_month(PMS, PME))}"
    f["pd_B24"] = f"=SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2)+{wk_cost(P, MASK_ALL)}"
    f["pd_B25"] = ("=SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$F:$F,$B$2,'Labour Advances'!$D:$D,\"Advance given\")"
                   "-SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$F:$F,$B$2,'Labour Advances'!$D:$D,\"Recovered from wages\")"
                   f"-SUMIFS({rng('U')},{rng('E')},$B$2)")
    tr = f"({rng('D')}=$D19)"
    f["pd_E19"] = f'=IF($D19="","",COUNTIFS({LA}$B:$B,$B$2,{LA}$E:$E,$D19,{LA}$A:$A,TODAY(),{LA}$N:$N,">0")+{wk_present_today(P, tr)})'
    f["pd_F19"] = (f'=IF($D19="","",SUMIFS({LA}$N:$N,{LA}$B:$B,$B$2,{LA}$E:$E,$D19,{LA}$A:$A,">="&$H$2,{LA}$A:$A,"<="&EOMONTH($H$2,0))'
                   f'+{wk_mandays(P, mask_month(PMS, PME) + "*" + tr)})')
    f["pd_G19"] = (f'=IF($D19="","",SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2,{LA}$E:$E,$D19,{LA}$A:$A,">="&$H$2,{LA}$A:$A,"<="&EOMONTH($H$2,0))'
                   f'+{wk_cost(P, mask_month(PMS, PME) + "*" + tr)})')
    f["pd_C42"] = ("=IF($A42=\"\",\"\",SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$B$2,'Supplier Invoices'!$H:$H,'Cost Codes'!$A2,'Supplier Invoices'!$M:$M,\"<>Draft\")"
                   "+SUMIFS('Labour Attendance'!$O:$O,'Labour Attendance'!$B:$B,$B$2,'Labour Attendance'!$K:$K,'Cost Codes'!$A2)"
                   "+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$B$2,'Site Expenses'!$C:$C,'Cost Codes'!$A2)"
                   f"+IF('Cost Codes'!$A2=Settings!$B$6,{wk_cost(P, MASK_ALL)},0))")
    # Wage Sheet row 6: add the weekly register for the worker, month and project filter
    W = lambda col: f'SUMIFS({rng(col)},{rng("B")},$A6,{rng("E")},IF($B$3="","*",$B$3),{rng("A")},">="&$B$2,{rng("A")},"<="&EOMONTH($B$2,0))'
    att = lambda st: (f"COUNTIFS({LA}$C:$C,$A6,{LA}$B:$B,IF($B$3=\"\",\"*\",$B$3),{LA}$A:$A,\">=\"&$B$2,{LA}$A:$A,\"<=\"&EOMONTH($B$2,0),{LA}$F:$F,\"{st}\")")
    sm = lambda col: (f"SUMIFS({LA}${col}:${col},{LA}$C:$C,$A6,{LA}$B:$B,IF($B$3=\"\",\"*\",$B$3),{LA}$A:$A,\">=\"&$B$2,{LA}$A:$A,\"<=\"&EOMONTH($B$2,0))")
    adv = lambda typ: (f"SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$B:$B,$A6,'Labour Advances'!$D:$D,\"{typ}\",'Labour Advances'!$A:$A,\">=\"&$B$2,'Labour Advances'!$A:$A,\"<=\"&EOMONTH($B$2,0))")
    f["wage_row6"] = [f'=IF($A6="","",{att("Present")}+{W("O")})', f'=IF($A6="","",{att("Half day")}+{W("P")})',
                      f'=IF($A6="","",{att("Absent")}+{W("Q")})', f'=IF($A6="","",{att("Leave")}+{W("R")})',
                      f'=IF($A6="","",{sm("N")}+{W("S")})', f'=IF($A6="","",{sm("I")}+{W("N")})',
                      f'=IF($A6="","",{sm("O")}+{W("T")})', f'=IF($A6="","",{adv("Advance given")})',
                      f'=IF($A6="","",{adv("Recovered from wages")}+{W("U")})']
    return f


if __name__ == "__main__":
    import sys
    if "integration" in sys.argv:
        f = integration()
        json.dump(f, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_requests", "12_integration.json"), "w"), indent=1)
        for k, v in f.items():
            print(k, len(v) if isinstance(v, str) else [len(x) for x in v])

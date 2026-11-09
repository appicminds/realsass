"""Switch worker / client / supplier dropdowns to names; the ID column next to each becomes automatic."""
import json, os
import gsheets_build as G
from simplify_live import IDS

N = 501
NAVY, GREY = "1F3864", "D9D9D9"
WA, LA, ADV, PRJ, PO, SI, WK = 2005, IDS["Labour Attendance"], IDS["Labour Advances"], IDS["Projects"], IDS["Purchase Orders"], IDS["Supplier Invoices"], IDS["Workers"]
LISTS = IDS["Lists"]


def hdr(sid, col, text, auto):
    f = {"textFormat": {"bold": True, "italic": auto, "foregroundColorStyle": {"rgbColor": G.rgb("000000" if auto else "FFFFFF")}},
         "backgroundColorStyle": {"rgbColor": G.rgb(GREY if auto else NAVY)}}
    return [G.rows_req(sid, 0, col, [[text]]),
            {"repeatCell": {"range": G.grid(sid, 0, 1, col, col + 1), "cell": {"userEnteredFormat": f},
                            "fields": "userEnteredFormat.textFormat.bold,userEnteredFormat.textFormat.italic,userEnteredFormat.textFormat.foregroundColorStyle,userEnteredFormat.backgroundColorStyle"}}]


def bg(sid, col, color):
    return {"repeatCell": {"range": G.grid(sid, 1, N, col, col + 1), "cell": {"userEnteredFormat": {"backgroundColorStyle": {"rgbColor": G.rgb(color)}}},
                           "fields": "userEnteredFormat.backgroundColorStyle"}}


def freeze_values(sid, col):
    return {"copyPaste": {"source": G.grid(sid, 1, N, col, col + 1), "destination": G.grid(sid, 1, N, col, col + 1), "pasteType": "PASTE_VALUES"}}


def formula_down(sid, col, f2):
    return [G.rows_req(sid, 1, col, [[f2]]),
            {"copyPaste": {"source": G.grid(sid, 1, 2, col, col + 1), "destination": G.grid(sid, 2, N, col, col + 1), "pasteType": "PASTE_FORMULA"}}]


def dv(sid, col, src):
    return G.dv_req(sid, col, src, 1, N)


def nodv(sid, col):
    return {"setDataValidation": {"range": G.grid(sid, 1, N, col, col + 1)}}


def protect(sid, col):
    return {"addProtectedRange": {"protectedRange": {"range": G.grid(sid, 1, N, col, col + 1), "description": "Auto formula column", "warningOnly": True}}}


def swap(sid, id_col, name_col, id_header, name_header, lookup_sheet, src, row_key="$A"):
    """Name column becomes the input (dropdown), ID column becomes a formula."""
    L = chr(ord("A") + name_col)
    f2 = f'=IF({row_key}2="","",IFERROR(INDEX({lookup_sheet}!$A:$A,MATCH({L}2,{lookup_sheet}!$B:$B,0)),""))'
    return ([freeze_values(sid, name_col)] + formula_down(sid, id_col, f2)
            + hdr(sid, id_col, id_header, True) + hdr(sid, name_col, name_header, False)
            + [bg(sid, id_col, "F2F2F2"), bg(sid, name_col, "FFFFFF"), nodv(sid, id_col), dv(sid, name_col, src), protect(sid, id_col)])


def build():
    R = []
    # helper lists of client and supplier names (dynamic)
    R.append(G.rows_req(LISTS, 0, 35, [["Clients (auto)", "Suppliers (auto)"],
                                       ['=IFERROR(FILTER(Parties!$B$2:$B$501,Parties!$C$2:$C$501="Client"),"")',
                                        '=IFERROR(FILTER(Parties!$B$2:$B$501,(Parties!$C$2:$C$501="Supplier")+(Parties!$C$2:$C$501="Subcontractor")),"")']]))
    # remove old warnings on the name columns (they become inputs); IDs from the earlier protection step
    for pid in (926875486, 80860453, 910331450, 357660670, 424695324):
        R.append({"deleteProtectedRange": {"protectedRangeId": pid}})
    R += swap(WA, 1, 2, "Worker ID (auto)", "Worker", "Workers", "=Workers!$B$2:$B$501")
    R.append(protect(WA, 3))  # Trade (auto)
    R += swap(LA, 2, 3, "Worker ID (auto)", "Worker", "Workers", "=Workers!$B$2:$B$501")
    R.append(protect(LA, 4))  # Trade (auto)
    R += swap(ADV, 1, 2, "Worker ID (auto)", "Worker", "Workers", "=Workers!$B$2:$B$501")
    R += swap(PRJ, 2, 3, "Client ID (auto)", "Client", "Parties", "=Lists!$AJ$2:$AJ$400")
    R += swap(PO, 4, 5, "Supplier ID (auto)", "Supplier", "Parties", "=Lists!$AK$2:$AK$400")
    # Supplier Invoices: column B becomes the supplier name; checks look up by name
    R += [G.rows_req(SI, 1, 1, [["Example Steel Traders"]]), dv(SI, 1, "=Lists!$AK$2:$AK$400")] + hdr(SI, 1, "Supplier", False)
    chk = ('=IF($A2="","",IF(COUNTIFS($B$2:$B$501,B2,$C$2:$C$501,C2)>1,"Duplicate invoice no.",IF(OR(G2="",H2=""),"Project and cost code required",'
           'IF(F2="","Non-PO: needs exception approval",IF(AND(IFERROR(INDEX(\'Purchase Orders\'!$G:$G,MATCH(F2,\'Purchase Orders\'!$A:$A,0)),"")="Goods",'
           'IFERROR(INDEX(\'Purchase Orders\'!$Q:$Q,MATCH(F2,\'Purchase Orders\'!$A:$A,0)),0)>IFERROR(INDEX(\'Purchase Orders\'!$P:$P,MATCH(F2,\'Purchase Orders\'!$A:$A,0)),0)),'
           '"Hold: invoiced above received",IF(IFERROR(INDEX(Parties!$I:$I,MATCH(B2,Parties!$B:$B,0)),"")<>"Yes","Supplier bank not verified",""))))))')
    R += formula_down(SI, 15, chk)
    # Workers: labour contractor by name; flag duplicate names
    R += [dv(WK, 7, "=Lists!$AK$2:$AK$400")] + hdr(WK, 7, "Labour contractor", False)
    R += formula_down(WK, 12, '=IF($A2="","",IF(COUNTIF($A$2:$A$501,A2)>1,"Duplicate worker ID",IF(COUNTIF($B$2:$B$501,B2)>1,"Two workers with this name",IF(N(E2)=0,"Daily rate missing",""))))')
    # Weekly Attendance check: worker name not found
    R += formula_down(WA, 24, '=IF($A2="","",IF(AND(C2<>"",B2=""),"Worker not found on Workers tab",IF(WEEKDAY(A2)<>5,"Week ending must be a Thursday",'
                              'IF(COUNTIFS($A$2:$A$501,A2,$B$2:$B$501,B2)>1,"Worker twice in this week",IF(AND(E2="",COUNTIF(G2:M2,"P")+COUNTIF(G2:M2,"H")>0),"Main project missing",'
                              'IF(COUNTA(G2:M2)=0,"No days marked",""))))))')
    # Worker Card: pick by name
    WC = 2007
    reg = lambda c: f"'Weekly Attendance'!${c}$2:${c}$501"
    arr = "{" + ",".join(reg(c) for c in ["A", "E", "G", "H", "I", "J", "K", "L", "M", "N", "S", "T", "U", "V", "W"]) + "}"
    R += [G.rows_req(WC, 1, 1, [["Usman But",
                                 '=IFERROR(INDEX(Workers!$A:$A,MATCH(B2,Workers!$B:$B,0))&"  ("&INDEX(Workers!$C:$C,MATCH(B2,Workers!$B:$B,0))&", "&TEXT(INDEX(Workers!$E:$E,MATCH(B2,Workers!$B:$B,0)),"#,##0")&" per day)","Pick a worker")']]),
          G.rows_req(WC, 1, 10, [["=IFERROR(INDEX(Workers!$L:$L,MATCH(B2,Workers!$B:$B,0)),0)"]]),
          G.rows_req(WC, 2, 10, [[f'=SUMIFS({reg("Q")},{reg("C")},$B$2,{reg("A")},">="&$B$3,{reg("A")},"<="&EOMONTH($B$3,0))']]),
          G.rows_req(WC, 5, 0, [[f'=IFERROR(SORT(FILTER({arr},{reg("C")}=$B$2,{reg("A")}>=$B$3,{reg("A")}<=EOMONTH($B$3,0)),1,TRUE),"No weeks for this worker in this month")']]),
          G.dv_req(WC, 1, "=Workers!$B$2:$B$501", 1, 2)]
    return R


if __name__ == "__main__":
    R = build()
    s = json.dumps(R)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_requests", "14_names.json"), "w").write(s)
    print(len(R), len(s))

"""Connect Weekly Attendance (through the hidden Labour Days helper) to Workers, dashboards and the Wage Sheet."""
import json, os
import gsheets_build as G

LD = "'Labour Days'!"
WA = "'Weekly Attendance'!"
LA = "'Labour Attendance'!"


def ld(c):
    return f"{LD}${c}$2:${c}$4000"


def wa(c):
    return f"{WA}${c}$2:${c}$501"


def build():
    MS, ME = "EOMONTH(TODAY(),-1)+1", "EOMONTH(TODAY(),0)"
    pm = lambda p, ms, me: f'{ld("B")},{p},{ld("A")},">="&{ms},{ld("A")},"<="&{me}'
    wm = lambda p, ms, me: f'{wa("E")},{p},{wa("A")},">="&{ms},{wa("A")},"<="&{me}'
    f = {}
    f["workers_L2"] = ("=IF($A2=\"\",\"\",SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$B:$B,A2,'Labour Advances'!$D:$D,\"Advance given\")"
                       "-SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$B:$B,A2,'Labour Advances'!$D:$D,\"Recovered from wages\")"
                       f"-SUMIFS({wa('U')},{wa('B')},A2))")
    p = "$A4"
    f["main_H4"] = ("=IF($A4=\"\",\"\",SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$A4,'Supplier Invoices'!$M:$M,\"<>Draft\")"
                    f"+SUMIFS({LA}$O:$O,{LA}$B:$B,$A4)+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$A4)"
                    f"+SUMIFS({ld('F')},{ld('B')},$A4)+SUMIFS({wa('Z')},{wa('E')},$A4))")
    f["main_W4"] = (f"=IF($A4=\"\",\"\",COUNTIFS({LA}$B:$B,$A4,{LA}$A:$A,TODAY(),{LA}$N:$N,\">0\")"
                    f"+COUNTIFS({ld('B')},$A4,{ld('A')},TODAY(),{ld('E')},\">0\"))")
    f["main_X4"] = (f"=IF($A4=\"\",\"\",SUMIFS({LA}$N:$N,{LA}$B:$B,$A4,{LA}$A:$A,\">=\"&{MS},{LA}$A:$A,\"<=\"&{ME})"
                    f"+SUMIFS({ld('E')},{pm(p, MS, ME)}))")
    f["main_Y4"] = (f"=IF($A4=\"\",\"\",SUMIFS({LA}$O:$O,{LA}$B:$B,$A4,{LA}$A:$A,\">=\"&{MS},{LA}$A:$A,\"<=\"&{ME})"
                    f"+SUMIFS({ld('F')},{pm(p, MS, ME)})+SUMIFS({wa('Z')},{wm(p, MS, ME)}))")
    P, PMS, PME = "$B$2", "$H$2", "EOMONTH($H$2,0)"
    f["pd_B9"] = ("=SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$B$2,'Supplier Invoices'!$M:$M,\"<>Draft\")"
                  f"+SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2)+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$B$2)"
                  f"+SUMIFS({ld('F')},{ld('B')},$B$2)+SUMIFS({wa('Z')},{wa('E')},$B$2)")
    f["pd_B19_25"] = [
        f"=COUNTIFS({LA}$B:$B,$B$2,{LA}$A:$A,TODAY(),{LA}$N:$N,\">0\")+COUNTIFS({ld('B')},$B$2,{ld('A')},TODAY(),{ld('E')},\">0\")",
        f"=COUNTIFS({LA}$B:$B,$B$2,{LA}$A:$A,TODAY(),{LA}$F:$F,\"Absent\")+COUNTIFS({ld('B')},$B$2,{ld('A')},TODAY(),{ld('G')},\"A\")",
        f"=SUMIFS({LA}$N:$N,{LA}$B:$B,$B$2,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+SUMIFS({ld('E')},{pm(P, PMS, PME)})",
        f"=SUMIFS({LA}$I:$I,{LA}$B:$B,$B$2,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+SUMIFS({wa('N')},{wm(P, PMS, PME)})",
        f"=SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+SUMIFS({ld('F')},{pm(P, PMS, PME)})+SUMIFS({wa('Z')},{wm(P, PMS, PME)})",
        f"=SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2)+SUMIFS({ld('F')},{ld('B')},$B$2)+SUMIFS({wa('Z')},{wa('E')},$B$2)",
        ("=SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$F:$F,$B$2,'Labour Advances'!$D:$D,\"Advance given\")"
         "-SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$F:$F,$B$2,'Labour Advances'!$D:$D,\"Recovered from wages\")"
         f"-SUMIFS({wa('U')},{wa('E')},$B$2)")]
    f["pd_E19_G19"] = [
        f"=IF($D19=\"\",\"\",COUNTIFS({LA}$B:$B,$B$2,{LA}$E:$E,$D19,{LA}$A:$A,TODAY(),{LA}$N:$N,\">0\")+COUNTIFS({ld('B')},$B$2,{ld('D')},$D19,{ld('A')},TODAY(),{ld('E')},\">0\"))",
        f"=IF($D19=\"\",\"\",SUMIFS({LA}$N:$N,{LA}$B:$B,$B$2,{LA}$E:$E,$D19,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+SUMIFS({ld('E')},{pm(P, PMS, PME)},{ld('D')},$D19))",
        f"=IF($D19=\"\",\"\",SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2,{LA}$E:$E,$D19,{LA}$A:$A,\">=\"&$H$2,{LA}$A:$A,\"<=\"&EOMONTH($H$2,0))+SUMIFS({ld('F')},{pm(P, PMS, PME)},{ld('D')},$D19)+SUMIFS({wa('Z')},{wm(P, PMS, PME)},{wa('D')},$D19))"]
    f["pd_C42"] = ("=IF($A42=\"\",\"\",SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$B$2,'Supplier Invoices'!$H:$H,'Cost Codes'!$A2,'Supplier Invoices'!$M:$M,\"<>Draft\")"
                   f"+SUMIFS({LA}$O:$O,{LA}$B:$B,$B$2,{LA}$K:$K,'Cost Codes'!$A2)"
                   "+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$B$2,'Site Expenses'!$C:$C,'Cost Codes'!$A2)"
                   f"+IF('Cost Codes'!$A2=Settings!$B$6,SUMIFS({ld('F')},{ld('B')},$B$2)+SUMIFS({wa('Z')},{wa('E')},$B$2),0))")
    # Wage Sheet row 6 (columns E..M). Day counts and wages from both attendance tabs.
    prj = 'IF($B$3="","*",$B$3)'
    dl = lambda extra: f'COUNTIFS({ld("C")},$A6,{ld("B")},{prj},{ld("A")},">="&$B$2,{ld("A")},"<="&EOMONTH($B$2,0),{extra})'
    ds = lambda col: f'SUMIFS({ld(col)},{ld("C")},$A6,{ld("B")},{prj},{ld("A")},">="&$B$2,{ld("A")},"<="&EOMONTH($B$2,0))'
    ws = lambda col: f'SUMIFS({wa(col)},{wa("B")},$A6,{wa("E")},{prj},{wa("A")},">="&$B$2,{wa("A")},"<="&EOMONTH($B$2,0))'
    att = lambda st: f'COUNTIFS({LA}$C:$C,$A6,{LA}$B:$B,{prj},{LA}$A:$A,">="&$B$2,{LA}$A:$A,"<="&EOMONTH($B$2,0),{LA}$F:$F,"{st}")'
    sm = lambda col: f'SUMIFS({LA}${col}:${col},{LA}$C:$C,$A6,{LA}$B:$B,{prj},{LA}$A:$A,">="&$B$2,{LA}$A:$A,"<="&EOMONTH($B$2,0))'
    adv = lambda typ: (f"SUMIFS('Labour Advances'!$E:$E,'Labour Advances'!$B:$B,$A6,'Labour Advances'!$D:$D,\"{typ}\","
                       "'Labour Advances'!$A:$A,\">=\"&$B$2,'Labour Advances'!$A:$A,\"<=\"&EOMONTH($B$2,0))")
    f["wage_E6_M6"] = [
        f'=IF($A6="","",{att("Present")}+{dl(ld("E") + ",1")})',
        f'=IF($A6="","",{att("Half day")}+{dl(ld("E") + ",0.5")})',
        f'=IF($A6="","",{att("Absent")}+{dl(ld("G") + ",\"A\"")})',
        f'=IF($A6="","",{att("Leave")}+{dl(ld("G") + ",\"L\"")})',
        f'=IF($A6="","",{sm("N")}+{ds("E")})',
        f'=IF($A6="","",{sm("I")}+{ws("N")})',
        f'=IF($A6="","",{sm("O")}+{ds("F")}+{ws("Z")})',
        f'=IF($A6="","",{adv("Advance given")})',
        f'=IF($A6="","",{adv("Recovered from wages")}+{ws("U")})']

    def cell(sid, r, c, vals):
        return G.rows_req(sid, r, c, [vals])

    def cp(sid, r, c0, c1, r1):
        return {"copyPaste": {"source": G.grid(sid, r, r + 1, c0, c1), "destination": G.grid(sid, r + 1, r1, c0, c1), "pasteType": "PASTE_FORMULA"}}
    R = [cell(1022380620, 1, 11, [f["workers_L2"]]), cp(1022380620, 1, 11, 12, 501),
         cell(2002, 3, 7, [f["main_H4"]]), cell(2002, 3, 22, [f["main_W4"], f["main_X4"], f["main_Y4"]]),
         cp(2002, 3, 7, 8, 103), cp(2002, 3, 22, 25, 103),
         cell(2003, 8, 1, [f["pd_B9"]]),
         G.rows_req(2003, 18, 1, [[x] for x in f["pd_B19_25"]]),
         cell(2003, 18, 4, f["pd_E19_G19"]), cp(2003, 18, 4, 7, 38),
         cell(2003, 41, 2, [f["pd_C42"]]), cp(2003, 41, 2, 3, 81),
         cell(2004, 5, 4, f["wage_E6_M6"]), cp(2004, 5, 4, 13, 505)]
    return R


if __name__ == "__main__":
    R = build()
    s = json.dumps(R)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_requests", "13_integration.json"), "w").write(s)
    print(len(s))

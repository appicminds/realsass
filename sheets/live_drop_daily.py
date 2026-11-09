"""The daily Labour Attendance tab was deleted: rebuild dashboard labour formulas from Weekly Attendance only."""
import json, os
import gsheets_build as G

LD = lambda c: f"'Labour Days'!${c}$2:${c}$4000"
WA = lambda c: f"'Weekly Attendance'!${c}$2:${c}$501"
OT = "AB"  # OT pay column after inserting Paid / Balance
MS, ME = "EOMONTH(TODAY(),-1)+1", "EOMONTH(TODAY(),0)"
pm = lambda p, ms, me: f'{LD("B")},{p},{LD("A")},">="&{ms},{LD("A")},"<="&{me}'
wm = lambda p, ms, me: f'{WA("E")},{p},{WA("A")},">="&{ms},{WA("A")},"<="&{me}'


def cell(sid, r, c, vals):
    return G.rows_req(sid, r, c, [vals])


def cp(sid, r, c0, c1, r1):
    return {"copyPaste": {"source": G.grid(sid, r, r + 1, c0, c1), "destination": G.grid(sid, r + 1, r1, c0, c1), "pasteType": "PASTE_FORMULA"}}


p = "$A4"
main = [
    ("=IF($A4=\"\",\"\",SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$A4,'Supplier Invoices'!$M:$M,\"<>Draft\")"
     f"+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$A4)+SUMIFS({LD('F')},{LD('B')},$A4)+SUMIFS({WA(OT)},{WA('E')},$A4))"),
]
mainWXY = [f"=IF($A4=\"\",\"\",COUNTIFS({LD('B')},$A4,{LD('A')},TODAY(),{LD('E')},\">0\"))",
           f"=IF($A4=\"\",\"\",SUMIFS({LD('E')},{pm(p, MS, ME)}))",
           f"=IF($A4=\"\",\"\",SUMIFS({LD('F')},{pm(p, MS, ME)})+SUMIFS({WA(OT)},{wm(p, MS, ME)}))"]
P, PMS, PME = "$B$2", "$H$2", "EOMONTH($H$2,0)"
pdB9 = ("=SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$B$2,'Supplier Invoices'!$M:$M,\"<>Draft\")"
        f"+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$B$2)+SUMIFS({LD('F')},{LD('B')},$B$2)+SUMIFS({WA(OT)},{WA('E')},$B$2)")
pdB = [f"=COUNTIFS({LD('B')},$B$2,{LD('A')},TODAY(),{LD('E')},\">0\")",
       f"=COUNTIFS({LD('B')},$B$2,{LD('A')},TODAY(),{LD('G')},\"A\")",
       f"=SUMIFS({LD('E')},{pm(P, PMS, PME)})",
       f"=SUMIFS({WA('N')},{wm(P, PMS, PME)})",
       f"=SUMIFS({LD('F')},{pm(P, PMS, PME)})+SUMIFS({WA(OT)},{wm(P, PMS, PME)})",
       f"=SUMIFS({LD('F')},{LD('B')},$B$2)+SUMIFS({WA(OT)},{WA('E')},$B$2)"]
pdEFG = [f"=IF($D19=\"\",\"\",COUNTIFS({LD('B')},$B$2,{LD('D')},$D19,{LD('A')},TODAY(),{LD('E')},\">0\"))",
         f"=IF($D19=\"\",\"\",SUMIFS({LD('E')},{pm(P, PMS, PME)},{LD('D')},$D19))",
         f"=IF($D19=\"\",\"\",SUMIFS({LD('F')},{pm(P, PMS, PME)},{LD('D')},$D19)+SUMIFS({WA(OT)},{wm(P, PMS, PME)},{WA('D')},$D19))"]
pdC42 = ("=IF($A42=\"\",\"\",SUMIFS('Supplier Invoices'!$J:$J,'Supplier Invoices'!$G:$G,$B$2,'Supplier Invoices'!$H:$H,'Cost Codes'!$A2,'Supplier Invoices'!$M:$M,\"<>Draft\")"
         "+SUMIFS('Site Expenses'!$F:$F,'Site Expenses'!$B:$B,$B$2,'Site Expenses'!$C:$C,'Cost Codes'!$A2)"
         f"+IF('Cost Codes'!$A2=Settings!$B$6,SUMIFS({LD('F')},{LD('B')},$B$2)+SUMIFS({WA(OT)},{WA('E')},$B$2),0))")
R = [cell(2002, 3, 7, main), cell(2002, 3, 22, mainWXY), cp(2002, 3, 7, 8, 103), cp(2002, 3, 22, 25, 103),
     cell(2003, 8, 1, [pdB9]), G.rows_req(2003, 18, 1, [[x] for x in pdB]),
     cell(2003, 18, 4, pdEFG), cp(2003, 18, 4, 7, 38),
     cell(2003, 41, 2, [pdC42]), cp(2003, 41, 2, 3, 81),
     cell(2003, 13, 6, ["Weekly attendance rows with checks", f"=COUNTIFS({WA('E')},$B$2,{WA('AA')},\"?*\")"]),
     {"updateCells": {"range": G.grid(IDS_LISTS := 219353797, 0, 6, 38, 39), "fields": "userEnteredValue"}}]
if __name__ == "__main__":
    s = json.dumps(R)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_requests", "16_drop_daily.json"), "w").write(s)
    print(s)

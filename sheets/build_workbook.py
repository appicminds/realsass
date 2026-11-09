"""Build the Construction ERP Google Sheets workbook (as .xlsx for import into Google Sheets).

Implements the R1 core of Construction_AI_ERP_Focused_Scope_PRD_v4.docx as a spreadsheet:
master data, BOQ, measurements -> RA bills -> receipts, change events, procurement
(requisition -> PO -> receipt -> supplier invoice), labour attendance, site expenses,
site records (diary, RFI, submittals, documents, inspections, safety, lookahead), CRM leads,
and a project dashboard using the PRD metric definitions (A, C, U, ETC, EAC, margin, variance).

Run:  python3 sheets/build_workbook.py
"""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
import datetime as dt
import os

ROWS = 500          # pre-filled formula rows on each register
PROJ_ROWS = 100     # project rows on the dashboard
FONT = "Arial"

MONEY = '#,##0;[Red](#,##0);"-"'
QTY = '#,##0.00;[Red](#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
DATE = "yyyy-mm-dd"
INT = '#,##0;(#,##0);"-"'

NAVY = "1F3864"
TEAL = "0F5E5E"
GREY_HDR = "D9D9D9"
AUTO_BG = "F2F2F2"
EX_FONT = Font(name=FONT, italic=True, color="7F7F7F")

D = dt.date

# ---------------------------------------------------------------------------
# Dropdown lists (Lists tab). Users can extend any list by typing below it.
# ---------------------------------------------------------------------------
LISTS = {
    "Project status": ["Planning", "Active", "On hold", "Closeout", "Closed"],
    "BOQ status": ["Draft", "Submitted", "Approved", "Superseded"],
    "Unit": ["m", "m2", "m3", "rft", "sft", "cft", "kg", "ton", "bag", "nos", "lot", "LS", "day", "hour"],
    "Measurement status": ["Draft", "Submitted", "Verified", "Returned", "Superseded"],
    "Bill status": ["Draft", "Submitted", "Partly certified", "Certified", "Rejected", "Disputed", "Corrected"],
    "Change source": ["Verbal instruction", "Written instruction", "RFI response", "Drawing revision",
                      "Site condition", "Client request"],
    "Commercial status": ["Identified", "Under assessment", "Notice prepared", "Submitted", "Partly approved",
                          "Approved", "Rejected", "Disputed", "Closed"],
    "Execution status": ["Not started", "Authorized to proceed", "In progress", "Completed", "Stopped"],
    "Requisition status": ["Draft", "Submitted", "Returned", "Approved", "Rejected", "Cancelled"],
    "PO type": ["Goods", "Services", "Subcontract", "Rental", "Advance"],
    "PO status": ["Draft", "Approved", "Partly received", "Received", "Closed", "Cancelled"],
    "Invoice status": ["Draft", "On hold", "Approved", "Posted", "Paid"],
    "Expense type": ["Petty cash", "Site expense", "Equipment rental", "Fuel", "Transport", "Overhead"],
    "Shift": ["Day", "Night"],
    "Report status": ["Draft", "Submitted", "Accepted", "Returned"],
    "RFI status": ["Open", "Awaiting response", "Answered", "Closed"],
    "Submittal type": ["Material sample", "Shop drawing", "Product data", "Method statement"],
    "Submittal status": ["Draft", "Submitted", "Under review", "Returned for revision", "Accepted",
                         "Accepted with conditions", "Rejected", "Superseded", "Withdrawn"],
    "Document status": ["Work in progress", "Shared for review", "Published", "Archived"],
    "Discipline": ["Architectural", "Structural", "MEP", "Civil", "Landscape"],
    "Quality type": ["Inspection", "Nonconformance", "Punch item", "Handover item"],
    "Quality status": ["Draft", "Requested", "Scheduled", "Inspected", "Accepted", "Failed", "Closed"],
    "Severity": ["Low", "Medium", "High", "Critical"],
    "Safety type": ["Hazard", "Near miss", "Incident", "Toolbox talk"],
    "Yes/No": ["Yes", "No"],
    "Party type": ["Client", "Supplier", "Subcontractor", "Consultant"],
    "Cost category": ["Material", "Labour", "Subcontract", "Equipment", "Overhead"],
    "Lead status": ["New", "Contacted", "Quoted", "Won", "Lost"],
    "Lead source": ["Referral", "Website", "Phone", "Walk-in", "Tender", "Social media"],
    "Payment mode": ["Bank transfer", "Cheque", "Cash"],
    "Trade": ["Mason", "Labourer / helper", "Carpenter", "Steel fixer", "Electrician", "Plumber", "Painter",
              "Tile fixer", "Welder", "Machine operator", "Driver", "Foreman", "Supervisor", "Engineer",
              "Storekeeper", "Watchman"],
    "Worker category": ["Daily wage", "Monthly staff", "Contractor labour"],
    "Attendance status": ["Present", "Half day", "Absent", "Leave"],
    "Advance type": ["Advance given", "Recovered from wages"],
}
LIST_COL = {name: get_column_letter(i + 1) for i, name in enumerate(LISTS)}


def lst(name):
    c = LIST_COL[name]
    return f"=Lists!${c}$2:${c}$60"


def ref(sheet, col_from=2, col_letter="A", n=ROWS + 1):
    return f"='{sheet}'!${col_letter}${col_from}:${col_letter}${n}"


PROJECTS = ref("Projects")
PARTIES = ref("Parties")
COSTCODES = ref("Cost Codes")
WORKERS = ref("Workers")
POLINES = ref("Purchase Orders")
BILLS = ref("RA Bills")
CHANGES = ref("Change Events")

# ---------------------------------------------------------------------------
# Sheet specs. Each column: (key, header, width, kind, extra)
#   kind "in"  = user input; extra may hold "dv" (validation) and "fmt"
#   kind "auto" = formula; extra["f"] = lambda r, c -> formula text
# c(key) returns this sheet's column letter, X(sheet, key) returns "'Sheet'!$L:$L"
# ---------------------------------------------------------------------------
SPECS = {}
LETTERS = {}


def X(sheet, key):
    L = LETTERS[sheet][key]
    return f"'{sheet}'!${L}:${L}"


def col(key, header, width=14, kind="in", **extra):
    return dict(key=key, header=header, width=width, kind=kind, **extra)


def lookup(sheet, key_col, val_col, lookup_cell, default='""'):
    return f"IFERROR(INDEX({X(sheet, val_col)},MATCH({lookup_cell},{X(sheet, key_col)},0)),{default})"


SPECS["Projects"] = dict(
    tab_color=NAVY,
    purpose="PROJECT-01 project master and contract configuration (BOQ-03, BILL-01).",
    cols=[
        col("id", "Project ID", 12),
        col("name", "Project name", 30),
        col("client", "Client (party ID)", 16, dv=PARTIES),
        col("client_name", "Client name", 26, "auto",
            f=lambda r, c: f'=IF(${c("id")}{r}="","",{lookup("Parties","id","name",c("client")+str(r))})'),
        col("location", "Location", 18),
        col("pm", "Project manager", 18),
        col("qs", "QS / measurement verifier", 20),
        col("supervisor", "Site supervisor", 18),
        col("start", "Start date", 12, fmt=DATE),
        col("end", "Planned end date", 14, fmt=DATE),
        col("status", "Status", 12, dv=lst("Project status")),
        col("contract", "Signed contract value (PKR)", 18, fmt=MONEY),
        col("ret_pct", "Retention %", 11, fmt=PCT),
        col("ret_cap", "Retention cap (PKR, blank = no cap)", 18, fmt=MONEY),
        col("advance", "Mobilization advance received (PKR)", 18, fmt=MONEY),
        col("adv_pct", "Advance recovery % per bill", 14, fmt=PCT),
        col("terms", "Payment terms (days)", 12, fmt=INT),
        col("u", "Remaining uncommitted cost U (PKR, PM/QS estimate)", 22, fmt=MONEY),
        col("u_date", "U estimate date", 13, fmt=DATE),
        col("notes", "Notes", 30),
    ],
    example=["PRJ-001", "Example residential block", "CL-001", None, "Lahore", "A. Khan", "S. Ahmed",
             "R. Ali", D(2026, 11, 1), D(2027, 10, 31), "Active", 12000000, 0.05, 600000, 1200000, 0.10,
             30, 500000, D(2026, 11, 30), "Example row, delete when you start"],
)

SPECS["Parties"] = dict(
    tab_color=NAVY,
    purpose="Clients, suppliers, subcontractors and consultants. Bank details stay in the accounting system.",
    cols=[
        col("id", "Party ID", 12),
        col("name", "Name", 28),
        col("type", "Type", 14, dv=lst("Party type")),
        col("contact", "Contact person", 18),
        col("phone", "Phone", 15, fmt="@"),
        col("email", "Email", 24),
        col("city", "City", 14),
        col("ntn", "NTN / tax no.", 14, fmt="@"),
        col("bank_ok", "Bank details independently verified", 16, dv=lst("Yes/No")),
        col("verified_by", "Verified by", 14),
        col("notes", "Notes", 30),
    ],
    example=[["CL-001", "Example Client Pvt Ltd", "Client", "M. Raza", "0300-0000000", None, "Lahore", None,
              "Yes", "Finance", "Example row"],
             ["SUP-001", "Example Steel Traders", "Supplier", "Z. Iqbal", "0321-0000000", None, "Lahore", None,
              "Yes", "Finance", "Example row"]],
)

SPECS["Cost Codes"] = dict(
    tab_color=NAVY,
    purpose="Cost codes used on budgets, POs, invoices, labour and expenses (FIN-02). Edit freely.",
    cols=[
        col("id", "Cost code", 14),
        col("desc", "Description", 30),
        col("cat", "Category", 14, dv=lst("Cost category")),
    ],
    example=[["01-CON", "Cement and concrete", "Material"], ["02-STL", "Reinforcement steel", "Material"],
             ["03-MAS", "Masonry and blocks", "Material"], ["04-FIN", "Finishes", "Material"],
             ["05-MEP", "MEP works", "Subcontract"], ["06-LAB", "Direct labour", "Labour"],
             ["07-SUB", "Civil subcontract", "Subcontract"], ["08-EQP", "Equipment and rental", "Equipment"],
             ["09-SITE", "Site overheads", "Overhead"], ["10-PREL", "Preliminaries", "Overhead"]],
)

SPECS["Workers"] = dict(
    tab_color=NAVY,
    purpose="LABOUR-01: masons, labourers and other workers. Keep CNIC and bank details in the payroll system.",
    cols=[
        col("id", "Worker ID", 11),
        col("name", "Name", 22),
        col("trade", "Trade", 16, dv=lst("Trade")),
        col("category", "Category", 15, dv=lst("Worker category")),
        col("rate", "Daily rate (PKR)", 13, fmt=MONEY),
        col("rate_from", "Rate effective from", 13, fmt=DATE),
        col("project", "Usual project", 12, dv=PROJECTS),
        col("contractor", "Labour contractor (party ID)", 16, dv=PARTIES),
        col("phone", "Phone", 15, fmt="@"),
        col("joined", "Joined on", 12, fmt=DATE),
        col("active", "Active", 9, dv=lst("Yes/No")),
        col("adv_bal", "Advance balance (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS({X("Labour Advances","amount")},{X("Labour Advances","worker")},{c("id")}{r},{X("Labour Advances","type")},"Advance given")-SUMIFS({X("Labour Advances","amount")},{X("Labour Advances","worker")},{c("id")}{r},{X("Labour Advances","type")},"Recovered from wages"))'),
        col("check", "Check", 20, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(COUNTIF(${c("id")}$2:${c("id")}${ROWS+1},{c("id")}{r})>1,"Duplicate worker ID",IF(N({c("rate")}{r})=0,"Daily rate missing","")))'),
        col("notes", "Notes", 24),
    ],
    example=[["W-001", "Example mason", "Mason", "Daily wage", 2500, D(2026, 11, 1), "PRJ-001", None, None,
              D(2026, 11, 1), "Yes", None, None, "Example row"],
             ["W-002", "Example helper", "Labourer / helper", "Daily wage", 1500, D(2026, 11, 1), "PRJ-001", None,
              None, D(2026, 11, 1), "Yes", None, None, "Example row"]],
)

SPECS["Labour Advances"] = dict(
    tab_color="7F6000",
    purpose="LABOUR-03/05: cash advances to workers and their recovery from wages.",
    cols=[
        col("date", "Date", 11, fmt=DATE),
        col("worker", "Worker ID", 10, dv=WORKERS),
        col("name", "Worker name", 18, "auto",
            f=lambda r, c: f'=IF(${c("date")}{r}="","",{lookup("Workers","id","name",c("worker")+str(r))})'),
        col("type", "Type", 18, dv=lst("Advance type")),
        col("amount", "Amount (PKR)", 12, fmt=MONEY),
        col("project", "Project", 11, dv=PROJECTS),
        col("by", "Paid / approved by", 14),
        col("notes", "Notes", 26),
    ],
    example=[D(2026, 11, 20), "W-001", None, "Advance given", 5000, "PRJ-001", "A. Khan", "Example row"],
)

SPECS["Budget"] = dict(
    tab_color=TEAL,
    purpose="Section 4.2: original approved budget and approved changes/transfers by project and cost code.",
    cols=[
        col("project", "Project", 12, dv=PROJECTS),
        col("code", "Cost code", 12, dv=COSTCODES),
        col("desc", "Cost code description", 26, "auto",
            f=lambda r, c: f'=IF(${c("project")}{r}="","",{lookup("Cost Codes","id","desc",c("code")+str(r))})'),
        col("original", "Original approved budget (PKR)", 18, fmt=MONEY),
        col("changes", "Approved changes and transfers (PKR)", 18, fmt=MONEY),
        col("current", "Current approved budget (PKR)", 18, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("project")}{r}="","",N({c("original")}{r})+N({c("changes")}{r}))'),
        col("approved_by", "Approved by", 14),
        col("notes", "Reason / notes", 30),
    ],
    example=[["PRJ-001", "02-STL", None, 2500000, 0, None, "Owner", "Example row"],
             ["PRJ-001", "06-LAB", None, 300000, 0, None, "Owner", "Example row"],
             ["PRJ-001", "09-SITE", None, 300000, 0, None, "Owner", "Example row"]],
)

SPECS["BOQ"] = dict(
    tab_color=TEAL,
    purpose="BOQ-01/02: contract BOQ lines with rate build-up. Add approved variations as new lines (version VO-xx).",
    cols=[
        col("project", "Project", 12, dv=PROJECTS),
        col("version", "BOQ version", 10),
        col("line", "BOQ line code", 12, fmt="@"),
        col("desc", "Description", 34),
        col("unit", "Unit", 8, dv=lst("Unit")),
        col("qty", "Contract qty", 12, fmt=QTY),
        col("mat", "Material rate", 12, fmt=MONEY),
        col("lab", "Labour rate", 12, fmt=MONEY),
        col("sub", "Subcontract rate", 12, fmt=MONEY),
        col("oh", "Overhead and profit rate", 12, fmt=MONEY),
        col("rate", "Unit rate (PKR)", 13, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("project")}{r}="","",N({c("mat")}{r})+N({c("lab")}{r})+N({c("sub")}{r})+N({c("oh")}{r}))'),
        col("amount", "Amount (PKR)", 15, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("project")}{r}="","",N({c("qty")}{r})*N({c("rate")}{r}))'),
        col("code", "Cost code", 11, dv=COSTCODES),
        col("status", "Status", 11, dv=lst("BOQ status")),
        col("notes", "Notes", 26),
        col("key", "Lookup key", 14, "auto",
            f=lambda r, c: f'=IF(${c("project")}{r}="","",IF({c("status")}{r}="Approved",{c("project")}{r}&"|"&{c("line")}{r},""))'),
    ],
    example=["PRJ-001", "v1", "1.01", "RCC slab concrete 1:2:4 incl. formwork", "m3", 200, 9000, 2500, 0, 1000,
             None, None, "01-CON", "Approved", "Example row"],
)

SPECS["Measurements"] = dict(
    tab_color=TEAL,
    purpose="PROJECT-04 / BILL-02/03: cumulative measured and certified quantities. Only Verified rows feed bills.",
    cols=[
        col("id", "Measurement ID", 13),
        col("date", "Date", 11, fmt=DATE),
        col("project", "Project", 11, dv=PROJECTS),
        col("line", "BOQ line code", 11, fmt="@"),
        col("desc", "BOQ description", 28, "auto",
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IFERROR(INDEX({X("BOQ","desc")},MATCH({c("project")}{r}&"|"&{c("line")}{r},{X("BOQ","key")},0)),"Approved BOQ line not found"))'),
        col("location", "Location", 16),
        col("bill", "RA bill no.", 10, dv=BILLS),
        col("submitted", "Submitted cumulative qty", 13, fmt=QTY),
        col("certified", "Certified cumulative qty", 13, fmt=QTY),
        col("status", "Status", 11, dv=lst("Measurement status")),
        col("verifier", "Verified by", 13),
        col("evidence", "Evidence link", 20),
        col("prev", "Previously certified qty", 13, "auto", fmt=QTY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS(${c("inc")}$1:{c("inc")}{r-1},${c("project")}$1:{c("project")}{r-1},{c("project")}{r},${c("line")}$1:{c("line")}{r-1},{c("line")}{r}))'),
        col("inc", "Increment qty this row", 13, "auto", fmt=QTY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF({c("status")}{r}="Verified",N({c("certified")}{r})-{c("prev")}{r},0))'),
        col("rate", "Rate (PKR)", 12, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS({X("BOQ","rate")},{X("BOQ","project")},{c("project")}{r},{X("BOQ","line")},{c("line")}{r},{X("BOQ","status")},"Approved"))'),
        col("value", "Increment value (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",{c("inc")}{r}*{c("rate")}{r})'),
        col("check", "Check", 24, "auto", flag=True,
            f=lambda r, c: (f'=IF(${c("id")}{r}="","",IF(N({c("certified")}{r})>SUMIFS({X("BOQ","qty")},{X("BOQ","project")},{c("project")}{r},{X("BOQ","line")},{c("line")}{r},{X("BOQ","status")},"Approved"),"Exceeds BOQ qty",'
                            f'IF(N({c("certified")}{r})>N({c("submitted")}{r}),"Certified above submitted",IF({c("inc")}{r}<0,"Downward correction",""))))')),
    ],
    example=["M-001", D(2026, 11, 30), "PRJ-001", "1.01", None, "Block A level 1", "RA-01", 85, 80, "Verified",
             "S. Ahmed", None],
)

SPECS["RA Bills"] = dict(
    tab_color=TEAL,
    purpose="BILL-03/04: running (RA) bills built from verified measurement increments assigned to the bill.",
    cols=[
        col("id", "RA bill no.", 10),
        col("project", "Project", 11, dv=PROJECTS),
        col("period", "Period to", 11, fmt=DATE),
        col("sub_date", "Submitted date", 12, fmt=DATE),
        col("cert_date", "Certified date", 12, fmt=DATE),
        col("status", "Status", 13, dv=lst("Bill status")),
        col("gross", "Gross certified work (PKR)", 15, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS({X("Measurements","value")},{X("Measurements","bill")},{c("id")}{r}))'),
        col("ret_before", "Retention held before (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS(${c("ret")}$1:{c("ret")}{r-1},${c("project")}$1:{c("project")}{r-1},{c("project")}{r}))'),
        col("ret", "Retention (PKR)", 13, "auto", fmt=MONEY,
            f=lambda r, c: (f'=IF(${c("id")}{r}="","",IF({lookup("Projects","id","ret_cap",c("project")+str(r))}="",'
                            f'{c("gross")}{r}*{lookup("Projects","id","ret_pct",c("project")+str(r),"0")},'
                            f'MAX(0,MIN({c("gross")}{r}*{lookup("Projects","id","ret_pct",c("project")+str(r),"0")},'
                            f'{lookup("Projects","id","ret_cap",c("project")+str(r),"0")}-{c("ret_before")}{r}))))')),
        col("adv_before", "Advance recovered before (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS(${c("adv")}$1:{c("adv")}{r-1},${c("project")}$1:{c("project")}{r-1},{c("project")}{r}))'),
        col("adv", "Advance recovery (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: (f'=IF(${c("id")}{r}="","",MAX(0,MIN({c("gross")}{r}*{lookup("Projects","id","adv_pct",c("project")+str(r),"0")},'
                            f'{lookup("Projects","id","advance",c("project")+str(r),"0")}-{c("adv_before")}{r})))')),
        col("ded", "Other approved deductions (PKR)", 14, fmt=MONEY),
        col("net", "Net amount due (PKR)", 15, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",{c("gross")}{r}-{c("ret")}{r}-{c("adv")}{r}-N({c("ded")}{r}))'),
        col("due", "Due date", 11, "auto", fmt=DATE,
            f=lambda r, c: f'=IF(OR(${c("id")}{r}="",{c("cert_date")}{r}=""),"",{c("cert_date")}{r}+{lookup("Projects","id","terms",c("project")+str(r),"0")})'),
        col("received", "Received incl. tax withheld (PKR)", 15, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS({X("Receipts","amount")},{X("Receipts","bill")},{c("id")}{r})+SUMIFS({X("Receipts","wht")},{X("Receipts","bill")},{c("id")}{r}))'),
        col("outstanding", "Outstanding (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(OR({c("status")}{r}="Draft",{c("status")}{r}="Rejected"),0,{c("net")}{r}-{c("received")}{r}))'),
        col("overdue", "Days overdue", 9, "auto", fmt=INT,
            f=lambda r, c: f'=IF(OR(${c("id")}{r}="",{c("due")}{r}="",{c("outstanding")}{r}<=0),"",MAX(0,TODAY()-{c("due")}{r}))'),
        col("cert_days", "Days submitted to certified", 11, "auto", fmt=INT,
            f=lambda r, c: f'=IF(OR(${c("id")}{r}="",{c("sub_date")}{r}=""),"",IF({c("cert_date")}{r}="",TODAY(),{c("cert_date")}{r})-{c("sub_date")}{r})'),
        col("owner", "Follow-up owner", 13),
        col("next", "Next action", 24),
    ],
    example=["RA-01", "PRJ-001", D(2026, 11, 30), D(2026, 12, 2), D(2026, 12, 10), "Certified", None, None, None,
             None, None, 20000, None, None, None, None, None, None, "S. Ahmed", "Chase balance payment"],
)

SPECS["Receipts"] = dict(
    tab_color=TEAL,
    purpose="BILL-05: client payments allocated to RA bills. Split one payment across bills on separate rows.",
    cols=[
        col("id", "Receipt ID", 11),
        col("date", "Date", 11, fmt=DATE),
        col("bill", "RA bill no.", 10, dv=BILLS),
        col("project", "Project", 11, "auto",
            f=lambda r, c: f'=IF(${c("id")}{r}="","",{lookup("RA Bills","id","project",c("bill")+str(r))})'),
        col("amount", "Amount received (PKR)", 15, fmt=MONEY),
        col("wht", "Tax withheld by client (PKR)", 15, fmt=MONEY),
        col("mode", "Mode", 13, dv=lst("Payment mode")),
        col("reference", "Bank / cheque reference", 18, fmt="@"),
        col("notes", "Notes", 28),
    ],
    example=["RC-001", D(2026, 12, 20), "RA-01", None, 500000, 0, "Bank transfer", "TRX-0001", "Example row"],
)

SPECS["Change Events"] = dict(
    tab_color=TEAL,
    purpose="CHG-01..05: instructions and changes. Approved amounts raise contract value; pending amounts are exposure only.",
    cols=[
        col("id", "Change ID", 10),
        col("project", "Project", 11, dv=PROJECTS),
        col("source", "Source", 16, dv=lst("Change source")),
        col("instr_date", "Instruction date", 12, fmt=DATE),
        col("desc", "Description", 30),
        col("location", "Location", 14),
        col("owner", "Owner", 13),
        col("notice_due", "Notice due date (from contract)", 14, fmt=DATE),
        col("est_cost", "Estimated cost (PKR)", 14, fmt=MONEY),
        col("risk_cap", "At-risk spend cap approved (PKR)", 15, fmt=MONEY),
        col("claimed", "Amount claimed (PKR)", 14, fmt=MONEY),
        col("approved", "Amount approved by client (PKR)", 15, fmt=MONEY),
        col("comm", "Commercial status", 15, dv=lst("Commercial status")),
        col("exec", "Execution status", 15, dv=lst("Execution status")),
        col("pending", "Pending claim (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(OR({c("comm")}{r}="Approved",{c("comm")}{r}="Partly approved",{c("comm")}{r}="Rejected",{c("comm")}{r}="Closed"),0,N({c("claimed")}{r})-N({c("approved")}{r})))'),
        col("disputed", "Rejected or disputed (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(OR({c("comm")}{r}="Partly approved",{c("comm")}{r}="Rejected",{c("comm")}{r}="Disputed",{c("comm")}{r}="Approved"),N({c("claimed")}{r})-N({c("approved")}{r}),0))'),
        col("approved_var", "Approved variation in contract (PKR)", 15, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(OR({c("comm")}{r}="Approved",{c("comm")}{r}="Partly approved",{c("comm")}{r}="Closed"),N({c("approved")}{r}),0))'),
        col("evidence", "Evidence link", 18),
        col("check", "Check", 22, "auto", flag=True,
            f=lambda r, c: (f'=IF(${c("id")}{r}="","",IF(AND({c("notice_due")}{r}<>"",{c("notice_due")}{r}<TODAY(),OR({c("comm")}{r}="Identified",{c("comm")}{r}="Under assessment",{c("comm")}{r}="Notice prepared")),"Notice overdue",'
                            f'IF(AND({c("notice_due")}{r}="",{c("comm")}{r}<>"Closed"),"Notice date not set","")))')),
    ],
    example=["CE-001", "PRJ-001", "Verbal instruction", D(2026, 11, 15), "Additional parapet wall on roof",
             "Roof", "S. Ahmed", D(2026, 11, 29), 350000, 300000, 500000, 300000, "Partly approved", "In progress"],
)

SPECS["Requisitions"] = dict(
    tab_color="7F6000",
    purpose="PROC-01: site material and service requests.",
    cols=[
        col("id", "Requisition no.", 12),
        col("date", "Date", 11, fmt=DATE),
        col("project", "Project", 11, dv=PROJECTS),
        col("item", "Item", 24),
        col("unit", "Unit", 8, dv=lst("Unit")),
        col("qty", "Qty", 10, fmt=QTY),
        col("needed", "Needed by", 11, fmt=DATE),
        col("code", "Cost code", 11, dv=COSTCODES),
        col("by", "Requested by", 13),
        col("approver", "Approved by", 13),
        col("status", "Status", 11, dv=lst("Requisition status")),
        col("po", "PO no.", 10),
        col("check", "Check", 22, "auto", flag=True,
            f=lambda r, c: (f'=IF(${c("id")}{r}="","",IF(AND({c("by")}{r}<>"",{c("by")}{r}={c("approver")}{r}),"Self-approval not allowed",'
                            f'IF(COUNTIFS(${c("project")}$2:${c("project")}${ROWS+1},{c("project")}{r},${c("item")}$2:${c("item")}${ROWS+1},{c("item")}{r},${c("status")}$2:${c("status")}${ROWS+1},"<>Cancelled",${c("status")}$2:${c("status")}${ROWS+1},"<>Rejected",${c("po")}$2:${c("po")}${ROWS+1},"")>1,"Possible duplicate request","")))')),
    ],
    example=["RQ-001", D(2026, 11, 5), "PRJ-001", "Steel bar 12 mm", "ton", 10, D(2026, 11, 12), "02-STL",
             "R. Ali", "A. Khan", "Approved", "PO-001"],
)

SPECS["Purchase Orders"] = dict(
    tab_color="7F6000",
    purpose="PROC-03 / LABOUR-04: one row per PO line (goods, services, subcontract). Open commitment feeds C.",
    cols=[
        col("id", "PO line ID", 11),
        col("po", "PO no.", 10),
        col("date", "Date", 11, fmt=DATE),
        col("project", "Project", 11, dv=PROJECTS),
        col("supplier", "Supplier (party ID)", 13, dv=PARTIES),
        col("supplier_name", "Supplier name", 22, "auto",
            f=lambda r, c: f'=IF(${c("id")}{r}="","",{lookup("Parties","id","name",c("supplier")+str(r))})'),
        col("type", "Type", 11, dv=lst("PO type")),
        col("code", "Cost code", 11, dv=COSTCODES),
        col("item", "Item / scope", 24),
        col("unit", "Unit", 8, dv=lst("Unit")),
        col("qty", "Qty ordered", 11, fmt=QTY),
        col("rate", "Rate (PKR)", 12, fmt=MONEY),
        col("amount", "PO amount (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",N({c("qty")}{r})*N({c("rate")}{r}))'),
        col("status", "Status", 12, dv=lst("PO status")),
        col("approver", "Approved by", 13),
        col("received", "Qty accepted", 11, "auto", fmt=QTY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS({X("Goods Receipts","accepted")},{X("Goods Receipts","po_line")},{c("id")}{r}))'),
        col("inv_qty", "Qty invoiced", 11, "auto", fmt=QTY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS({X("Supplier Invoices","qty")},{X("Supplier Invoices","po_line")},{c("id")}{r},{X("Supplier Invoices","status")},"<>Draft"))'),
        col("invoiced", "Invoiced amount (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",SUMIFS({X("Supplier Invoices","amount")},{X("Supplier Invoices","po_line")},{c("id")}{r},{X("Supplier Invoices","status")},"<>Draft"))'),
        col("open", "Open commitment C (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(OR({c("status")}{r}="Draft",{c("status")}{r}="Cancelled",{c("status")}{r}="Closed"),0,MAX(0,{c("amount")}{r}-{c("invoiced")}{r})))'),
    ],
    example=["PO-001-1", "PO-001", D(2026, 11, 6), "PRJ-001", "SUP-001", None, "Goods", "02-STL", "Steel bar 12 mm",
             "ton", 10, 250000, None, "Approved", "A. Khan"],
)

SPECS["Goods Receipts"] = dict(
    tab_color="7F6000",
    purpose="PROC-04: accepted and rejected deliveries against PO lines.",
    cols=[
        col("id", "GRN no.", 10),
        col("date", "Date", 11, fmt=DATE),
        col("po_line", "PO line ID", 11, dv=POLINES),
        col("project", "Project", 11, "auto",
            f=lambda r, c: f'=IF(${c("id")}{r}="","",{lookup("Purchase Orders","id","project",c("po_line")+str(r))})'),
        col("item", "Item", 22, "auto",
            f=lambda r, c: f'=IF(${c("id")}{r}="","",{lookup("Purchase Orders","id","item",c("po_line")+str(r))})'),
        col("accepted", "Qty accepted", 11, fmt=QTY),
        col("rejected", "Qty rejected", 11, fmt=QTY),
        col("batch", "Batch / DC no.", 13, fmt="@"),
        col("by", "Received by", 13),
        col("note", "Discrepancy note / photo link", 28),
        col("check", "Check", 20, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(SUMIFS(${c("accepted")}$2:${c("accepted")}${ROWS+1},${c("po_line")}$2:${c("po_line")}${ROWS+1},{c("po_line")}{r})>{lookup("Purchase Orders","id","qty",c("po_line")+str(r),"0")},"Received above PO qty",""))'),
    ],
    example=["GRN-001", D(2026, 11, 10), "PO-001-1", None, None, 6, 0, "DC-5521", "R. Ali", None],
)

SPECS["Supplier Invoices"] = dict(
    tab_color="7F6000",
    purpose="PROC-06/07/09, FIN-02: supplier and subcontractor bills. Every line needs project and cost code.",
    cols=[
        col("id", "Entry ID", 10),
        col("supplier", "Supplier (party ID)", 13, dv=PARTIES),
        col("inv_no", "Supplier invoice no.", 14, fmt="@"),
        col("date", "Invoice date", 11, fmt=DATE),
        col("due", "Due date", 11, fmt=DATE),
        col("po_line", "PO line ID (blank = non-PO)", 13, dv=POLINES),
        col("project", "Project", 11, dv=PROJECTS),
        col("code", "Cost code", 11, dv=COSTCODES),
        col("qty", "Qty", 9, fmt=QTY),
        col("amount", "Amount excl. tax (PKR)", 14, fmt=MONEY),
        col("tax", "Tax (PKR)", 11, fmt=MONEY),
        col("total", "Total (PKR)", 13, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",N({c("amount")}{r})+N({c("tax")}{r}))'),
        col("status", "Status", 10, dv=lst("Invoice status")),
        col("paid", "Paid (PKR)", 13, fmt=MONEY),
        col("balance", "Balance payable (PKR)", 14, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF({c("status")}{r}="Draft",0,{c("total")}{r}-N({c("paid")}{r})))'),
        col("check", "Check", 26, "auto", flag=True,
            f=lambda r, c: (f'=IF(${c("id")}{r}="","",IF(COUNTIFS(${c("supplier")}$2:${c("supplier")}${ROWS+1},{c("supplier")}{r},${c("inv_no")}$2:${c("inv_no")}${ROWS+1},{c("inv_no")}{r})>1,"Duplicate invoice no.",'
                            f'IF(OR({c("project")}{r}="",{c("code")}{r}=""),"Project and cost code required",'
                            f'IF({c("po_line")}{r}="","Non-PO: needs exception approval",'
                            f'IF(AND({lookup("Purchase Orders","id","type",c("po_line")+str(r))}="Goods",{lookup("Purchase Orders","id","inv_qty",c("po_line")+str(r),"0")}>{lookup("Purchase Orders","id","received",c("po_line")+str(r),"0")}),"Hold: invoiced above received",'
                            f'IF({lookup("Parties","id","bank_ok",c("supplier")+str(r))}<>"Yes","Supplier bank not verified",""))))))')),
    ],
    example=["SI-001", "SUP-001", "INV-7781", D(2026, 11, 12), D(2026, 12, 12), "PO-001-1", "PRJ-001", "02-STL", 6,
             1500000, 0, None, "Approved", 0],
)

SPECS["Labour Attendance"] = dict(
    tab_color="7F6000",
    purpose="LABOUR-02: one row per worker per day. Blank hours on a Present row count as a full day.",
    cols=[
        col("date", "Date", 11, fmt=DATE),
        col("project", "Project", 11, dv=PROJECTS),
        col("worker", "Worker ID", 10, dv=WORKERS),
        col("name", "Worker name", 18, "auto",
            f=lambda r, c: f'=IF(${c("date")}{r}="","",{lookup("Workers","id","name",c("worker")+str(r))})'),
        col("trade", "Trade", 14, "auto",
            f=lambda r, c: f'=IF(${c("date")}{r}="","",{lookup("Workers","id","trade",c("worker")+str(r))})'),
        col("status", "Status", 10, dv=lst("Attendance status")),
        col("shift", "Shift", 8, dv=lst("Shift")),
        col("hours", "Hours worked (blank = full day)", 11, fmt=QTY),
        col("ot", "Overtime hours", 9, fmt=QTY),
        col("work", "Work / location", 20),
        col("code", "Cost code", 11, dv=COSTCODES),
        col("approver", "Marked by", 12),
        col("rate", "Daily rate (PKR)", 12, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("date")}{r}="","",{lookup("Workers","id","rate",c("worker")+str(r),"0")})'),
        col("days", "Days counted", 9, "auto", fmt=QTY,
            f=lambda r, c: f'=IF(${c("date")}{r}="","",IF({c("status")}{r}="Half day",0.5,IF({c("status")}{r}="Present",IF({c("hours")}{r}="",1,{c("hours")}{r}/Settings!$B$3),0)))'),
        col("cost", "Labour cost (PKR)", 13, "auto", fmt=MONEY,
            f=lambda r, c: f'=IF(${c("date")}{r}="","",{c("rate")}{r}*({c("days")}{r}+N({c("ot")}{r})/Settings!$B$3*Settings!$B$4))'),
        col("check", "Check", 22, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("date")}{r}="","",IF({c("status")}{r}="","Status missing",IF(COUNTIFS(${c("date")}$2:${c("date")}${ROWS+1},{c("date")}{r},${c("worker")}$2:${c("worker")}${ROWS+1},{c("worker")}{r},${c("shift")}$2:${c("shift")}${ROWS+1},{c("shift")}{r})>1,"Same worker twice in shift","")))'),
    ],
    example=[[D(2026, 11, 30), "PRJ-001", "W-001", None, None, "Present", "Day", None, 2, "Block A slab", "06-LAB", "R. Ali"],
             [D(2026, 11, 30), "PRJ-001", "W-002", None, None, "Half day", "Day", None, None, "Block A slab", "06-LAB", "R. Ali"]],
)

SPECS["Site Expenses"] = dict(
    tab_color="7F6000",
    purpose="FIN-04: petty cash and direct site expenses with project and cost code.",
    cols=[
        col("date", "Date", 11, fmt=DATE),
        col("project", "Project", 11, dv=PROJECTS),
        col("code", "Cost code", 11, dv=COSTCODES),
        col("type", "Type", 14, dv=lst("Expense type")),
        col("desc", "Description", 26),
        col("amount", "Amount (PKR)", 13, fmt=MONEY),
        col("paid_to", "Paid to", 16),
        col("receipt", "Receipt attached", 10, dv=lst("Yes/No")),
        col("approver", "Approved by", 13),
        col("settled", "Settled in accounts", 10, dv=lst("Yes/No")),
        col("check", "Check", 22, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("date")}{r}="","",IF({c("receipt")}{r}<>"Yes","Receipt missing",IF({c("settled")}{r}<>"Yes","Open advance","")))'),
    ],
    example=[D(2026, 11, 30), "PRJ-001", "09-SITE", "Petty cash", "Water tanker", 6000, "Local vendor", "Yes",
             "A. Khan", "No"],
)

SPECS["Daily Diary"] = dict(
    tab_color="38761D",
    purpose="PROJECT-03 / OPS-01: one row per work item per daily report. Diary quantities are observations, not certified.",
    cols=[
        col("date", "Date", 11, fmt=DATE),
        col("project", "Project", 11, dv=PROJECTS),
        col("location", "Site / location", 16),
        col("shift", "Shift", 8, dv=lst("Shift")),
        col("author", "Supervisor", 13),
        col("weather", "Weather", 10),
        col("work", "Work done", 28),
        col("line", "BOQ line code", 10, fmt="@"),
        col("qty", "Qty done", 10, fmt=QTY),
        col("unit", "Unit", 7, dv=lst("Unit")),
        col("labour", "Labour count", 9, fmt=INT),
        col("equipment", "Equipment on site", 16),
        col("materials", "Material notes", 20),
        col("blockers", "Blockers / issues", 22),
        col("photos", "Photo link", 18),
        col("status", "Status", 10, dv=lst("Report status")),
    ],
    example=[D(2026, 11, 30), "PRJ-001", "Block A level 1", "Day", "R. Ali", "Clear", "Slab casting bay 2", "1.01",
             40, "m3", 22, "Mixer, vibrator", "Cement 300 bags used", "None", None, "Submitted"],
)

SPECS["RFIs"] = dict(
    tab_color="38761D",
    purpose="RFI-01: requests for information. A scope-changing answer should create a Change Event.",
    cols=[
        col("id", "RFI no.", 9),
        col("project", "Project", 11, dv=PROJECTS),
        col("date", "Date raised", 11, fmt=DATE),
        col("question", "Question", 30),
        col("location", "Location", 14),
        col("drawing", "Drawing ref", 12),
        col("assigned", "Assigned to", 13),
        col("required", "Response required by", 12, fmt=DATE),
        col("response", "Response", 28),
        col("resp_date", "Response date", 11, fmt=DATE),
        col("status", "Status", 12, dv=lst("RFI status")),
        col("change", "Linked change ID", 11, dv=CHANGES),
        col("check", "Check", 14, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(AND({c("required")}{r}<>"",{c("required")}{r}<TODAY(),OR({c("status")}{r}="Open",{c("status")}{r}="Awaiting response")),"Overdue",""))'),
    ],
    example=["RFI-001", "PRJ-001", D(2026, 11, 14), "Confirm parapet height on roof", "Roof", "A-301 rev B",
             "Consultant", D(2026, 11, 21), "1.2 m as per revised section", D(2026, 11, 18), "Answered", "CE-001"],
)

SPECS["Submittals"] = dict(
    tab_color="38761D",
    purpose="SUB-01..03: material samples, shop drawings, product data and method statements.",
    cols=[
        col("id", "Submittal no.", 11),
        col("project", "Project", 11, dv=PROJECTS),
        col("type", "Type", 15, dv=lst("Submittal type")),
        col("spec", "Spec ref", 10),
        col("desc", "Description", 26),
        col("vendor", "Vendor / subcontractor", 18),
        col("rev", "Revision", 8),
        col("submitted", "Submitted date", 11, fmt=DATE),
        col("reviewer", "Reviewer", 13),
        col("due", "Review due", 11, fmt=DATE),
        col("on_site", "Required on site", 11, fmt=DATE),
        col("status", "Status", 16, dv=lst("Submittal status")),
        col("conditions", "Response / conditions", 24),
        col("check", "Check", 16, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(AND({c("due")}{r}<>"",{c("due")}{r}<TODAY(),OR({c("status")}{r}="Submitted",{c("status")}{r}="Under review")),"Review overdue",IF(OR({c("status")}{r}="Rejected",{c("status")}{r}="Superseded"),"Do not procure","")))'),
    ],
    example=["SUB-001", "PRJ-001", "Material sample", "03 30 00", "Ready-mix concrete 4000 psi", "Example RMC",
             "0", D(2026, 11, 3), "Consultant", D(2026, 11, 10), D(2026, 11, 20), "Accepted", None],
)

SPECS["Documents"] = dict(
    tab_color="38761D",
    purpose="DOC-01/02: drawing and document register with revisions.",
    cols=[
        col("id", "Document no.", 13),
        col("project", "Project", 11, dv=PROJECTS),
        col("discipline", "Discipline", 13, dv=lst("Discipline")),
        col("title", "Title", 28),
        col("rev", "Revision", 8, fmt="@"),
        col("date", "Revision date", 11, fmt=DATE),
        col("status", "Status", 15, dv=lst("Document status")),
        col("afu", "Approved for use", 10, dv=lst("Yes/No")),
        col("approver", "Approved by", 13),
        col("superseded", "Superseded by", 12),
        col("link", "File link", 22),
    ],
    example=["A-301", "PRJ-001", "Architectural", "Roof plan and sections", "B", D(2026, 11, 18), "Published",
             "Yes", "Consultant", None, None],
)

SPECS["Quality & Punch"] = dict(
    tab_color="38761D",
    purpose="QUAL-01..03, HAND-01: inspections, nonconformances, punch and handover items.",
    cols=[
        col("id", "Item ID", 10),
        col("project", "Project", 11, dv=PROJECTS),
        col("date", "Date", 11, fmt=DATE),
        col("type", "Type", 13, dv=lst("Quality type")),
        col("location", "Location", 14),
        col("desc", "Description / criteria", 28),
        col("severity", "Severity", 9, dv=lst("Severity")),
        col("responsible", "Responsible party", 15),
        col("due", "Due date", 11, fmt=DATE),
        col("action", "Corrective action", 22),
        col("status", "Status", 11, dv=lst("Quality status")),
        col("rework", "Rework cost (PKR)", 12, fmt=MONEY),
        col("verified", "Verified by", 13),
        col("check", "Check", 18, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(AND({c("severity")}{r}="Critical",{c("status")}{r}<>"Accepted",{c("status")}{r}<>"Closed"),"Blocks handover",IF(AND({c("due")}{r}<>"",{c("due")}{r}<TODAY(),{c("status")}{r}<>"Accepted",{c("status")}{r}<>"Closed"),"Overdue","")))'),
    ],
    example=["QC-001", "PRJ-001", D(2026, 11, 28), "Inspection", "Block A level 1", "Slab reinforcement before casting",
             "High", "Steel fixer", D(2026, 11, 29), None, "Accepted", 0, "S. Ahmed"],
)

SPECS["Safety"] = dict(
    tab_color="38761D",
    purpose="SAFE-01: hazards, near misses, incidents and toolbox talks. Keep injury details in restricted records.",
    cols=[
        col("id", "Safety ID", 10),
        col("project", "Project", 11, dv=PROJECTS),
        col("date", "Date", 11, fmt=DATE),
        col("type", "Type", 12, dv=lst("Safety type")),
        col("desc", "Description", 30),
        col("severity", "Severity", 9, dv=lst("Severity")),
        col("owner", "Owner", 13),
        col("action", "Corrective action", 24),
        col("due", "Due date", 11, fmt=DATE),
        col("closed", "Closed", 8, dv=lst("Yes/No")),
        col("check", "Check", 12, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(AND({c("closed")}{r}<>"Yes",{c("due")}{r}<>"",{c("due")}{r}<TODAY()),"Overdue",""))'),
    ],
    example=["SF-001", "PRJ-001", D(2026, 11, 25), "Toolbox talk", "Working at height, 18 attendees", "Low",
             "R. Ali", None, None, "Yes"],
)

SPECS["Lookahead"] = dict(
    tab_color="38761D",
    purpose="PLAN-01 / LOOK-01: two-to-six-week lookahead with constraints. Not ready while a blocker is open.",
    cols=[
        col("project", "Project", 11, dv=PROJECTS),
        col("activity", "Activity", 26),
        col("location", "Location / trade", 16),
        col("start", "Planned start", 11, fmt=DATE),
        col("finish", "Planned finish", 11, fmt=DATE),
        col("owner", "Work owner", 13),
        col("blocker", "Constraint / blocker", 24),
        col("blocker_owner", "Blocker owner", 13),
        col("resolve_by", "Resolve by", 11, fmt=DATE),
        col("resolved", "Blocker resolved", 9, dv=lst("Yes/No")),
        col("actual", "Actual finish", 11, fmt=DATE),
        col("reason", "Non-completion reason", 20),
        col("ready", "Readiness", 12, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("project")}{r}="","",IF({c("actual")}{r}<>"","",IF(AND({c("blocker")}{r}<>"",{c("resolved")}{r}<>"Yes"),"Not ready",IF(AND({c("finish")}{r}<>"",{c("finish")}{r}<TODAY()),"Late",""))))'),
    ],
    example=["PRJ-001", "Roof parapet wall", "Roof / masonry", D(2026, 12, 7), D(2026, 12, 12), "R. Ali",
             "Blocks delivery", "Procurement", D(2026, 12, 4), "No"],
)

SPECS["Leads"] = dict(
    tab_color="999999",
    purpose="CRM-01/02 (R3 in the PRD): enquiries and follow-ups.",
    cols=[
        col("id", "Lead ID", 9),
        col("date", "Date", 11, fmt=DATE),
        col("client", "Client name", 22),
        col("source", "Source", 12, dv=lst("Lead source")),
        col("contact", "Contact", 16),
        col("phone", "Phone", 14, fmt="@"),
        col("location", "Location", 14),
        col("work", "Expected work", 24),
        col("value", "Estimated value (PKR)", 15, fmt=MONEY),
        col("owner", "Owner", 13),
        col("next", "Next follow-up", 11, fmt=DATE),
        col("status", "Status", 10, dv=lst("Lead status")),
        col("loss", "Loss reason", 18),
        col("check", "Check", 16, "auto", flag=True,
            f=lambda r, c: f'=IF(${c("id")}{r}="","",IF(AND({c("next")}{r}<>"",{c("next")}{r}<TODAY(),{c("status")}{r}<>"Won",{c("status")}{r}<>"Lost"),"Follow-up overdue",IF(AND({c("status")}{r}="Lost",{c("loss")}{r}=""),"Add loss reason","")))'),
    ],
    example=["LD-001", D(2026, 11, 2), "Example Developers", "Referral", "H. Shah", None, "Islamabad",
             "G+3 commercial building", 45000000, "A. Khan", D(2026, 11, 20), "Quoted"],
)

ORDER = ["Projects", "Parties", "Cost Codes", "Workers", "Budget", "BOQ", "Measurements", "RA Bills", "Receipts",
         "Change Events", "Requisitions", "Purchase Orders", "Goods Receipts", "Supplier Invoices",
         "Labour Attendance", "Labour Advances", "Site Expenses", "Daily Diary", "RFIs", "Submittals", "Documents",
         "Quality & Punch", "Safety", "Lookahead", "Leads"]

for name in ORDER:
    LETTERS[name] = {cdef["key"]: get_column_letter(i + 1) for i, cdef in enumerate(SPECS[name]["cols"])}

def build_xlsx():
    # ---------------------------------------------------------------------------
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    HDR_BORDER = Border(bottom=Side(style="medium", color="404040"))


    def style_header(cell, auto=False, fill=NAVY):
        cell.font = Font(name=FONT, bold=True, color="000000" if auto else "FFFFFF", italic=auto)
        cell.fill = PatternFill("solid", fgColor=GREY_HDR if auto else fill)
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = HDR_BORDER


    def build_register(ws, name):
        spec = SPECS[name]
        cols = spec["cols"]
        L = LETTERS[name]
        c = lambda k: L[k]
        ws.sheet_properties.tabColor = spec["tab_color"]
        for i, cd in enumerate(cols, start=1):
            auto = cd["kind"] == "auto"
            h = ws.cell(row=1, column=i, value=cd["header"] + (" (auto)" if auto else ""))
            style_header(h, auto)
            ws.column_dimensions[get_column_letter(i)].width = cd["width"]
        ws.row_dimensions[1].height = 48
        ws.freeze_panes = "B2" if name not in ("Cost Codes",) else "A2"

        examples = spec.get("example") or []
        if examples and not isinstance(examples[0], list):
            examples = [examples]
        n_ex = len(examples)

        for i, cd in enumerate(cols, start=1):
            letter = get_column_letter(i)
            fmt = cd.get("fmt")
            if cd["kind"] == "auto":
                for r in range(2, ROWS + 2):
                    cell = ws.cell(row=r, column=i, value=cd["f"](r, c))
                    cell.fill = PatternFill("solid", fgColor=AUTO_BG)
                    cell.font = Font(name=FONT)
                    if fmt:
                        cell.number_format = fmt
            else:
                if fmt:
                    for r in range(2, ROWS + 2):
                        ws.cell(row=r, column=i).number_format = fmt
            if cd.get("dv"):
                dv = DataValidation(type="list", formula1=cd["dv"], allow_blank=True, showDropDown=False)
                dv.error = "Pick a value from the list, or add it to the source list first."
                dv.errorStyle = "warning"
                ws.add_data_validation(dv)
                dv.add(f"{letter}2:{letter}{ROWS + 1}")
            if cd.get("flag"):
                ws.conditional_formatting.add(
                    f"{letter}2:{letter}{ROWS + 1}",
                    FormulaRule(formula=[f"LEN({letter}2)>0"], fill=PatternFill("solid", fgColor="F4CCCC"),
                                font=Font(color="990000", bold=True)))

        for ri, row in enumerate(examples, start=2):
            for i, v in enumerate(row, start=1):
                if v is None or cols[i - 1]["kind"] == "auto":
                    continue
                cell = ws.cell(row=ri, column=i, value=v)
                if name != "Cost Codes":
                    cell.font = EX_FONT
        ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{ROWS + 1}"


    # ---------------- Start Here ----------------
    ws = wb.active
    ws.title = "Start Here"
    ws.sheet_properties.tabColor = "C00000"
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 100
    ws["A1"] = "Construction ERP workbook"
    ws["A1"].font = Font(name=FONT, bold=True, size=18, color=NAVY)
    ws["A2"] = "Built from the Construction Intelligence Platform PRD v4 (R1 core). Amounts in PKR excluding recoverable tax."
    ws["A2"].font = Font(name=FONT, italic=True, color="595959")

    r = 4
    ws.cell(row=r, column=1, value="How the tabs are marked").font = Font(name=FONT, bold=True, size=12)
    r += 1
    legend = [("Dark blue header", "You type in this column. Many columns have dropdowns."),
              ("Grey header, (auto)", "Formula column. Do not type here; it fills in when the row's first column has a value."),
              ("Grey italic row", "Example row showing the expected format. Delete it (right-click the row number, Delete row) when you start."),
              ("Red cell in a Check column", "Something needs attention: duplicate, overdue, missing approval or over-limit."),
              ]
    for a, b in legend:
        ws.cell(row=r, column=1, value=a)
        ws.cell(row=r, column=2, value=b)
        r += 1
    ws["A5"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A5"].font = Font(name=FONT, color="FFFFFF", bold=True)
    ws["A6"].fill = PatternFill("solid", fgColor=GREY_HDR)
    ws["A6"].font = Font(name=FONT, italic=True, bold=True)
    ws["A7"].font = EX_FONT
    ws["A8"].fill = PatternFill("solid", fgColor="F4CCCC")
    ws["A8"].font = Font(name=FONT, color="990000", bold=True)

    r += 1
    ws.cell(row=r, column=1, value="Order to start adding data").font = Font(name=FONT, bold=True, size=12)
    r += 1
    steps = [
        ("1. Settings and Lists", "Check standard hours and overtime multiplier. Add your own units, statuses or sources at the bottom of any Lists column."),
        ("2. Cost Codes", "Replace the starter codes with your chart of cost codes."),
        ("3. Parties, Workers", "Add clients, suppliers, subcontractors and workers. Mark supplier bank details as verified only after an independent check."),
        ("4. Projects", "One row per project with contract value, retention, advance recovery and payment terms. Update U (remaining uncommitted cost) every month."),
        ("5. Budget, BOQ", "Enter the approved budget by cost code and the contract BOQ lines with Status = Approved. Add approved variations as new BOQ lines (version VO-01 etc.)."),
        ("6. Daily work", "Supervisors fill Daily Diary, Labour Attendance, Site Expenses, Goods Receipts, Quality & Punch and Safety."),
        ("7. Procurement", "Requisitions, then Purchase Orders (one row per PO line), Goods Receipts, then Supplier Invoices against the PO line."),
        ("8. Billing", "QS records cumulative quantities in Measurements, sets Status = Verified and the RA bill no. RA Bills totals the increments, then deducts retention and advance recovery. Record payments in Receipts."),
        ("9. Changes", "Log every instruction in Change Events. Only Approved or Partly approved amounts raise the contract value; the rest stays as pending exposure."),
        ("10. Review", "Dashboard shows each project's contract, cost, commitments, forecast, billing and alerts. Cost Report drills into one project by cost code."),
    ]
    for a, b in steps:
        ws.cell(row=r, column=1, value=a).font = Font(name=FONT, bold=True)
        ws.cell(row=r, column=2, value=b)
        r += 1

    r += 1
    ws.cell(row=r, column=1, value="Key definitions (PRD section 4)").font = Font(name=FONT, bold=True, size=12)
    r += 1
    defs = [
        ("Actual cost A", "Supplier invoices (not Draft) + labour attendance cost + site expenses."),
        ("Committed cost C", "Approved PO amounts not yet invoiced."),
        ("Uncommitted cost U", "PM/QS estimate of remaining work not in A or C (Projects tab). Left blank, the forecast shows as incomplete instead of zero."),
        ("ETC and EAC", "ETC = C + U. EAC = A + C + U."),
        ("Revised contract value", "Signed contract + approved variations from Change Events. Pending claims are excluded."),
        ("Forecast margin", "Revised contract value minus EAC."),
        ("Forecast variance", "Current approved budget minus EAC. Negative means forecast overrun."),
        ("Verified, not billed", "Value of verified measurement increments not yet assigned to an RA bill (certification backlog)."),
        ("RA bill net", "Gross certified work - retention (capped) - advance recovery (up to advance received) - other deductions."),
    ]
    for a, b in defs:
        ws.cell(row=r, column=1, value=a).font = Font(name=FONT, bold=True)
        ws.cell(row=r, column=2, value=b)
        r += 1

    r += 1
    ws.cell(row=r, column=1, value="Tab guide").font = Font(name=FONT, bold=True, size=12)
    r += 1
    for name in ORDER:
        ws.cell(row=r, column=1, value=name).font = Font(name=FONT, bold=True)
        ws.cell(row=r, column=2, value=SPECS[name]["purpose"])
        r += 1
    ws.cell(row=r, column=1, value="Dashboard").font = Font(name=FONT, bold=True)
    ws.cell(row=r, column=2, value="FIN-06 / UX-01: one row per project with cost, forecast, billing, collection and alert counts.")
    r += 1
    ws.cell(row=r, column=1, value="Cost Report").font = Font(name=FONT, bold=True)
    ws.cell(row=r, column=2, value="Pick a project in cell B1 to see budget, actual and committed cost by cost code.")
    r += 2
    ws.cell(row=r, column=1, value="Limits").font = Font(name=FONT, bold=True, size=12)
    r += 1
    ws.cell(row=r, column=2, value=(f"Each register has formulas pre-filled for {ROWS} rows. To add more, select the last row, copy it and paste below. "
                                    "A spreadsheet cannot enforce approvals or lock approved records: use Data > Protect ranges and version history "
                                    "to protect approved BOQ lines and closed months."))
    for row in ws.iter_rows(min_row=4, max_row=r, max_col=2):
        for cell in row:
            if cell.font is None or cell.font.name != FONT:
                cell.font = Font(name=FONT, bold=cell.font.bold if cell.font else False,
                                 color=cell.font.color if cell.font else None)
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------------- Settings ----------------
    st = wb.create_sheet("Settings")
    st.sheet_properties.tabColor = "C00000"
    st.column_dimensions["A"].width = 38
    st.column_dimensions["B"].width = 14
    st.column_dimensions["C"].width = 50
    st["A1"] = "Setting"; st["B1"] = "Value"; st["C1"] = "Used by"
    for cell in (st["A1"], st["B1"], st["C1"]):
        style_header(cell)
    settings = [("Company name", "Your company", "Report headings"),
                ("Standard hours per day", 8, "Labour Attendance cost = daily rate / standard hours x hours"),
                ("Overtime multiplier", 1.5, "Labour Attendance overtime cost"),
                ("Currency", "PKR", "All amounts")]
    for i, (a, b, cc) in enumerate(settings, start=2):
        st.cell(row=i, column=1, value=a).font = Font(name=FONT)
        v = st.cell(row=i, column=2, value=b)
        v.font = Font(name=FONT, color="0000FF")
        v.fill = PatternFill("solid", fgColor="FFF2CC")
        st.cell(row=i, column=3, value=cc).font = Font(name=FONT)

    # ---------------- Registers ----------------
    for name in ORDER:
        build_register(wb.create_sheet(name), name)

    # ---------------- Dashboard ----------------
    db = wb.create_sheet("Dashboard", 2)
    db.sheet_properties.tabColor = "C00000"
    P = LETTERS["Projects"]


    def pj(key, r):
        return f"Projects!${P[key]}{r}"


    dash_cols = [
        ("Project", 11, None, lambda r: f'=IF(Projects!$A{r - 2}="","",Projects!$A{r - 2})'),
        ("Project name", 26, None, lambda r: f'=IF($A{r}="","",Projects!$B{r - 2})'),
        ("Status", 10, None, lambda r: f'=IF($A{r}="","",{pj("status", r - 2)})'),
        ("Signed contract", 14, MONEY, lambda r: f'=IF($A{r}="","",N({pj("contract", r - 2)}))'),
        ("Approved variations", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Change Events","approved_var")},{X("Change Events","project")},$A{r}))'),
        ("Revised contract", 14, MONEY, lambda r: f'=IF($A{r}="","",D{r}+E{r})'),
        ("Current budget", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Budget","current")},{X("Budget","project")},$A{r}))'),
        ("Actual cost A", 14, MONEY, lambda r: (f'=IF($A{r}="","",SUMIFS({X("Supplier Invoices","amount")},{X("Supplier Invoices","project")},$A{r},{X("Supplier Invoices","status")},"<>Draft")'
                                               f'+SUMIFS({X("Labour Attendance","cost")},{X("Labour Attendance","project")},$A{r})+SUMIFS({X("Site Expenses","amount")},{X("Site Expenses","project")},$A{r}))')),
        ("Committed C", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Purchase Orders","open")},{X("Purchase Orders","project")},$A{r}))'),
        ("Uncommitted U", 14, MONEY, lambda r: f'=IF($A{r}="","",IF({pj("u", r - 2)}="","Missing",{pj("u", r - 2)}))'),
        ("EAC = A+C+U", 14, MONEY, lambda r: f'=IF($A{r}="","",IF(J{r}="Missing","Incomplete",H{r}+I{r}+J{r}))'),
        ("Forecast variance", 14, MONEY, lambda r: f'=IF($A{r}="","",IF(K{r}="Incomplete","Incomplete",G{r}-K{r}))'),
        ("Forecast margin", 14, MONEY, lambda r: f'=IF($A{r}="","",IF(K{r}="Incomplete","Incomplete",F{r}-K{r}))'),
        ("Margin %", 10, PCT, lambda r: f'=IF(OR($A{r}="",K{r}="Incomplete"),"",IF(F{r}=0,0,M{r}/F{r}))'),
        ("Verified, not billed", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Measurements","value")},{X("Measurements","project")},$A{r},{X("Measurements","bill")},""))'),
        ("Billed net", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","net")},{X("RA Bills","project")},$A{r},{X("RA Bills","status")},"<>Draft",{X("RA Bills","status")},"<>Rejected"))'),
        ("Received", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Receipts","amount")},{X("Receipts","project")},$A{r})+SUMIFS({X("Receipts","wht")},{X("Receipts","project")},$A{r}))'),
        ("Receivable", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","outstanding")},{X("RA Bills","project")},$A{r}))'),
        ("Overdue receivable", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","outstanding")},{X("RA Bills","project")},$A{r},{X("RA Bills","overdue")},">0"))'),
        ("Retention held", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("RA Bills","ret")},{X("RA Bills","project")},$A{r},{X("RA Bills","status")},"<>Draft",{X("RA Bills","status")},"<>Rejected"))'),
        ("Payables due", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Supplier Invoices","balance")},{X("Supplier Invoices","project")},$A{r}))'),
        ("Pending claims", 14, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Change Events","pending")},{X("Change Events","project")},$A{r}))'),
        ("Open items needing action", 12, INT, lambda r: (f'=IF($A{r}="","",COUNTIFS({X("Change Events","project")},$A{r},{X("Change Events","check")},"?*")'
                                                         f'+COUNTIFS({X("RFIs","project")},$A{r},{X("RFIs","check")},"?*")+COUNTIFS({X("Submittals","project")},$A{r},{X("Submittals","check")},"?*")'
                                                         f'+COUNTIFS({X("Quality & Punch","project")},$A{r},{X("Quality & Punch","check")},"?*")+COUNTIFS({X("Safety","project")},$A{r},{X("Safety","check")},"?*")'
                                                         f'+COUNTIFS({X("Lookahead","project")},$A{r},{X("Lookahead","ready")},"?*"))')),
        ("Critical punch open", 10, INT, lambda r: f'=IF($A{r}="","",COUNTIFS({X("Quality & Punch","project")},$A{r},{X("Quality & Punch","check")},"Blocks handover"))'),
    ]
    FIRST = 4
    db["A1"] = "Project dashboard (PKR)"
    db["A1"].font = Font(name=FONT, bold=True, size=14, color=NAVY)
    db["E1"] = "As of"
    db["E1"].font = Font(name=FONT, bold=True)
    db["F1"] = "=TODAY()"
    db["F1"].number_format = DATE
    db["A2"] = "All projects"
    db["A2"].font = Font(name=FONT, bold=True)
    for i, (h, w, fmt, f) in enumerate(dash_cols, start=1):
        L = get_column_letter(i)
        db.column_dimensions[L].width = w
        style_header(db.cell(row=3, column=i, value=h), fill=TEAL)
        for r in range(FIRST, FIRST + PROJ_ROWS):
            cell = db.cell(row=r, column=i, value=f(r))
            cell.font = Font(name=FONT)
            if fmt:
                cell.number_format = fmt
        if fmt in (MONEY, INT) and i >= 4 and h not in ("Uncommitted U",):
            tot = db.cell(row=2, column=i, value=f"=SUM({L}{FIRST}:{L}{FIRST + PROJ_ROWS - 1})")
            tot.font = Font(name=FONT, bold=True)
            tot.number_format = fmt
            tot.fill = PatternFill("solid", fgColor="DDEBF7")
    for col_idx in (10, 11, 12, 13, 14):
        db.cell(row=2, column=col_idx).value = None
    db.cell(row=2, column=10, value="Totals of A, C and forecast only make sense when every project has U.").font = Font(name=FONT, italic=True, color="595959")
    db.row_dimensions[3].height = 45
    db.freeze_panes = "C4"
    db.conditional_formatting.add(f"W{FIRST}:X{FIRST + PROJ_ROWS - 1}",
                                  FormulaRule(formula=[f"N(W{FIRST})>0"], fill=PatternFill("solid", fgColor="F4CCCC"),
                                              font=Font(color="990000", bold=True)))
    db.conditional_formatting.add(f"J{FIRST}:L{FIRST + PROJ_ROWS - 1}",
                                  FormulaRule(formula=[f'OR(J{FIRST}="Missing",J{FIRST}="Incomplete")'],
                                              fill=PatternFill("solid", fgColor="FFF2CC")))

    # ---------------- Cost Report ----------------
    cr = wb.create_sheet("Cost Report", 3)
    cr.sheet_properties.tabColor = "C00000"
    cr["A1"] = "Project"
    cr["A1"].font = Font(name=FONT, bold=True)
    cr["B1"] = "PRJ-001"
    cr["B1"].font = Font(name=FONT, bold=True, color="0000FF")
    cr["B1"].fill = PatternFill("solid", fgColor="FFF2CC")
    dv = DataValidation(type="list", formula1=PROJECTS, allow_blank=False)
    cr.add_data_validation(dv)
    dv.add("B1")
    cr["C1"] = f'=IFERROR(INDEX(Projects!$B:$B,MATCH(B1,Projects!$A:$A,0)),"Pick a project")'
    cr["C1"].font = Font(name=FONT, italic=True)
    cr_cols = [
        ("Cost code", 12, None, lambda r: f"=IF('Cost Codes'!$A{r - 2}=\"\",\"\",'Cost Codes'!$A{r - 2})"),
        ("Description", 28, None, lambda r: f"=IF($A{r}=\"\",\"\",'Cost Codes'!$B{r - 2})"),
        ("Current budget", 15, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Budget","current")},{X("Budget","project")},$B$1,{X("Budget","code")},$A{r}))'),
        ("Supplier invoices", 15, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Supplier Invoices","amount")},{X("Supplier Invoices","project")},$B$1,{X("Supplier Invoices","code")},$A{r},{X("Supplier Invoices","status")},"<>Draft"))'),
        ("Labour", 15, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Labour Attendance","cost")},{X("Labour Attendance","project")},$B$1,{X("Labour Attendance","code")},$A{r}))'),
        ("Site expenses", 15, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Site Expenses","amount")},{X("Site Expenses","project")},$B$1,{X("Site Expenses","code")},$A{r}))'),
        ("Actual cost A", 15, MONEY, lambda r: f'=IF($A{r}="","",D{r}+E{r}+F{r})'),
        ("Committed C", 15, MONEY, lambda r: f'=IF($A{r}="","",SUMIFS({X("Purchase Orders","open")},{X("Purchase Orders","project")},$B$1,{X("Purchase Orders","code")},$A{r}))'),
        ("Budget left after A and C", 17, MONEY, lambda r: f'=IF($A{r}="","",C{r}-G{r}-H{r})'),
        ("% of budget used", 11, PCT, lambda r: f'=IF($A{r}="","",IF(C{r}=0,0,(G{r}+H{r})/C{r}))'),
    ]
    for i, (h, w, fmt, f) in enumerate(cr_cols, start=1):
        L = get_column_letter(i)
        cr.column_dimensions[L].width = w
        style_header(cr.cell(row=3, column=i, value=h), fill=TEAL)
        for r in range(4, 104):
            cell = cr.cell(row=r, column=i, value=f(r))
            cell.font = Font(name=FONT)
            if fmt:
                cell.number_format = fmt
        if fmt == MONEY:
            t = cr.cell(row=2, column=i, value=f"=SUM({L}4:{L}103)")
            t.number_format = MONEY
            t.font = Font(name=FONT, bold=True)
            t.fill = PatternFill("solid", fgColor="DDEBF7")
    cr["A2"] = "Total"
    cr["A2"].font = Font(name=FONT, bold=True)
    cr["J2"] = '=IF(C2=0,0,(G2+H2)/C2)'
    cr["J2"].number_format = PCT
    cr.row_dimensions[3].height = 32
    cr.freeze_panes = "C4"
    cr["L3"] = ("Costs entered without a cost code do not appear here. Check the Check column on Supplier Invoices.")
    cr["L3"].font = Font(name=FONT, italic=True, color="595959")

    # ---------------- Lists ----------------
    ls = wb.create_sheet("Lists")
    ls.sheet_properties.tabColor = "595959"
    for i, (name, values) in enumerate(LISTS.items(), start=1):
        style_header(ls.cell(row=1, column=i, value=name), fill="595959")
        ls.column_dimensions[get_column_letter(i)].width = max(14, len(name) + 2)
        for j, v in enumerate(values, start=2):
            ls.cell(row=j, column=i, value=v).font = Font(name=FONT)
    ls.row_dimensions[1].height = 32
    ls.freeze_panes = "A2"


    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Construction_ERP_Workbook.xlsx")
    wb.save(out)
    print(out, os.path.getsize(out), "bytes")
    print(wb.sheetnames)


if __name__ == "__main__":
    build_xlsx()

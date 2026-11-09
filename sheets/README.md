# Construction ERP workbook (Google Sheets)

`Construction_ERP_Workbook.xlsx` is a working spreadsheet version of the R1 core in
`Construction_AI_ERP_Focused_Scope_PRD_v4.docx`.

## Open it in Google Sheets

1. Go to https://sheets.google.com and create a blank spreadsheet, or open Google Drive.
2. In Sheets: **File > Import > Upload**, pick `Construction_ERP_Workbook.xlsx`, choose
   **Replace spreadsheet**. (In Drive: **New > File upload**, then right-click the file >
   **Open with > Google Sheets**.)
3. Read the **Start Here** tab, delete the grey example rows, and start entering data.

## Rebuild

```bash
python3 sheets/build_workbook.py
```

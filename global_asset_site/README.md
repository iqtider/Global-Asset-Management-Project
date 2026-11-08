# Global Asset Management – Django site

A small web front end for the `global_asset` MySQL database. It shows a dashboard, runs the 15 project queries with one click, displays the `v_operations` view, lets you browse every table, and has forms that use the stored procedure and both triggers.

## What you need

- Python 3.10 or newer
- MySQL 8.0 or newer, running on your computer (MySQL Workbench is fine)

## Setup (about 5 minutes)

1. **Create the database.** Open `setup.sql` in MySQL Workbench and run it (lightning-bolt button), or from a terminal:
   ```
   mysql -u root -p < setup.sql
   ```
   This drops and recreates `global_asset` with all tables, sample data, the view, the function, the procedure and the triggers.

2. **Install the Python packages.** In a terminal inside this folder:
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)
   source venv/bin/activate     (Mac/Linux)
   pip install -r requirements.txt
   ```

3. **Tell the site your MySQL password.** It logs in as `root` with no password unless you set these:
   ```
   set DB_PASSWORD=yourpassword           (Windows Command Prompt)
   $env:DB_PASSWORD="yourpassword"        (Windows PowerShell)
   export DB_PASSWORD=yourpassword        (Mac/Linux)
   ```
   `DB_USER`, `DB_HOST`, `DB_PORT` and `DB_NAME` work the same way if yours differ.

4. **Start the site.**
   ```
   python manage.py runserver
   ```
   Open http://127.0.0.1:8000 in your browser.

## Pages

| Page | What it shows |
| --- | --- |
| Dashboard | Counts of agencies, agents, assets, etc., and asset risk levels from `fn_asset_risk()` |
| Queries | All 15 queries as cards. Each page shows the problem, the results table and the SQL. Queries 3–5 have a dropdown to pick the agent, meeting place or country. |
| Operations (view) | Everything in `v_operations`, with a colour-coded risk column |
| Manage assets | Add an asset (the `trg_asset_value_check` trigger rejects values other than High/Medium/Low) and reassign an agent (`sp_assign_asset` procedure; the `trg_agent_reassign` trigger writes to the log shown below the form) |
| Tables | Raw contents of every table |

## Demo script for the presentation

1. Dashboard: point out the counts and risk levels (stored function).
2. Queries: open 2 (big join), 8 (GROUP BY), 11 (HAVING), 14 (correlated subquery). On query 5, switch the country in the dropdown.
3. Operations: the view in action.
4. Manage assets: type "Extreme" as a value and show the trigger rejecting it. Then add a valid asset, reassign an agent to it, and show the new row in the assignment log.
5. Try assigning an asset that already has a handler to show the procedure's error check.

To reset the data after a demo, run `setup.sql` again.

## Troubleshooting

- **"Access denied for user 'root'"**: set `DB_PASSWORD` (step 3) in the same terminal before `runserver`.
- **"Unknown database 'global_asset'"**: run `setup.sql` first.
- **"FUNCTION fn_asset_risk does not exist"**: you created the tables some other way; run `setup.sql` so the view, function, procedure and triggers exist.

from urllib.parse import urlencode

from django.db import DatabaseError, connection
from django.http import Http404
from django.shortcuts import redirect, render
from .auth import login_required
from .queries import QUERIES

QUERIES_BY_NUMBER = {q["number"]: q for q in QUERIES}

# Tables a visitor may browse, with the column to sort by.
TABLES = {
    "Region": "RegionName",
    "country": "CountryName",
    "Agency": "AgencyName",
    "Agent": "AgentID",
    "Asset": "AssetID",
    "Ways_of_Contact": "DesignatedPlace",
    "Assignment_Log": "LogID",
}


def run_sql(sql, params=None):
    """Run a query and return (column names, rows)."""
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description] if cursor.description else []
        rows = cursor.fetchall() if cursor.description else []
    return columns, rows


def error_message(exc):
    # MySQL errors arrive as (code, message); show only the message.
    args = getattr(exc, "args", ())
    return args[1] if len(args) > 1 else str(exc)

@login_required
def home(request):
    counts = {}
    for label, table in [("Agencies", "Agency"), ("Agents", "Agent"), ("Assets", "Asset"),
                         ("Countries", "country"), ("Regions", "Region"), ("Meeting places", "Ways_of_Contact")]:
        counts[label] = run_sql(f"SELECT COUNT(*) FROM {table}")[1][0][0]
    _, risk_rows = run_sql(
        "SELECT fn_asset_risk(AssetID) AS Risk, COUNT(*) FROM Asset GROUP BY Risk "
        "ORDER BY FIELD(Risk, 'Critical', 'Elevated', 'Routine')"
    )
    return render(request, "dashboard/home.html", {
        "counts": counts,
        "risk_rows": risk_rows,
        "queries": QUERIES,
        "tables": TABLES,
    })


def query_list(request):
    return render(request, "dashboard/query_list.html", {"queries": QUERIES, "tables": TABLES})


def query_detail(request, number):
    query = QUERIES_BY_NUMBER.get(number)
    if query is None:
        raise Http404("No such query")

    options, chosen, params = [], None, None
    if query["param"]:
        options = [row[0] for row in run_sql(query["param"]["options_sql"])[1]]
        chosen = request.GET.get("value", query["param"]["default"])
        if chosen not in options:
            chosen = query["param"]["default"]
        params = [chosen]

    columns, rows = run_sql(query["sql"], params)
    return render(request, "dashboard/query_detail.html", {
        "query": query,
        "columns": columns,
        "rows": rows,
        "options": options,
        "chosen": chosen,
        "prev": QUERIES_BY_NUMBER.get(number - 1),
        "next": QUERIES_BY_NUMBER.get(number + 1),
        "tables": TABLES,
    })


def operations(request):
    columns, rows = run_sql(
        "SELECT AssetName, AssetValue, AssetCountry, CountryRegion, Accessibility, "
        "fn_asset_risk(AssetID) AS Risk, Handler, Agency, MeetingPlace, RecognitionSignal "
        "FROM v_operations ORDER BY AssetID"
    )
    return render(request, "dashboard/operations.html", {"columns": columns, "rows": rows, "tables": TABLES})


def table_view(request, table):
    if table not in TABLES:
        raise Http404("No such table")
    columns, rows = run_sql(f"SELECT * FROM `{table}` ORDER BY `{TABLES[table]}`")
    return render(request, "dashboard/table.html", {
        "table": table, "columns": columns, "rows": rows, "tables": TABLES,
    })


def manage(request):
    """Add an asset (checked by trg_asset_value_check) and reassign agents (sp_assign_asset + trg_agent_reassign)."""
    message, error = request.GET.get("ok"), None

    if request.method == "POST":
        action = request.POST.get("action")
        try:
            if action == "add_asset":
                run_sql(
                    "INSERT INTO Asset (AssetID, AssetName, AssetCountry, AssetWays_of_Contact, AssetValue, AssetConnection) "
                    "VALUES ((SELECT next_id FROM (SELECT COALESCE(MAX(AssetID), 0) + 1 AS next_id FROM Asset) t), "
                    "%s, %s, %s, %s, %s)",
                    [request.POST["name"].strip(), request.POST["country"], request.POST["place"],
                     request.POST["value"].strip(), request.POST["connection"].strip()],
                )
                return redirect(f"{request.path}?{urlencode({'ok': 'Asset added.'})}")
            if action == "assign":
                run_sql("CALL sp_assign_asset(%s, %s)", [request.POST["agent"], request.POST["asset"]])
                return redirect(f"{request.path}?{urlencode({'ok': 'Asset reassigned. The trigger logged the change below.'})}")
        except DatabaseError as exc:
            error = error_message(exc)

    agents = run_sql(
        "SELECT ag.AgentID, ag.AgentName, ag.AgentAgency, a.AssetName FROM Agent ag "
        "LEFT JOIN Asset a ON ag.AgentAssets = a.AssetID ORDER BY ag.AgentName"
    )[1]
    assets = run_sql(
        "SELECT a.AssetID, a.AssetName, a.AssetCountry, ag.AgentName FROM Asset a "
        "LEFT JOIN Agent ag ON ag.AgentAssets = a.AssetID ORDER BY a.AssetID"
    )[1]
    countries = [r[0] for r in run_sql("SELECT CountryName FROM country ORDER BY CountryName")[1]]
    places = [r[0] for r in run_sql("SELECT DesignatedPlace FROM Ways_of_Contact ORDER BY DesignatedPlace")[1]]
    log_columns, log_rows = run_sql(
        "SELECT l.LogID, ag.AgentName, old.AssetName AS OldAsset, new.AssetName AS NewAsset, l.ChangedAt "
        "FROM Assignment_Log l "
        "LEFT JOIN Agent ag ON l.AgentID = ag.AgentID "
        "LEFT JOIN Asset old ON l.OldAssetID = old.AssetID "
        "LEFT JOIN Asset new ON l.NewAssetID = new.AssetID "
        "ORDER BY l.LogID DESC"
    )
    return render(request, "dashboard/manage.html", {
        "message": message, "error": error,
        "agents": agents, "assets": assets, "countries": countries, "places": places,
        "log_columns": log_columns, "log_rows": log_rows, "tables": TABLES,
    })

"""The 15 queries from 03_queries.sql, with titles for the website.

Queries 3 to 5 take a value picked on the page (agent, meeting place, country)
instead of the fixed example in the .sql file.
"""

QUERIES = [
    {
        "number": 1,
        "title": 'Asset map',
        "problem": 'every asset with its country, region and how hard that region is to get into.',
        "techniques": 'JOIN',
        "param": None,
        "sql": """
SELECT a.AssetName, a.AssetCountry, c.CountryRegion, r.Accessibility
FROM Asset a
JOIN country c ON a.AssetCountry = c.CountryName
JOIN Region r  ON c.CountryRegion = r.RegionName
ORDER BY r.Accessibility, a.AssetName;
""",
    },
    {
        "number": 2,
        "title": 'Handler briefing sheet',
        "problem": 'each agent, their agency, the asset they run, where they meet and the recognition signal.',
        "techniques": 'multi-table JOIN',
        "param": None,
        "sql": """
SELECT ag.AgentName, ag.AgentAgency, a.AssetName, a.AssetCountry,
       w.DesignatedPlace AS MeetingPlace, w.Visual_Confirmation AS RecognitionSignal
FROM Agent ag
JOIN Asset a           ON ag.AgentAssets = a.AssetID
JOIN Ways_of_Contact w ON a.AssetWays_of_Contact = w.DesignatedPlace
ORDER BY ag.AgentAgency, ag.AgentName;
""",
    },
    {
        "number": 3,
        "title": 'Compromised agent',
        "problem": 'if an agent is exposed, which asset and meeting place are now at risk?',
        "techniques": 'JOIN, WHERE',
        "param": {"label": 'Agent', "options_sql": 'SELECT AgentName FROM Agent ORDER BY AgentName', "default": 'Tom Becker'},
        "sql": """
SELECT ag.AgentName, a.AssetName, a.AssetWays_of_Contact AS MeetingPlaceAtRisk
FROM Agent ag
JOIN Asset a ON ag.AgentAssets = a.AssetID
WHERE ag.AgentName = %s;
""",
    },
    {
        "number": 4,
        "title": 'Burned meeting place',
        "problem": 'if a meeting place is discovered, which assets and handlers used it?',
        "techniques": 'JOIN, WHERE',
        "param": {"label": 'Meeting place', "options_sql": 'SELECT DISTINCT AssetWays_of_Contact FROM Asset ORDER BY 1', "default": 'Cafe'},
        "sql": """
SELECT a.AssetName, a.AssetCountry, ag.AgentName AS Handler
FROM Asset a
JOIN Agent ag ON ag.AgentAssets = a.AssetID
WHERE a.AssetWays_of_Contact = %s;
""",
    },
    {
        "number": 5,
        "title": 'Country crisis',
        "problem": 'when trouble breaks out in a country, which assets are there and who must be contacted?',
        "techniques": 'JOIN, WHERE',
        "param": {"label": 'Country', "options_sql": 'SELECT DISTINCT AssetCountry FROM Asset ORDER BY 1', "default": 'Iran'},
        "sql": """
SELECT a.AssetName, a.AssetValue, ag.AgentName AS Handler, ag.AgentAgency
FROM Asset a
JOIN Agent ag ON ag.AgentAssets = a.AssetID
WHERE a.AssetCountry = %s;
""",
    },
    {
        "number": 6,
        "title": 'High-value watchlist',
        "problem": 'our most valuable assets and the agents responsible for them.',
        "techniques": 'JOIN, WHERE',
        "param": None,
        "sql": """
SELECT a.AssetName, a.AssetCountry, a.AssetConnection, ag.AgentName AS Handler
FROM Asset a
JOIN Agent ag ON ag.AgentAssets = a.AssetID
WHERE a.AssetValue = 'High'
ORDER BY a.AssetCountry;
""",
    },
    {
        "number": 7,
        "title": 'Coverage gaps',
        "problem": 'countries in the database where we have no assets at all.',
        "techniques": 'LEFT JOIN, IS NULL',
        "param": None,
        "sql": """
SELECT c.CountryName, c.CountryRegion
FROM country c
LEFT JOIN Asset a ON a.AssetCountry = c.CountryName
WHERE a.AssetID IS NULL;
""",
    },
    {
        "number": 8,
        "title": 'Regional strength',
        "problem": 'how many assets each region has, and how many of them are high value.',
        "techniques": 'JOIN, COUNT, SUM, GROUP BY',
        "param": None,
        "sql": """
SELECT c.CountryRegion, COUNT(*) AS TotalAssets, SUM(a.AssetValue = 'High') AS HighValueAssets
FROM Asset a
JOIN country c ON a.AssetCountry = c.CountryName
GROUP BY c.CountryRegion
ORDER BY TotalAssets DESC, c.CountryRegion;
""",
    },
    {
        "number": 9,
        "title": 'Agency workload',
        "problem": 'how many agents each agency has in the field.',
        "techniques": 'COUNT, GROUP BY, ORDER BY',
        "param": None,
        "sql": """
SELECT AgentAgency, COUNT(*) AS AgentsInField
FROM Agent
GROUP BY AgentAgency
ORDER BY AgentsInField DESC, AgentAgency;
""",
    },
    {
        "number": 10,
        "title": 'Agency value breakdown',
        "problem": 'how many High, Medium and Low value assets each agency runs.',
        "techniques": 'JOIN, CASE, SUM, GROUP BY',
        "param": None,
        "sql": """
SELECT ag.AgentAgency,
       SUM(CASE WHEN a.AssetValue = 'High'   THEN 1 ELSE 0 END) AS High,
       SUM(CASE WHEN a.AssetValue = 'Medium' THEN 1 ELSE 0 END) AS Medium,
       SUM(CASE WHEN a.AssetValue = 'Low'    THEN 1 ELSE 0 END) AS Low
FROM Agent ag
JOIN Asset a ON ag.AgentAssets = a.AssetID
GROUP BY ag.AgentAgency
ORDER BY High DESC, ag.AgentAgency;
""",
    },
    {
        "number": 11,
        "title": 'Overused meeting places',
        "problem": 'places used by more than one asset, which raises the risk of exposure.',
        "techniques": 'COUNT, GROUP BY, HAVING',
        "param": None,
        "sql": """
SELECT AssetWays_of_Contact AS MeetingPlace, COUNT(*) AS AssetsUsingIt,
       GROUP_CONCAT(AssetName ORDER BY AssetName SEPARATOR ', ') AS Assets
FROM Asset
GROUP BY AssetWays_of_Contact
HAVING COUNT(*) > 1
ORDER BY AssetsUsingIt DESC, MeetingPlace;
""",
    },
    {
        "number": 12,
        "title": 'No local agency',
        "problem": 'assets working in countries that have no intelligence agency of their own.',
        "techniques": 'Subquery with IN',
        "param": None,
        "sql": """
SELECT AssetName, AssetCountry, AssetConnection
FROM Asset
WHERE AssetCountry IN (SELECT CountryName FROM country WHERE CountryAgencies IS NULL)
ORDER BY AssetCountry, AssetName;
""",
    },
    {
        "number": 13,
        "title": 'Riskiest assignments',
        "problem": 'agents whose asset is in a region with restricted access.',
        "techniques": 'Nested subqueries',
        "param": None,
        "sql": """
SELECT AgentName, AgentAgency
FROM Agent
WHERE AgentAssets IN (
    SELECT AssetID FROM Asset
    WHERE AssetCountry IN (
        SELECT CountryName FROM country
        WHERE CountryRegion IN (SELECT RegionName FROM Region WHERE Accessibility = 'Restricted')))
ORDER BY AgentAgency, AgentName;
""",
    },
    {
        "number": 14,
        "title": 'Behind enemy lines',
        "problem": "agencies running an asset inside an adversary's home country.",
        "techniques": 'Correlated subquery with EXISTS',
        "param": None,
        "sql": """
SELECT ay.AgencyName, ay.Adversaries
FROM Agency ay
WHERE EXISTS (
    SELECT 1
    FROM Agent ag
    JOIN Asset a   ON ag.AgentAssets = a.AssetID
    JOIN country c ON a.AssetCountry = c.CountryName
    WHERE ag.AgentAgency = ay.AgencyName
      AND FIND_IN_SET(c.CountryAgencies, REPLACE(ay.Adversaries, ' ', '')) > 0);
""",
    },
    {
        "number": 15,
        "title": 'Possible teamwork',
        "problem": 'pairs of agents from the same or allied agencies whose assets are in the same region.',
        "techniques": 'Self JOIN',
        "param": None,
        "sql": """
SELECT ag1.AgentName AS Agent1, ag1.AgentAgency AS Agency1,
       ag2.AgentName AS Agent2, ag2.AgentAgency AS Agency2,
       c1.CountryRegion AS SharedRegion
FROM Agent ag1
JOIN Agent ag2   ON ag1.AgentID < ag2.AgentID
JOIN Agency ay1  ON ag1.AgentAgency = ay1.AgencyName
JOIN Asset a1    ON ag1.AgentAssets = a1.AssetID
JOIN Asset a2    ON ag2.AgentAssets = a2.AssetID
JOIN country c1  ON a1.AssetCountry = c1.CountryName
JOIN country c2  ON a2.AssetCountry = c2.CountryName
WHERE c1.CountryRegion = c2.CountryRegion
  AND (ag1.AgentAgency = ag2.AgentAgency
       OR FIND_IN_SET(ag2.AgentAgency, REPLACE(ay1.Allies, ' ', '')) > 0)
ORDER BY SharedRegion, Agent1, Agent2;
""",
    },
    {
        "number": 16,
        "title": 'Shifted Agent and Assets',
        "problem": 'agent assets and meeting places shifted across rows for operational deception.',
        "techniques": 'JOIN, Window functions (LEAD, LAG)',
        "param": None,
        "sql": """
SELECT 
    ag.AgentID,
    ag.AgentName,
    -- Shift the Asset ID down by 1 row
    LEAD(ag.AgentAssets, 1, ag.AgentAssets) OVER (ORDER BY ag.AgentID) AS False_AgentAssets,
    -- Shift the Ways of Contact up by 1 row
    LAG(a.AssetWays_of_Contact, 1, a.AssetWays_of_Contact) OVER (ORDER BY ag.AgentID) AS False_AgentWays_of_Contact,
    ag.AgentAgency
FROM Agent ag
LEFT JOIN Asset a ON ag.AgentAssets = a.AssetID
ORDER BY ag.AgentID;
""",
    },
{
        "number": 17,
        "title": 'True Agent Operations',
        "problem": 'baseline view of agents, their assigned assets, and their meeting places.',
        "techniques": 'JOIN',
        "param": None,
        "sql": """
SELECT 
    ag.AgentID,
    ag.AgentName,
    ag.AgentAssets,
    a.AssetWays_of_Contact AS AgentWays_of_Contact,
    ag.AgentAgency
FROM Agent ag
LEFT JOIN Asset a ON ag.AgentAssets = a.AssetID
ORDER BY ag.AgentID;
""",
    },
    {
            "number": 18,
            "title": 'Side-by-side agent operations comparison',
            "problem": 'compare true agent assets and meeting places directly against their shifted deceptive counterparts.',
            "techniques": 'JOIN, CTEs, Window functions (LEAD, LAG)',
            "param": None,
            "sql": """
    WITH true_ops AS (
        SELECT 
            ag.AgentID,
            ag.AgentName,
            ag.AgentAssets,
            a.AssetWays_of_Contact AS AgentWays_of_Contact,
            ag.AgentAgency
        FROM Agent ag
        LEFT JOIN Asset a ON ag.AgentAssets = a.AssetID
    ),
    false_ops AS (
        SELECT 
            ag.AgentID,
            LEAD(ag.AgentAssets, 1, ag.AgentAssets) OVER (ORDER BY ag.AgentID) AS False_AgentAssets,
            LAG(a.AssetWays_of_Contact, 1, a.AssetWays_of_Contact) OVER (ORDER BY ag.AgentID) AS False_AgentWays_of_Contact
        FROM Agent ag
        LEFT JOIN Asset a ON ag.AgentAssets = a.AssetID
    )
    SELECT 
        t.AgentID,
        t.AgentName,
        t.AgentAssets AS True_Asset,
        t.AgentWays_of_Contact AS True_MeetingPlace,
        f.False_AgentAssets AS False_Asset,
        f.False_AgentWays_of_Contact AS False_MeetingPlace,
        t.AgentAgency
    FROM true_ops t
    JOIN false_ops f ON t.AgentID = f.AgentID
    ORDER BY t.AgentID;
    """,
        },
        {
            "number": 19,
            "title": 'Randomized Agent-Asset ID Shuffling',
            "problem": 'independently randomize agents and assets using cryptographic salts to compare randomized asset IDs against true assigned asset IDs.',
            "techniques": 'WITH (CTE), ROW_NUMBER(), SHA2(), CONCAT(), JOIN',
            "param": None,
            "sql": """
            WITH ShuffledAgents AS (
                SELECT 
                    AgentID,
                    AgentName,
                    AgentAssets AS True_AssetID,
                    -- Independently randomize agents using a unique salt
                    ROW_NUMBER() OVER (ORDER BY SHA2(CONCAT(AgentID, 'agent_shuffle_salt'), 256)) AS r_agent
                FROM Agent
            ),
            ShuffledAssets AS (
                SELECT 
                    AssetID,
                    -- Independently randomize assets using a different salt
                    ROW_NUMBER() OVER (ORDER BY SHA2(CONCAT(AssetID, 'asset_shuffle_salt'), 256)) AS r_asset
                FROM Asset
            )
            SELECT 
                sa.AgentName,
                ast_shuffled.AssetID AS Randomized_Asset_ID,  -- True randomized shuffle ID (no fixed shift)
                sa.True_AssetID AS True_Asset_ID              -- What the true asset ID really is
            FROM ShuffledAgents sa
            -- Pair the independently shuffled lists together by their random row numbers
            JOIN ShuffledAssets ast_shuffled ON sa.r_agent = ast_shuffled.r_asset;
            """,
        },
        {
        "number": 20,
        "title": 'Mission Debriefing',
        "problem": 'display a final closing banner for the operational briefing.',
        "techniques": 'SELECT, UNION ALL, String literals',
        "param": None,
        "sql": """
        SELECT '          ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗██╗' AS `MISSION COMPLETE`
        UNION ALL SELECT '╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║██║'
        UNION ALL SELECT '   ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║██║'
        UNION ALL SELECT '   ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║╚═╝'
        UNION ALL SELECT '   ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝██╗'
        UNION ALL SELECT '   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚═╝';
        """,
            },
]

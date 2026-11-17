# Normalization Summary

**Global Asset Management**: Taseen Iqtider, Jose Avila, Austin Taylor

This section checks each table in `global_asset_site/setup.sql` against First, Second and Third Normal Form, explains why it passes, and records the design trade-offs we made on purpose.

## The rules we checked

| Form | Rule | What it prevents |
|---|---|---|
| **1NF** | Every column holds one atomic value. No repeating groups. Every table has a primary key. | Lists packed into a cell, which can't be searched or joined cleanly. |
| **2NF** | 1NF, and every non-key column depends on the *whole* primary key. | Partial dependencies in tables with composite keys. |
| **3NF** | 2NF, and no non-key column depends on another non-key column (no transitive dependencies). | The same fact being stored many times and drifting out of sync. |

## Functional dependencies, table by table

Every table has a single-column primary key, so **no partial dependency is possible, and every table that is in 1NF is automatically in 2NF**. The real work is 1NF and 3NF.

| Table | Primary key | Functional dependencies | 1NF | 2NF | 3NF |
|---|---|---|---|---|---|
| `Region` | `RegionName` | RegionName → Water_Access, Air_access, Land_access, Accessibility | ✅ | ✅ | ✅ |
| `country` | `CountryName` | CountryName → CountryRegion, CountryAgencies | ✅ | ✅ | ✅ |
| `Ways_of_Contact` | `DesignatedPlace` | DesignatedPlace → Secure_Droppoff, Telecommunication, Visual_Confirmation | ✅ | ✅ | ✅ |
| `Agency` | `AgencyName` | AgencyName → AgencyCountries, Contact_Place, Allies, Adversaries | ✅ | ✅ | ✅ |
| `Asset` | `AssetID` | AssetID → AssetName, AssetCountry, AssetWays_of_Contact, AssetValue, AssetConnection | ✅ | ✅ | ✅ |
| `Agent` | `AgentID` | AgentID → AgentName, AgentAssets, AgentWays_of_Contact, AgentAgency | ✅ | ✅ | ✅ |
| `Assignment_Log` | `LogID` | LogID → AgentID, OldAssetID, NewAssetID, ChangedAt | ✅ | ✅ | ✅ |

### Why each table is in 3NF

- **Region**: `Accessibility` might look like it's computed from the three access flags, but it isn't. Asia has water, air and land access and is still *Restricted*. Accessibility is an independent fact about the region, so there's no transitive dependency.
- **country**: The region's details (accessibility, access routes) are **not** copied into `country`. Only the foreign key `CountryRegion` is stored, and the rest is reached by a join. This is the classic 3NF decomposition.
- **Ways_of_Contact**: The drop-off, telecom method and recognition signal all describe the meeting place itself and nothing else.
- **Agency**: The home country and contact place are stored as foreign keys, not as copies of the country's region or the place's signal. `Allies` and `Adversaries` each hold a single agency name (see note 1).
- **Asset**: Country and meeting place are foreign keys. The asset's region is *not* stored on the asset. It comes from `Asset → country → Region`, which avoids the transitive dependency AssetID → AssetCountry → CountryRegion.
- **Agent**: The agent's agency and asset are foreign keys. The agency's home country and the asset's details are not repeated on the agent.
  - `AgentWays_of_Contact` is **not** derived from the asset's meeting place. Agent 1 (John Smith) uses the *Safe House*, while his asset Victor meets at the *Park Bench*. They are different facts: the handler's own base vs. where the asset is met.
- **Assignment_Log**: An append-only audit table. Each row is one event written by the `trg_agent_reassign` trigger.

## How we got here (decomposition)

The proposal started from one wide "operations" record: agent, agency, asset, country, region, accessibility, meeting place and recognition signal on the same row. That single table has these dependencies:

```
AgentID → AgentName, AgentAgency, AgentAssets
AgentAssets (AssetID) → AssetName, AssetCountry, AssetValue, AssetWays_of_Contact
AssetCountry → CountryRegion
CountryRegion → Accessibility, Water/Air/Land access
AssetWays_of_Contact → Visual_Confirmation, Secure_Droppoff, Telecommunication
```

Every arrow after the first is a transitive dependency. Region details would repeat on every row for that region, and a recognition signal would repeat for every asset using that place. Changing Asia's accessibility would mean editing many rows (an update anomaly).

We split the record along each dependency, giving `Agent`, `Asset`, `country`, `Region`, `Ways_of_Contact` and `Agency`, connected by foreign keys. The wide record still exists for reading, but only as the **view** `v_operations`, which rebuilds it with joins. The view stores nothing, so it can't create anomalies.

## Design notes and known trade-offs

1. **Allies / Adversaries hold one agency each.** The Milestone 2 data dictionary described them as comma-delimited lists. A list in one cell would break 1NF. In the implemented data each holds exactly one value, so the table is in 1NF. To let an agency have several allies, the correct design is a junction table:
   `Agency_Relation(AgencyName FK, OtherAgency FK, RelationType)`, with primary key `(AgencyName, OtherAgency)`.
2. **`country.CountryAgencies` overlaps with `Agency.AgencyCountries`.** Both record which agency belongs to which country, from opposite directions. This isn't a 3NF violation, since each column depends only on its own table's key. It is still redundancy *between* tables: if one side changes, the other must be updated too. A fully normalized design would drop `CountryAgencies` and find a country's agencies with `SELECT AgencyName FROM Agency WHERE AgencyCountries = ?`. We kept it because query 12 ("No local agency") reads it directly.
3. **One asset per agent, one handler per asset.** `Agent.AgentAssets` is a single foreign key, so an agent handles one asset. The stored procedure `sp_assign_asset` refuses to give an asset to a second agent. Supporting many assets per agent would need an `Agent_Asset(AgentID, AssetID)` junction table.
4. **Referential integrity.** All eight relationships are enforced with foreign keys, including `Asset.AssetCountry → country`, which was added in the final version. `Assignment_Log` deliberately has no foreign keys, so the audit history survives even if an agent or asset is later deleted.
5. **Domain rule.** `AssetValue` is limited to High / Medium / Low by the trigger `trg_asset_value_check`. This keeps the data clean without needing a separate lookup table.

## Conclusion

All seven tables satisfy **1NF, 2NF and 3NF**. Every non-key attribute depends on the key, the whole key, and nothing but the key. Region, country and meeting-place details are stored once and reached through foreign keys. The combined operational picture is produced on demand by the `v_operations` view. The remaining redundancy (`CountryAgencies`) and the single-valued `Allies`/`Adversaries` columns are documented design choices, and we've described the junction-table change that would remove them.

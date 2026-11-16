**Creating the View for the Original Table (Agent):**



CREATE VIEW true\_agent\_operations AS

SELECT 

&#x20;   AgentID,

&#x20;   AgentName,

&#x20;   AgentAssets,

&#x20;   AgentWays\_of\_Contact,

&#x20;   AgentAgency

FROM Agent;



**Create False Table Using Lead and Lag:**



CREATE VIEW false\_agent\_operations\_shifted AS

SELECT 

&#x20;   AgentID,

&#x20;   AgentName,

&#x20;   -- Shift the Asset ID down by 1 row

&#x20;   LEAD(AgentAssets, 1, AgentAssets) OVER (ORDER BY AgentID) AS False\_AgentAssets,

&#x20;   -- Shift the Ways of Contact up by 1 row

&#x20;   LAG(AgentWays\_of\_Contact, 1, AgentWays\_of\_Contact) OVER (ORDER BY AgentID) AS False\_AgentWays\_of\_Contact,

&#x20;   AgentAgency

FROM Agent;



**View the original table alongside the fake**:



SELECT \* FROM true\_agent\_operations;

SELECT \* FROM false\_agent\_operations\_shifted;




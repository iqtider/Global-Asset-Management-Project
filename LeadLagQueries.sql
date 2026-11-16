
#Creating the View for the Original Table (Agent):

CREATE VIEW true_agent_operations AS
SELECT 
    AgentID,
    AgentName,
    AgentAssets,
    AgentWays_of_Contact,
    AgentAgency
FROM Agent;

#Create False Table Using Lead and Lag:
#Lead and lag is a bit simpler, lag will look at data in a previous row related to the data in the current row
#For instance, the asset of the agent above the current agent you are looking at. If Dave manages Sarah in row 2
#Geoffrey will be looking at Sarah when running lag from row 3. When in row 1, there is no data above it so the 
#data that you are looking at is, "null". Lead is practically the same, looking forward in the same way we were looking
#Backwards, in terms of our table, we will do a simple shift where we move each asset up. This creates a problem however,
#which is the fact that we now have our 10th agent with the same asset as our 9th. We can solve this randomization and
#hashing using SHA2.

CREATE VIEW false_agent_operations_shifted AS
SELECT 
    AgentID,
    AgentName,
    #Shift the Asset ID down by 1 row
    LEAD(AgentAssets, 1, AgentAssets) OVER (ORDER BY AgentID) AS False_AgentAssets,
    #Shift the Ways of Contact up by 1 row
    LAG(AgentWays_of_Contact, 1, AgentWays_of_Contact) OVER (ORDER BY AgentID) AS False_AgentWays_of_Contact,
    AgentAgency
FROM Agent;

#View the original table alongside the fake (only needs name changed to whatever the name of the view is):

SELECT * FROM true_agent_operations;
SELECT * FROM false_agent_operations_shifted;

SELECT 
    f.AgentName, 
    ast.AssetName AS False_AssetName
FROM false_agent_operations_random f
JOIN Asset ast ON f.False_AgentAssets = ast.AssetID;


#Randomize the table instead of using Lead / Lag
#The benefit of this is the fact that it will not give you Dual Agents as shown with lead and lag alone
#The SHA2 is a built in crpyto hashing function which calculates the checksum which is a small piece of the 
#digital data from the file, message, etc. This can be used against data that has already been through the hashing
#process to ensure that it has not been corrupted by finding that specific checksum. Even if a single bit changes, 
#It will effect the whole file and change the checksum. 
WITH ShuffledAgents AS (
    SELECT 
        AgentID,
        AgentName,
        AgentAssets AS True_AssetID,
        #Independently randomize agents using a unique salt
        ROW_NUMBER() OVER (ORDER BY SHA2(CONCAT(AgentID, 'agent_shuffle_salt'), 256)) AS r_agent
    FROM Agent
),
ShuffledAssets AS (
    SELECT 
        AssetID,
        AssetName,
        #Independently randomize assets using a different salt
        ROW_NUMBER() OVER (ORDER BY SHA2(CONCAT(AssetID, 'asset_shuffle_salt'), 256)) AS r_asset
    FROM Asset
)
SELECT 
    sa.AgentName,
    ast_shuffled.AssetName AS Randomized_Asset_Name,  #True randomized shuffle (no fixed shift)
    ast_true.AssetName AS True_Asset_Name             #What the data really is
FROM ShuffledAgents sa
#Pair the independently shuffled lists together by their random row numbers
JOIN ShuffledAssets ast_shuffled ON sa.r_agent = ast_shuffled.r_asset
#Bring in the true asset name for side-by-side comparison
JOIN Asset ast_true ON sa.True_AssetID = ast_true.AssetID;
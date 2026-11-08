-- One-file setup for the website: tables, sample data, view, function, procedure and triggers.
-- Run it in MySQL Workbench (File > Run SQL Script) or: mysql -u root -p < setup.sql
-- WARNING: it drops and recreates the global_asset database.

-- Your create_tables.sql. Only change: 'references Country(' -> 'references country(' (line 38),
-- because MySQL on Linux treats table names as case-sensitive and the original fails there (Windows is fine).
DROP DATABASE IF EXISTS global_asset;
CREATE DATABASE global_asset;

 
use global_asset;

 
#---Regions---
create table Region(
    Water_Access varchar(5),
    Air_access varchar(5),
    Land_access varchar(5),
    Accessibility varchar(255),
    RegionName varchar(255) primary key
);
 
#---Country---
create table country(
    CountryName varchar(255) primary key,
    CountryRegion varchar(255),
    CountryAgencies varchar(255),
    foreign key (CountryRegion) references Region(RegionName)
);
 
#---Ways_of_Contact---
create table Ways_of_Contact(
    DesignatedPlace varchar(255) primary key,
    Secure_Droppoff varchar(255),
    Telecommunication varchar(255),
    Visual_Confirmation varchar(255)
    );
 
#---Agency---
create table Agency(
    AgencyName varchar(255) primary key,
    AgencyCountries varchar(255),
    Contact_Place varchar(50),
    Allies varchar(255),
    Adversaries varchar(255),
    foreign key (AgencyCountries) references country(CountryName),
    foreign key (Contact_Place) references Ways_of_Contact(DesignatedPlace)
    );
 
#---Asset---
create table Asset(
    AssetID int primary key,
    AssetName varchar(255) not null,
    AssetCountry varchar(255),
    AssetWays_of_Contact varchar(50),
    AssetValue varchar(50),
    AssetConnection varchar(255),
    foreign key (AssetWays_of_Contact) references Ways_of_Contact(DesignatedPlace)
);    
 
#---Agent---
create table Agent(
    AgentID int primary key,
    AgentName varchar(255) not null,
    AgentAssets int,
    AgentWays_of_Contact varchar(50),
    AgentAgency varchar(255),
    foreign key (AgentAgency) references Agency(AgencyName),
    foreign key (AgentWays_of_Contact) references Ways_of_Contact(DesignatedPlace),
    foreign key (AgentAssets) references Asset(AssetID)
);
 
#region
INSERT INTO Region (Water_Access, Air_access, Land_access, Accessibility, RegionName) VALUES
('Yes', 'Yes', 'Yes', 'Open',       'North America'),
('Yes', 'Yes', 'Yes', 'Open',       'Europe'),
('Yes', 'Yes', 'Yes', 'Restricted', 'Asia'),
('No',  'Yes', 'Yes', 'Restricted', 'Middle East'),
('Yes', 'Yes', 'Yes', 'Moderate',   'Africa');
 
#country
INSERT INTO country (CountryName, CountryRegion, CountryAgencies) VALUES
('USA',     'North America', 'CIA'),
('UK',      'Europe',        'MI6'),
('Germany', 'Europe',        NULL),
('Russia',  'Europe',        'FSB'),
('China',   'Asia',          'MSS'),
('Iran',    'Middle East',   NULL),
('France',  'Europe',        'DGSE'),
('Israel',  'Middle East',   'Mossad'),
('Egypt',   'Africa',        NULL),
('Japan',   'Asia',          NULL);
 
#ways_of_contact 
INSERT INTO Ways_of_Contact (DesignatedPlace, Secure_Droppoff, Telecommunication, Visual_Confirmation) VALUES
('Park Bench',    'Hollow tree',      'Burner phone',        'Red scarf'),
('Safe House',    'Locked cabinet',   'Encrypted email',     'Passphrase'),
('Cafe',          'Under table',      'Encrypted messaging', 'Newspaper'),
('Train Station', 'Locker 42',        'Burner phone',        'Blue umbrella'),
('Embassy Annex', 'Diplomatic pouch', 'Secure line',         'Badge check'),
('Hotel Lobby',   'Room safe',        'Secure line',         'Folded map'),
('Library',       'Book return slot', 'Encrypted messaging', 'Yellow folder');
 
#agency
INSERT INTO Agency (AgencyName, AgencyCountries, Contact_Place, Allies, Adversaries) VALUES
('CIA',    'USA',    'Safe House',    'MI6', 'FSB'),
('MI6',    'UK',     'Embassy Annex', 'CIA', 'FSB'),
('FSB',    'Russia', 'Park Bench',    'MSS', 'CIA'),
('MSS',    'China',  'Cafe',          'FSB', 'CIA'),
('DGSE',   'France', 'Hotel Lobby',   'MI6', 'FSB'),
('Mossad', 'Israel', 'Library',       'CIA', 'MSS');
 
#asset
INSERT INTO Asset (AssetID, AssetName, AssetCountry, AssetWays_of_Contact, AssetValue, AssetConnection) VALUES
(1,  'Victor', 'Russia',  'Park Bench',    'High',   'Government contact'),
(2,  'Ellen',  'Germany', 'Cafe',          'Medium', 'Embassy staff'),
(3,  'Faith',  'Iran',    'Train Station', 'High',   'Nuclear technician'),
(4,  'May',    'China',   'Cafe',          'High',   'Telecom engineer'),
(5,  'Daniel', 'USA',     'Park Bench',    'Medium', 'Defense contractor'),
(6,  'Claire', 'UK',      'Train Station', 'Low',    'Civil servant'),
(7,  'Kevin',  'Egypt',   'Hotel Lobby',   'High',   'Military officer'),
(8,  'Harry',  'Japan',   'Library',       'Low',    'Business executive'),
(9,  'Sam',    'Russia',  'Cafe',          'Medium', 'Bank clerk'),
(10, 'Lisa',   'Iran',    'Library',       'High',   'University professor');
 
#agent 
INSERT INTO Agent (AgentID, AgentName, AgentAssets, AgentWays_of_Contact, AgentAgency) VALUES
(1,  'John Smith',     1,  'Safe House',     'CIA'),
(2,  'Mary Allen',     3,  'Train Station',  'CIA'),
(3,  'James Whitby',   2,  'Embassy Annex',  'MI6'),
(4,  'Olivia Hart',    4,  'Cafe',           'MI6'),
(5,  'Evan Peters',    5,  'Park Bench',     'FSB'),
(6,  'Will Chambers',  6,  'Cafe',           'MSS'),
(7,  'Chris Davis',    7,  'Hotel Lobby',    'DGSE'),
(8,  'Rachel Cohen',   10, 'Library',        'Mossad'),
(9,  'Tom Becker',     9,  'Cafe',           'CIA'),
(10, 'Amy Tanner',     8,  'Train Station',  'MI6');

-- One row per asset: where it is, how valuable, who handles it, and how to make contact
CREATE OR REPLACE VIEW v_operations AS
SELECT a.AssetID, a.AssetName, a.AssetValue, a.AssetConnection,
       a.AssetCountry, c.CountryRegion, r.Accessibility,
       ag.AgentName AS Handler, ag.AgentAgency AS Agency,
       a.AssetWays_of_Contact AS MeetingPlace, w.Visual_Confirmation AS RecognitionSignal
FROM Asset a
JOIN country c              ON a.AssetCountry = c.CountryName
JOIN Region r               ON c.CountryRegion = r.RegionName
LEFT JOIN Agent ag          ON ag.AgentAssets = a.AssetID
LEFT JOIN Ways_of_Contact w ON a.AssetWays_of_Contact = w.DesignatedPlace;



DROP FUNCTION IF EXISTS fn_asset_risk;
DROP PROCEDURE IF EXISTS sp_assign_asset;

DELIMITER //

-- Function: rates an asset's risk from its value and how restricted its region is
CREATE FUNCTION fn_asset_risk(p_asset_id INT)
RETURNS VARCHAR(10)
READS SQL DATA
BEGIN
    DECLARE v_value VARCHAR(50);
    DECLARE v_access VARCHAR(255);

    SELECT a.AssetValue, r.Accessibility INTO v_value, v_access
    FROM Asset a
    JOIN country c ON a.AssetCountry = c.CountryName
    JOIN Region r  ON c.CountryRegion = r.RegionName
    WHERE a.AssetID = p_asset_id;

    RETURN CASE
        WHEN v_value IS NULL                                  THEN 'Unknown'
        WHEN v_value = 'High' AND v_access = 'Restricted'     THEN 'Critical'
        WHEN v_value = 'High' OR  v_access = 'Restricted'     THEN 'Elevated'
        ELSE 'Routine'
    END;
END //

-- Procedure: hands an asset to an agent, refusing if the asset is already handled
CREATE PROCEDURE sp_assign_asset(IN p_agent_id INT, IN p_asset_id INT)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Agent WHERE AgentID = p_agent_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Agent does not exist';
    ELSEIF NOT EXISTS (SELECT 1 FROM Asset WHERE AssetID = p_asset_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Asset does not exist';
    ELSEIF EXISTS (SELECT 1 FROM Agent WHERE AgentAssets = p_asset_id AND AgentID <> p_agent_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Asset already has a handler';
    ELSE
        UPDATE Agent SET AgentAssets = p_asset_id WHERE AgentID = p_agent_id;
    END IF;
END //

DELIMITER ;



-- Audit table the trigger writes to
CREATE TABLE IF NOT EXISTS Assignment_Log (
    LogID      INT AUTO_INCREMENT PRIMARY KEY,
    AgentID    INT,
    OldAssetID INT,
    NewAssetID INT,
    ChangedAt  DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TRIGGER IF EXISTS trg_agent_reassign;
DROP TRIGGER IF EXISTS trg_asset_value_check;

DELIMITER //

-- Trigger 1: log every change to which asset an agent handles
CREATE TRIGGER trg_agent_reassign
AFTER UPDATE ON Agent
FOR EACH ROW
BEGIN
    IF NOT (OLD.AgentAssets <=> NEW.AgentAssets) THEN
        INSERT INTO Assignment_Log (AgentID, OldAssetID, NewAssetID)
        VALUES (NEW.AgentID, OLD.AgentAssets, NEW.AgentAssets);
    END IF;
END //

-- Trigger 2: only allow AssetValue to be High, Medium or Low
CREATE TRIGGER trg_asset_value_check
BEFORE INSERT ON Asset
FOR EACH ROW
BEGIN
    IF NEW.AssetValue NOT IN ('High', 'Medium', 'Low') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'AssetValue must be High, Medium or Low';
    END IF;
END //

DELIMITER ;


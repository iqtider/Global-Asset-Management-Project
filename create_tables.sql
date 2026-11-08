
 
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
    foreign key (AgencyCountries) references Country(CountryName),
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
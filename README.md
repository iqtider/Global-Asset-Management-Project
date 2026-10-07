# Global Asset Management

> A database management project exploring the organization, relationships,
> querying, and controlled retrieval of fictional intelligence data.

### Project Status
`PROPOSAL / DESIGN PHASE`

This project is currently under development. The database structure,
entities, relationships, queries, and access concepts described here
represent our current design direction and may change as the project evolves.

---

## Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [Our Approach](#our-approach)
- [Current Database Model](#current-database-model)
- [Proposed Entities](#proposed-entities)
- [Query Design](#query-design)
- [Data Access Concept](#data-access-concept)
- [ER Diagram](#er-diagram)
- [Documentation Status](#documentation-status)

---

## Overview

Global Asset Management is a database management project designed around
the organization and retrieval of fictional intelligence information.

The system explores relationships between intelligence agencies, agents,
assets, countries, geographic regions, and methods of communication.

A major focus of the project is the use of relational database design and
SQL queries to organize connected information while controlling how the
intended relationships between records are retrieved.

---

## The Problem

Intelligence organizations may need to manage interconnected information
involving agents, assets, agencies, locations, and communication methods.

Within our project scenario, this information is considered highly
sensitive. The database therefore explores how this information can be
organized while limiting straightforward access to the intended
relationships between records.

The project uses this scenario to explore relational database design,
structured data organization, and SQL-based information retrieval.

---

## Our Approach

Our current design explores a database where the visible arrangement of
data may not always directly represent the intended relationships between
records.

Instead, specific SQL queries and knowledge of how the information is
organized may be required to retrieve the intended relationships.

The project currently focuses on two major areas:

### Database Organization

Designing related entities that represent agents, assets, agencies,
countries, regions, and communication methods.

### Information Retrieval

Using SQL queries, known patterns, and relationships between tables to
retrieve and interpret the intended information.

> This approach is still being developed and may change as the database
> design is revised.

---

## Current Database Model

The current proposal contains six primary entity areas:

| Entity | Current Purpose |
|---|---|
| `Agency` | Represents an intelligence organization |
| `Agent` | Represents personnel associated with an agency |
| `Asset` | Represents a source or individual associated with an agent |
| `Country` | Stores country-level information |
| `Regions` | Represents geographic regions and accessibility information |
| `Ways_of_Contact` | Represents possible methods of communication |

The entities, attributes, and relationships shown here represent the
current proposal and are subject to revision.

---

## Proposed Entities

<details>
<summary><strong>Agency</strong></summary>

Current proposed attributes and relationships:

- Name
- Agents
- Countries
- Ways of Contact
- Allies
- Adversaries

</details>

<details>
<summary><strong>Agent</strong></summary>

Current proposed attributes and relationships:

- Name
- Agent ID
- Assets
- Ways of Contact
- Agency

</details>

<details>
<summary><strong>Asset</strong></summary>

Current proposed attributes and relationships:

- Asset ID
- Country
- Ways of Contact
- Value
- Connections
- Agent ID

</details>

<details>
<summary><strong>Country</strong></summary>

Current proposed attributes and relationships:

- Hostile Group
- Region Name
- Agencies

</details>

<details>
<summary><strong>Regions</strong></summary>

Current proposed attributes and relationships:

- Name
- Water Access
- Air Access
- Land Access
- Agents
- Agent ID
- Assets
- Accessibility

</details>

<details>
<summary><strong>Ways of Contact</strong></summary>

Current proposed attributes and relationships:

- Designated Place
- Secure Dropoff
- Telecommunication
- Visual Confirmation
- Asset ID

</details>

---

## Query Design

Queries are expected to be one of the main technical components of
Global Asset Management.

Based on the current proposal, the project may explore SQL techniques
including:

- Pattern matching with `LIKE`
- `OFFSET`
- `LEAD()`
- `LAG()`
- Filtering using known information
- Queries across related entities

These techniques may be used to identify patterns and retrieve intended
relationships from the database.

The exact query structure and implementation are still being developed.

<details>
<summary><strong>Why are queries important to this project?</strong></summary>

The current project concept does not rely only on directly reading
individual database records.

Queries may play a role in determining how related information is located,
combined, and interpreted.

This makes query design a central part of both the database implementation
and the project's access concept.

</details>

---

## Data Access Concept

The current proposal explores an additional access concept based on the
organization and positioning of information within the database.

Certain relationships may depend on patterns or intentional differences
between the apparent arrangement of records and their intended
relationships.

<details>
<summary><strong>How is this intended to work?</strong></summary>

A user with knowledge of the expected pattern or organization could use
the appropriate database query to retrieve the intended information.

The final method has not yet been determined and may change as the project
moves from its proposal into implementation.

</details>

<details>
<summary><strong>Is this the final security design?</strong></summary>

No.

The current proposal describes an early design concept involving patterns,
data organization, and specialized queries.

The implementation may be revised as the database schema and project
requirements become more defined.

</details>

---

## ER Diagram

The current proposal includes an initial Entity Relationship model
connecting the major parts of the database.

The current design includes relationships among:

`Agency` • `Agent` • `Asset` • `Country` • `Regions` • `Ways of Contact`

The ER model is still under development and may change as entities,
attributes, keys, and relationships are refined.

### Current ER Diagram

<!--
Once your ER diagram image is added to the repository, replace the line
below with something like:

![Global Asset Management ER Diagram](docs/er-diagram.png)
-->

`Updated ER Diagram Coming Soon`

---

## Documentation Status

**Current Stage:** `Proposal / Early Design`

This README reflects the current direction of Global Asset Management
rather than a finalized system specification.

As the project develops, this document will be updated to reflect changes
to:

- Database entities and attributes
- Entity relationships
- SQL query design
- Data access methods
- ER diagram
- Final database implementation

**Last Updated:** October 2026

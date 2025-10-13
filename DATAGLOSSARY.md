# DATA GLOSSARY

This file describes the data schema in abstract terms. For Postgres and JSON Schema instantiations of this abstract schema, see the (schemas)[schemas] directory.

## Gotchas

* Note that all tables have a `timestamp` field, which must be expressed in ISO-8601 YYYY-MM-DDThh:mm:ss.ffffff format. Timestamp datatype is accordingly VARCHAR(25).
* In earlier versions of this schema, the `person` table was referred to as the `pop_profile` table (with 'pop' referring to Persons on Probation)
* In earlier versions of this schema, a `pop_location` table was included to accommodate near-realtime reporting of tag location. This proved to be superfluous to requirements, however, and has now been dropped.


### people

 #### id 
 `INTEGER PRIMARY KEY AUTOINCREMENT`

 The prinary key. Not used elsewhere.

 #### delius_id
`VARCHAR(50) NOT NULL` 

Identifier used by the nDelius system, the chief system used for recording information about PoPs.

The actual form of this ID is unknown at time of writing (11 July 2025). Values currently in this field are purely synthetic.

#### unique_device_wearer_id
`VARCHAR(50) NOT NULL`

In Allied/MDSS datasets, PoPs are referred to as 'device wearers (possibly because of the use made of tags by other clients such as the Home Office). 

This identifier accordingly acts as a main point of entry into MDSS datasets.

#### person_id
`VARCHAR(50) NOT NULL`

The main identifier used in the database, acting as a foreign key in the `pop_location` and `pop_profile` tables.


#### given_name
`VARCHAR(50) NOT NULL`

The name chosen for or by the PoP. In western-style naming conventions, this may also be known as the 'first name', 'forename', or 'Christian name' of the PoP. 

#### family_name
`VARCHAR(50) NOT NULL`

The name inherited by the PoP from a parent, caregiver, or other ward or guardian. In western-style naming conventions this will normally be the last name.

#### alias
`VARCHAR(50)`

A familiar name, by which the PoP may prefer to be addressed. Often a shortned form of the given name. Optional.

#### toy
`BOOLEAN`

An indication of whether this record is part of the selected minimal 'toy' dataset created for exploratory and development purposes. 

Note that `toy` is indicated explicitly only in `pop_profile` records; toy `events` and `locations` are identifiable only through joining with `pop_profile`. 

### event

For more information on the event model represented in this table, see the EVENTMODEL.md document.

#### id
`INTEGER PRIMARY KEY AUTOCREMENT`

Primary key. Not used elsewhere.

#### person_id
`VARCHAR(50)`

Foreign key to the `pop_profile` table.

#### event_name
`VARCHAR(150)`

Any of the event names listed in the EVENTMODEL.md document.



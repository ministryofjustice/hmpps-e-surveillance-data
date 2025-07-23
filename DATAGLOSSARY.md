# DATA GLOSSARY

**A note on sqlite:** Data is stored in a sqlite file. Although queryable as a standard SQL database, it should be noted that sqlite's schema enforcement is quite loose.

With regard to datatypes, sqlite uses a relatively small number, mapped from more restrictive SQL constructs. For instance, VARCHAR fields are all, under the sqlite hood, of TEXT type, and character limits are accordingly not enforced. Similarly, floats and doubles are all REAL numbers.

sqlite also does not enforce key constraints by default. To enable foreign keys, the `foreign keys` pragma must be set to 'on' prior to loading the sqlite dump, like this:

``` PRAGMA foreign_keys = on; ```


## Tables

Note: the `pop` prefix refers to 'Person on Probation'

Note that all tables have a `timestamp` field, which must be expressed in ISO-8601 YYYY-MM-DDThh:mm:ss.ffffff format. Timestamp datatype is accordingly VARCHAR(25).


### pop_profile

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

An indication of whether this record is part of the selected minimal 'toy' dataset created for exploratory and development purposes. 

Note that `toy` is indicated explicitly only in `pop_profile` records; toy `events` and `locations` are identifiable only through joining with `pop_profile`. 

### pop_location

Note that more geographic information is available from source systems, including bearing, speed, GPS satellite visibility, and more. Excluded at present, as relevance has not yet been established.

#### id
`INTEGER PRIMARY KEY AUTOCREMENT`

Primary key. Not used elsewhere.

#### person_id
`VARCHAR(50)`
Foreign key to the `pop_profile` table.

#### latitude
`REAL`

Latitude of device.

#### longitude
`REAL`

Longitude of device.

#### latitude
`REAL`

Latitude of device.

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



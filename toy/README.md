# Background

This toy dataset contains records sufficient for testing basic functionality of alerts relating to:

* attempts to tamper with tagging equipment
* failure to appear at curfew
* entry into an exclusion zone

In all cases the basic mechanism is the same: a notification is sent if and only if an alerting event is logged and no cancelling event is received within a designated threshold. For more information see the [Event Model](../EVENTMODEL.md) file.

Complete specification of the tests these records support can be found in the [Test Details](TESTDETAILS.MD) document.

## Thresholds

The thresholds within which receipt of a cancelling event serves to cancel a notification have been defined as follows:

|Violation type|Threshold|
|-------|-------|
|Tamper|2 minutes|
|Curfew| 10 minutes|
|Exclusion zone| 5 minutes|

These times are arbitrary and may change in future as more live data comes onstream.

Events are sent out at a maximum rate of one per minute. Thresholds accordingly cannot be < 2 mins

## Dataset

The toy dataset contains 20 Person on Probation (POP) records and 39 events.

Of the 39 events, 13 are cancelling events and the remainder are triggering events.

Data is spit up into five minute batches - which has no effect on the 'pop_profile' table or timestamps, but must be taken into account with `event`.

### Loading the data

For schema details, see the [Data Glossary](../DATAGLOSSARY.md).

### Querying the data

The join column for the `pop_profile` and `event` tables is `person_id`. However, as `person_id` is populated by 32-digit hex values, filtering using this field is cumbersome.

The simplest (from a human perspective) way to retrieve and filter data is using the `pop_profile.alias` field, using a query of the form:

`SELECT * FROM event AS e JOIN pop_profile AS pp ON e.person_id=pp.person_id WHERE pp.alias='{alias name}';`

 

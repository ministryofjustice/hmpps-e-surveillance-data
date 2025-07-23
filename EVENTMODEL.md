# EVENT MODEL

## General event model

The fundamental point to note about the overall data model is that, taken individually, events are stateless. That is to say, although data is received in batches, this data can be treated as consisting of an event stream of immutable and atomic events, to be processed in the order of their timestamp. 

Events of interest to the notification service may generically be termed 'potential violation events'. In the general model, such an event may be said to initiate a state of potential violation that lasts until either:

1. A subsequent event indicates that the state of potential violation is at an end (effectively, that the potential violation has been 'cancelled')
2. Some threshold of significance has been passed indicating that the potential violation should now be treated as an actual violation.

Note, however, that the event vocabulary is not well-defined. There are many different event types, some with overlapping meanings. Accordingly, rules will need to be defined to deal with the broad semantics of the event typology (see **Events of Interest**, below)

A more complete [list of events](https://jubilant-adventure-g65j3om.pages.github.io/hmpps/electronic_monitoring/source_data/live/live_data_sources/) is available from the AP team. The semantics of these events is not always clear. For immediate purposes, the event typology defined below is adequate.

### Example

For instance, attempts by a Person on Probation (PoP) to remove an assigned tag in contravention of their licence terms is referred to as 'tampering', and appears in our data as an `EV_PID_STRAP_TAMPER_START` event.

However, there may be false positives here: should the wearer simply be scratching an itch, this tamper event may simply be a 'false positive'. Should the manipulation of the tag cease almost immediately, this would appear in our data as `EV_PID_STRAP_TAMPER_END`.

Should the `EV_PID_STRAP_TAMPER_END` event have a timestamp within a few seconds of `EV_PID_STRAP_TAMPER_START`, then, it seems reasonable to conclude that no malicious activity has been detected and that the original tamper detection should be ignored.

Should no `EV_PID_STRAP_TAMPER_END` event be received, however, or should it not arrive until after two or three minutes have elapsed, the potential violation should then be considered an actual violation, and be treated as such.

Some research is needed to determine what the appropriate thresholds are for the various violation events of interest to the service.

## Events of interest

### Supported scenarios

Three scenarios are of interest:

1. **Tampers**: The Person on Probation (PoP) attempts to remove his or her tag, in violation of license conditions.
2. **Curfew violations**: A zone (typically a home and/or workplace) has been defined, in which the PoP must be present within defined hours. These zones are sometimes referred to as 'inclusion' zones, because they define an area to which the PoP is confined at specified times. Curfew violations thus indicate that a PoP is __absent__ from an area in which he or she is expected to be present.
3. **Exclusion zone violations**: A zone has been defined (for example, an airport or area around a school) which the PoP is not allowed to enter. Exclusion zone violations indicate that the PoP is __present__ in an area from which he or she is expected to be absent. Unlike inclusion zones, exclusion zones are typically 24/7 restrictions: there is no point at which the offender is allowed into the exclusion zone. However, there may be some exceptions.

### Tamper events

As noted in the example above, tamper events are indicated by events of type `EV_PID_STRAP_TAMPER_START`. 

### Curfew violations

Curfew violations are indicated by the following event types.

* `EV_ZONE_INCLUSION_TU_ABSENT_AT_START_TIME`
* `EV_CURFEWED_PID_ABSENT`
* `EV_PID_ABSENT`
* `EV_PID_ABSENT_DURING`

These events are terminated by any of:

* `EV_ZONE_INCLUSION_TU_ARRIVED_DURING_TIME`
* `EV_CURFEWED_PID_ARRIVED`
* `EV_PID_ARRIVED`

In addition, there is a selection of events that do not terminate the violation, but potentially indicate its escalation:

* `EV_ZONE_INCLUSION_TU_ABSENT_AT_END_TIME`
* `EV_ZONE_INCLUSION_TU_ARRIVED_AFTER_END_TIME`
* `EV_PID_ARRIVED_AFTER_END`

The precise semantics of the above lists are currently unclear and may be subject to change.

### Exclusion zone violations

Note that while the names of these event types all imply that exclusions are time-limited, in practice most exclusion zones are in effect around the clock.

Exclusion zone violations are initiated by:

* `EV_EXCLUDED_PID_ARRIVED_DURING_EXCLUSION`
* `EV_ZONE_EXCLUSION_TU_PRESENT_AT_START_TIME`
* `EV_ZONE_EXCLUSION_TU_ARRIVED_DURING_TIME`

They are terminated by:

* `EV_EXCLUDED_PID_DEPARTED_DURING_EXCLUSION`
* `EV_ZONE_EXCLUSION_TU_DEPARTED_DURING_TIME`

As with inclusion violations, the semantics of these event types are unclear, and will need to be clarified in the course of development.

## Status checks

In addition to the codes listed above, there are numerous others that can be ignored for the purposes of the notifications service. One value worth noting, however, is `EV_PARTIAL_CALLBACK`, as this constitutes single largest category of updates. `EV_PARTIAL CALLBACK` is a routine status check to ensure the continued tag functioning.


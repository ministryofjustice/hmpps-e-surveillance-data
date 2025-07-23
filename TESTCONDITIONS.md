# TEST CONDITIONS

Right now, we do not need to / cannot distinguish particularly between different kinds of event. Regardless of whether the violation flagged is a tamper, inclusion, or exclusion event, in each case a notification generates an alert if a countermanding eveent is not received within some specified threshold time. For tamper events, the logic is very simple, as there is only one kind of event flag and one corresponding countermand. Inclusion and exclusion violations may be triggered by more than one kind of event, and countermanded by more than one kind of event. However, the underlying logic remains the same.

This means a relatively small class of generic tests covers all scenarios as currently defined (though note that improved understanding of EMS or HMPPS procedures may lead to revision or expansion of this list).

## Routine status checks do not raise an alert

* `EV_PARTIAL_CALLBACK` events do not raise an alert

## Violation events raise an alert if past threshold time

* For a list of violation events, see DATAGLOSSARY.md

## Violation events do not raise an alert if a countermand is received within threshold time

* For a list of violation countermands, see DATAGLOSSARY.md

## Violation events raises an alert if tamper event clear received past threshold time

* If the countermand is received past the threshold, this does not affect the original alert

## Multiple violations should follow the same rules as above

* The same logic given above applies even where more than one license condition is violated at the same time, for example:
    * a tamper event is received while a PoP is absent from a required inclusion zone
    * a tamper event is received while a PoP is present in an exclusion zone
    * a PoP is absent from an inclusion zone and present in an exclusion zone
    * ... and countermands for all of these produce appropriate effects
    	* countermanding a tamper event received while a PoP is late for curfew
    	* countermanding a tamper event received while a PoP remains in an exclusion zone
    	* countermanding an exclusion violation while the PoP remains late for curfew


  ### Synthetic data requirements

  Of the 20 'toy' entities: 

  * 14 should consist of 'simple' events
      * 3 should consist only of routine status alerts
      * 3 should contain 2-3 tamper events, of which 1 or 2 are subsequently cleared within threshold
      * 4 should contain curfew (inclusion) violations
          * 2 are cleared within threshold
          * 2 are not cleared within threshold
      * 4 should contain exclusion violations
          * 2 are cleared within threshold
          * 2 are not cleared within threshold
  * 6 should consist of 'complex' events
      * 1 where a tamper event occurs during a curfew violation and neither are countermanded
      * 1 where a tamper event occurs within an exclusion zone and neither event is countermanded
      * 1 where a PoP is both absent from an inclusion zone and present within an exclusin zone
      * 1 where a tamper event occurs during a curfew violation, but the tamper event is countermanded
      * 1 where a tamper event occurs within an exclusion zone, but the tamper event is countermanded
      * 1 where a PoP is both absent from an inclusion zone and present in an exclusion zone, but a countermand for the exclusion event is received


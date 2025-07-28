# Test conditions

## TEST CONDITION 1
### Routine status checks do not trigger notifications.

This is provided by 

* record 1 in the pop_profile table ("Mo") 
* record 6 in the pop_profile table ("Taz")

There are no violation events for these person records.


## TEST CONDITION 2
### Tamper events trigger notifications.

This test condition is provided by record 2 ("Cy").  A tamper event is raised and is never cancelled. 


## TEST CONDITION 3
### Tamper events trigger notifications if not cancelled within a given threshold.

We define the threshold arbitrarily here at **2 minutes**.

This test condition is provided by record 3 ("Dan"). A tamper event is raised, and only cancelled 3m later. 



## TEST CONDITION 4
### Tamper events do not trigger notifications if cancelled before the threshold is crossed.

This test condition is provided by record 4, "Raj". A tamper event is detected but is cancelled 1m later.


## COMPLEX TEST 1 (Test conditions 2 & 4)

Record 5 ("Ew") triggers three separate tamper events, only two of which are cancelled.


## TEST CONDITION 5
### Curfew absence events trigger notifications if not cancelled.

This is tested with person record 7, "Jay"


## TEST CONDITION 6
### Curfew absence events trigger notifications if not cancelled within the threshold time.

We arbitrarlly set this threshold time as **5 minutes**.

This is tested with person record 8, "Lee", with the cancelling event arriving only after 6 minutes.


## TEST CONDITION 7
### Curfew absence events do not trigger notifications if cancelled within the threshold time.

This is tested using person records 9 and 10, "Dave" and "Ami".

Note the variety of `event_names` related to curfew absence events and their cancellation.


## TEST CONDITION 8
### Exclusion violation events trigger notifications if not cancelled.

This is tested with person record 7, "B"


## TEST CONDITION 9
### Exclusion zone violations trigger notifications if not cancelled within the threshold time.

We arbitrarlly set this threshold time at **5 minutes**.

This is tested with person record 13, "AJ", with the cancelling event arriving only after 7 minutes.


## TEST CONDITION 10
### Exclusion violation events do not trigger notifications if cancelled within the threshold time.

This is tested using person records 14 and 15, "Tommy" and "J".

Note the variety of `event_names` related to exclusion zone violation events and their cancellation.


## COMPLEX TEST 2
### (Test conditions 2 & 5)

Both a tamper and a curfew violation occur, and are not cancelled.

This condition is tested by record 16, "Omz".


## COMPLEX TEST 3
### (Test conditions 2 & 8)

A tamper event and exclusion violation occur, and are not cancelled

This condition is tested by record 17, "Sam".


## COMPLEX TEST 4
### (Test conditions 5 & 8)

A curfew violation and exclusion violation occur, and are not cancelled.

This condition is tested by record 18, "Haz".


## COMPLEX TEST 5
### (Test conditions 4 & 5)

A tamper event occurs during a curfew violation, but is cancelled within the threshold time

This condition is tested by record 18, "Issy".

 
## COMPLEX TEST 6
### (Test conditions 4 & 8)

A tamper event occurs during an exclusion zone violation, but is cancelled within the threshold time

This condition is tested by record 19, "Nat".


## COMPLEX TEST 7
### (Test conditions 5 & 10)

The offender is both absent from an inclusion zone and present in an exclusion zone, 
but the exclusion violation is cancelled within the threshold time.

This condition is tested by record 11, "Kay".



# How to use this script

## Dependencies

The script uses the Faker library. `pip3 install Faker` is likely to resolve this for most users. 

## Running the script

Running the `generate_data.py` script is as simple as:

`python3 generate_data.py` on the command line.

You will then be given a series of prompts about what percentage of the data you wish to be clean (i.e., how many persons should not be associated with any events whatsoever), what percentage should be associated with tamper events, and so on. 

Note that random numbers are used to allocate events, so these percentages will not be reflected precisely in the data. The intention is purely to create a reasonably representative and comprehensive dataset for testing purposes. For this, exactness is not required.
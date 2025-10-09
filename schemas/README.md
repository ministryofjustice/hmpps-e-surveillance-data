# Using the JSON schema files

## In Python

Quick and dirty validation of CSV data against the JSON Schema files can be easily done using the Python 3 `csvmodel` library. This can be useful for testing whether the JSON Schema has been correctly specified, whether test data passes basic sanity checks, etc.

Usage in the simplest case is straightforward.

First, install the package.

`$ pip install csvmodel`

Then run `csvmodel` providing the path to the file you wish to validate, and the schema against which it should be validated. E.g.,

` $ csvmodel --json-schema=person.schema.json ../data_generation/sample/person-2025-08-05T13_10_38.8891.csv`

Further documentation can be found at the `csvmodel` [package site](https://pypi.org/project/csvmodel/).

## In JVM languages

There is no widely-used Java library for direct parsing and validation of CSV data against JSON Schema. 

In production use, then, the JSON Schema will need to be converted into a JSON object, and data parsed from CSVs or other sources validated against this.

Multiple libraries are available for use with JSON Schemas. One of the more popular is [Jackson](https://github.com/FasterXML/jackson).



# JUUL Document Analysis

## Setup
> poetry install

## Notes about libraries and data formats used
* We're using [Polars](https://docs.pola.rs/) instead of Pandas for DataFrames for its performance. 
* As a result, most intermediate files referenced in these example notebooks were recently changed to Parquet format from CSV. The JUUL documents made available through UCSF's API contain records with lists of strings, which Polars' CSV writer cannot handle as of now. Parquet provides a much more performant, compressed format.

Of course, you are welcome to use Pandas yourself if preferred. Any Polars DataFrame output from the utility functions provided here can be converted to pandas with `.to_pandas()`, but given the large size of the full dataset (> 2.4 million records), we recommend polars where possible for efficiency's sake.
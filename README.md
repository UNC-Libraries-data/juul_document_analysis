# JUUL Document Analysis

## Setup
> poetry install

## Notes about libraries and data formats used
* We're using [Polars](https://docs.pola.rs/) instead of Pandas for DataFrames for its performance. 
* As a result, most intermediate files referenced in these example notebooks were recently changed to Parquet format from CSV. The JUUL documents made available through UCSF's API contain records with lists of strings, which Polars' CSV writer cannot handle as of now. Parquet provides a much more performant, compressed format.
* Given the dataset's large size, parquet files allow us to handle complex data structures more efficiently as parquet’s columnar storage enables faster data retrieval and reduced file size.

Of course, you are welcome to use Pandas yourself if preferred. Any Polars DataFrame output from the utility functions provided here can be converted to pandas with `.to_pandas()`, but given the large size of the full dataset (> 2.4 million records), we recommend polars where possible for efficiency's sake.

To further help simplify conversions, there is a csv_to_parquet helper function available in src/util.py to convert CSV files to Parquet format.

# Text Analysis Resources for JUUL Industry Documents
Created by [University Libraries at the University of North Carolina at Chapel Hill](http://library.unc.eud/data/) in collaboration with [Industry Documents Library at University of California San Francisco](https://www.industrydocuments.ucsf.edu/). To access the Jupyter Notebooks we use for our tutorials, visit our [GitHub repository](https://github.com/UNC-Libraries-data/juul_document_analysis).

For more information about the JUUL Labs Document Collection for North Carolina, see our [libguide](https://guides.lib.unc.edu/juul).

We have also created a [Zotero library](https://www.zotero.org/groups/5395305/juul_proj_docs/library) with resources for text analysis methodology on similar collections that may serve as background reading for your text analysis project.

## Introductory Tutorials
* [How to use the Industry Documents Library API Python Wrapper](/html/JUUL_using_python_wrapper.html)
* [How to create a type-specific dataset](/html/JUUL_create_type_dataset.html)

## Working with Specific Document Types
* [Working with Emails](/)
* [Working with Spreadsheets](/)
* [Working with Documents](/)
* [Working with Audio](/)
* [Working with Audio-visual material](/html/JUUL_long_vid_transcription.html)
* [Working with Slack messages](/html/JUUL_stitching_slack_messages.html)

## Advanced Tutorials
* [Conducting a Time Series Analysis on Emails](/html/JUUL_Email_Time_Series.html)
* [Conducting Employee Network Analysis](/Jupyter/JUUL_Employee_Network_Analysis.ipynb)
* [Conducting Key word Extract and Named Entity Recognition(NER) on Emails](/html/JUUL_NER_and_keyword_extraction_Emails.html)
* [Creating a RAG Model with Email Documents](/JUUL_rag_model.ipynb)

**MORE TUTORIALS COMING SOON**

For questions about these tutorials or about conducting your own text analysis research using the JUUL Labs Documents Collection for North Carolina, please contact [Rolando Rodriguez](mailto:rolando@ad.unc.edu) 

## Notes about libraries and data formats used
* We're using [Polars](https://docs.pola.rs/) instead of Pandas for DataFrames for its performance. 
* As a result, most intermediate files referenced in these example notebooks were recently changed to Parquet format from CSV. The JUUL documents made available through UCSF's API contain records with lists of strings, which Polars' CSV writer cannot handle as of now. Parquet provides a much more performant, compressed format.
* Given the dataset's large size, parquet files allow us to handle complex data structures more efficiently as parquet’s columnar storage enables faster data retrieval and reduced file size.

Of course, you are welcome to use Pandas yourself if preferred. Any Polars DataFrame output from the utility functions provided here can be converted to pandas with `.to_pandas()`, but given the large size of the full dataset (> 2.4 million records), we recommend polars where possible for efficiency's sake.

To further help simplify conversions, there is a csv_to_parquet helper function available in src/util.py to convert CSV files to Parquet format.

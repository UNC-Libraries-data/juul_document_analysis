from zipfile import ZipFile
import polars as pl
import os

def write_db_from_zip(db_uri: str, table_name: str, filepath: str, overwrite=False) -> None:
    """Writes to a local postgres instance using a local .zip of the entire collection"""
    batch = 0
    with ZipFile(filepath, 'r') as z:
        total = len(z.filelist)
        for i, f in enumerate(z.filelist):
            try:
                print(f"Processing file {f.filename}: {i}/{total}")
                df = pl.read_csv(z.open(f).read(), separator="|")
                # Remove null characters from all String columns
                df = df.with_columns(
                        pl.all().map_elements(lambda x: x if type(x) == int else x.replace("\0", ""), return_dtype=pl.String)
                        )

                df.write_database(
                    table_name=table_name,
                    connection=db_uri,
                    if_table_exists='append' if batch > 0 else 'replace',
                    engine='adbc',
                )
                batch += 1
            except Exception as e:
                  print(f"Failed to ingest CSV file from ZIP: {f}, retrying with chunking...")
                  df = pl.read_csv(z.open(f).read(), separator="|")
                  df = df.with_columns(pl.col("ocr_text").map_elements(lambda x: x.replace("\x00", ""), return_dtype=pl.String).alias("ocr_text"))
                  for chunk in df.iter_slices(n_rows=1):
                      try:
                        chunk.write_database(
                            table_name=table_name,
                            connection=db_uri,
                            if_table_exists='append' if batch > 0 else 'replace',
                            engine='adbc'
                        )
                      except Exception as e:
                          print(e)


if __name__ == "__main__":
    db_uri = os.getenv('DB_URI')
    table_name = os.getenv('DB_TABLE')
    filepath = os.getenv('ZIP_FILEPATH')
    write_db_from_zip(db_uri=db_uri, table_name=table_name, filepath=filepath)

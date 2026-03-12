# Part 1, Session 5 - Data Wrangling

<br><br>

This is what a real-world AI application looks like:

<p align="center">
   <img src="img/iceberg.jpeg" width="40%">
</p>

### Below the waterline

- That's the **Data - lots and lots of data**
- In multiple **Formats**
- From multiple **Sources**
- Sometimes it's not pretty
- The data you need is rarely available **as-is**, it usually must first be **wrangled** into a usable format.

### Above the waterline

- The **data wrangling code** that transforms the data into a usable format
- The standard/traditional **application code** that uses the data

### The Tip of the Iceberg

- That's the AI part - models, prompts, LLMs, MCP, Agent Framework, algorithms, etc.

### So, what is Data Wrangling?

- **It's the art of transforming messy raw data into a usable formats for your needs**
- [Data Wrangling at Wikipedia](https://en.wikipedia.org/wiki/Data_wrangling)

<br><br><br>

## Common File Formats

- Text 
- CSV = Comma Separated Values
- TSV = Tab Separated Values
- JSON = JavaScript Object Notation.  Widely used, flexible-schema
- Markdown - a simple text format to produce formatted HTML.  Liked by LLMs.
- **TOON** = Newer format for AI applications
  - Compact and efficient format for LLMs
  - "Information dense", reduces LLM token consumption (we'll cover this in a later session)
  - “I didn't have time to write a short letter, so I wrote a long one instead.” - Mark Twain

<br><br><br>

## Common Data Wrangling Use-Cases

- Merging multiple data sources into a single enhanced/augmented file
- Create CSV content to load into a relational Database
  - Such as Azure PostgreSQL
  - Or a Spark dataframe
    - We'll cover dataframes in the next lesson w/Jupyter
- Create **JSON** content to load into **Azure Cosmos DB or Azure Search**
- Collect descriptive text content for creating **embeddings** for a **Vector Database** (i.e. - Semantic Search)
  - Embeddings and vector search will be covered in a later session

<br><br><br>

## Python is a GREAT programming language for data Wrangling

  - Many useful standard and third-party libraries for this
  - json and csv standard libraries.  And many more
  - [pandas](https://pandas.pydata.org) for CSV/TSV data (covered in the next lesson w/Jupyter)
  - [polars](https://pola.rs) a modern and faster implementation of dataframes
  - [duckdb](https://duckdb.org) for remote files in various formats, then read the data with SQL
    - 
    - It's **not** a database, it's a library
  - [beautifulsoup](https://beautiful-soup-4.readthedocs.io/en/latest/) for parsing HTML
  - [openpyxl](https://openpyxl.readthedocs.io/en/stable/) for Excel files
  - PDF will be covered at a later session, using Azure Document Intelligence

We'll use the **duckdb** library in this session.  It's **NOT a database**.
Rather, it's a **library** that allows you to fetch data and query it with SQL.

<br><br><br>

### Wait, what's SQL?

- SQL = Structured Query Language
- SQL is a language for querying Relational Databases
- There's an Industry Standard, called the ANSI Standard for SQL - all major relational databases support it

### Wait, what's a Relational Database?

- A database that stores the data in **tables**
  - The tables have rows and columns, much like a spreadsheet
  - The columns have strict datatypes (string, integer, float, boolean, etc.)
- The tables can be related to each other through **foreign keys (FK)**
  - For example, an Address table with a state column; state a FK to a row in the States table
- **Referential Integrity** is enforced by the database
  - For example, an address with the state of "QQ" is invalid, as there is no state with the code "QQ"

### Why should I care about SQL?

- Because it is widely used - relational databases, libraries (i.e. - duckdb), and Spark (future session)
- You will encounter SQL often in AI applications

### Pro Tip - Learn SQL with sqlite3

- sqlite3 runs on your laptop (Windows, Mac, or Linux), and it's a great way to get started with databases
- [sqlite3](https://sqlite.org)
- CSV files can be exported from Excel, and then imported into sqlite3
  - This, however, isn't covered in this series

<br><br><br>

## Excellent Public Data Sources

These are listed here for your exploration.

  - [Kaggle](https://www.kaggle.com/datasets)
  - [Hugging Face](https://huggingface.co/docs/datasets/en/index)
  - [Open Flights](https://openflights.org/data) - airports, airlines, routes
  - [IMDb](https://developer.imdb.com/non-commercial-datasets/) - movies
  - many, many, many more...

<br><br><br>

## Demonstration

This session uses file **main-wrangling.py**.

```
python main-wrangling.py help

Usage:
    Data wrangling with duckdb, polars, toon-python, etc.
    with both local and remote files.
    python main-wrangling.py <func>
    python main-wrangling.py help
    python main-wrangling.py postal_codes_nc_csv_to_json
    python main-wrangling.py center_of_nc_with_polars
    python main-wrangling.py postal_codes_nc_csv_to_toon
    python main-wrangling.py imdb
    python main-wrangling.py openflights
    python main-wrangling.py augment_openflights_airports
    python main-wrangling.py gen_pypi_download_lib_json_script
    python main-wrangling.py explore_downloaded_pypi_libs
    python main-wrangling.py create_cosmosdb_pypi_lib_documents
    python main-wrangling.py add_embeddings_to_cosmosdb_documents
    python main-wrangling.py uv_parse
    python main-wrangling.py gen_graph_data
```

Please explore **main-wrangling.py** on your own.
Only a few of its' functions will be demonstrated in the session.

### Wrangling North Carolina Postal Codes

The input data, file **data/postal_codes/postal_codes_nc.csv**.

It is fairly clean data, and it has a useful **header row** (i.e. - first row) that describes the columns.

```
id,postal_cd,country_cd,city_name,state_abbrv,latitude,longitude
10949,27006,US,Advance,NC,35.9445620000,-80.4376310000
10950,27007,US,Ararat,NC,36.3768840000,-80.5962650000
10951,27009,US,Belews Creek,NC,36.2239300000,-80.0800180000
10952,27010,US,Bethania,NC,36.1822000000,-80.3384000000
10953,27011,US,Boonville,NC,36.2091840000,-80.6937720000
10954,27012,US,Clemmons,NC,36.0040180000,-80.3714450000
10955,27013,US,Cleveland,NC,35.7634680000,-80.7037300000
10956,27014,US,Cooleemee,NC,35.8119670000,-80.5542580000
10957,27016,US,Danbury,NC,36.4445880000,-80.2165700000
...
```

The Python code to process this data:

```
def postal_codes_nc_csv_to_json():
    """
    Read a local CSV file with DuckDB.
    Then query it with SQL.
    Then transform the CSV data into a JSON file.
    """
    infile = "data/postal_codes/postal_codes_nc.csv"
    rel = duckdb.read_csv(infile)
    rel.show()
    print(rel.shape)       # Print the shape of the data (1080, 7) rows and columns
    print(str(type(rel)))  # <class 'duckdb.duckdb.DuckDBPyRelation'>

    # In this SQL, 'rel' refers to the above python variable name!  duckdb is clever that way.
    davidson = duckdb.sql("SELECT postal_cd, city_name FROM rel WHERE postal_cd = 28036")
    davidson.show()
    print(rel.df().columns.tolist())

    # Transform the CSV data into a JSON file.
    # DuckDB has some dataframe methods - df().
    outfile = "data/postal_codes/postal_codes_nc.json"
    rel.df().to_json(outfile, orient="records", lines=True)
    print(f"file written: {outfile}")
```

Note the SQL query executed above by duckdb:

```
SELECT postal_cd, city_name FROM rel WHERE postal_cd = 28036
```

The **SELECT** statement is used to query the data in the database.

#### python main-wrangling.py postal_codes_nc_csv_to_json

```
$ python main-wrangling.py postal_codes_nc_csv_to_json

┌───────┬───────────┬────────────┬──────────────┬─────────────┬───────────┬────────────┐
│  id   │ postal_cd │ country_cd │  city_name   │ state_abbrv │ latitude  │ longitude  │
│ int64 │   int64   │  varchar   │   varchar    │   varchar   │  double   │   double   │
├───────┼───────────┼────────────┼──────────────┼─────────────┼───────────┼────────────┤
│ 10949 │     27006 │ US         │ Advance      │ NC          │ 35.944562 │ -80.437631 │
│ 10950 │     27007 │ US         │ Ararat       │ NC          │ 36.376884 │ -80.596265 │
│ 10951 │     27009 │ US         │ Belews Creek │ NC          │  36.22393 │ -80.080018 │
│ 10952 │     27010 │ US         │ Bethania     │ NC          │   36.1822 │   -80.3384 │
│ 10953 │     27011 │ US         │ Boonville    │ NC          │ 36.209184 │ -80.693772 │
│ 10954 │     27012 │ US         │ Clemmons     │ NC          │ 36.004018 │ -80.371445 │
│ 10955 │     27013 │ US         │ Cleveland    │ NC          │ 35.763468 │  -80.70373 │
│ 10956 │     27014 │ US         │ Cooleemee    │ NC          │ 35.811967 │ -80.554258 │
│ 10957 │     27016 │ US         │ Danbury      │ NC          │ 36.444588 │  -80.21657 │
│ 10958 │     27017 │ US         │ Dobson       │ NC          │ 36.375294 │ -80.804534 │
│   ·   │       ·   │ ·          │   ·          │ ·           │      ·    │       ·    │
│   ·   │       ·   │ ·          │   ·          │ ·           │      ·    │       ·    │
│   ·   │       ·   │ ·          │   ·          │ ·           │      ·    │       ·    │
│ 12019 │     28814 │ US         │ Asheville    │ NC          │   35.6006 │   -82.5545 │
│ 12020 │     28815 │ US         │ Asheville    │ NC          │   35.6006 │   -82.5545 │
│ 12021 │     28816 │ US         │ Asheville    │ NC          │   35.6006 │   -82.5545 │
│ 12022 │     28901 │ US         │ Andrews      │ NC          │ 35.197799 │ -83.810292 │
│ 12023 │     28902 │ US         │ Brasstown    │ NC          │ 35.028354 │ -83.962106 │
│ 12024 │     28903 │ US         │ Culberson    │ NC          │   34.9919 │   -84.1679 │
│ 12025 │     28904 │ US         │ Hayesville   │ NC          │ 35.073862 │ -83.705197 │
│ 12026 │     28905 │ US         │ Marble       │ NC          │ 35.161114 │ -83.927575 │
│ 12027 │     28906 │ US         │ Murphy       │ NC          │ 35.139744 │ -84.103558 │
│ 12028 │     28909 │ US         │ Warne        │ NC          │ 35.011807 │ -83.918818 │
├───────┴───────────┴────────────┴──────────────┴─────────────┴───────────┴────────────┤
│ 1080 rows (20 shown)                                                       7 columns │
└──────────────────────────────────────────────────────────────────────────────────────┘

(1080, 7)
<class '_duckdb.DuckDBPyRelation'>
┌───────────┬───────────┐
│ postal_cd │ city_name │
│   int64   │  varchar  │
├───────────┼───────────┤
│     28036 │ Davidson  │
└───────────┴───────────┘
```

#### A brief comment on relative file sizes - csv vs json vs toon

The TOON format is information-dense.  Lower token utilization for LLMs.

```
$ ls -al | grep postal_codes_nc
-rw-r--r--@  1 cjoakim  staff   61273 Jan 18 14:09 postal_codes_nc.csv
-rw-r--r--@  1 cjoakim  staff  145298 Jan 31 15:48 postal_codes_nc.json
-rw-r--r--@  1 cjoakim  staff   53583 Jan 31 15:49 postal_codes_nc.toon
```

### Find the Geographic Center of North Carolina with Polars 

```
def center_of_nc_with_polars():
    # Read the CSV file into a Polars dataframe (df)
    df = pl.read_csv("data/postal_codes/postal_codes_nc.csv")
    
    # Explore the dataframe (EDA)
    print(df.head())
    print(df.tail())
    print(df.describe())
    print(df.dtypes)
    print(df.columns)
    print(df.shape)

    # Calculate the center of the state (average of the latitude and longitude)
    avg_lat = df.select(pl.col("latitude").mean()).item()
    avg_lon = df.select(pl.col("longitude").mean()).item()
    print(f"North Carolina center (avg of postal codes): latitude={avg_lat:.6f}, longitude={avg_lon:.6f}")
```

#### python main-wrangling.py center_of_nc_with_polars

```
...
North Carolina center (avg of postal codes): latitude=35.573456, longitude=-79.545256
```

<br><br><br>

### Wrangling IMDb Data

Very large TSV file dataset with Movies, Ratings, Actors, Directors, etc.

- See https://developer.imdb.com/non-commercial-datasets/
- name.basics.tsv.gz
- title.akas.tsv.gz
- title.basics.tsv.gz
- title.crew.tsv.gz
- title.episode.tsv.gz
- title.principals.tsv.gz
- title.ratings.tsv.gz

This is all the code we need to read the names g-zipped dataset.
This is also a clean dataset with a useful header row.

```
def imdb():
    data = duckdb.read_csv("https://datasets.imdbws.com/name.basics.tsv.gz")
    data.show()
    print(data.shape)  # (15056031, 6) <-- 15-million+ rows!
```

#### python main-wrangling.py imdb

```
python main-wrangling.py imdb
┌───────────┬──────────────────────┬───────────┬───────────┬──────────────────────┬──────────────────────────┐
│  nconst   │     primaryName      │ birthYear │ deathYear │  primaryProfession   │      knownForTitles      │
│  varchar  │       varchar        │  varchar  │  varchar  │       varchar        │         varchar          │
├───────────┼──────────────────────┼───────────┼───────────┼──────────────────────┼──────────────────────────┤
│ nm0000001 │ Fred Astaire         │ 1899      │ 1987      │ actor,miscellaneou…  │ tt0072308,tt0050419,tt…  │
│ nm0000002 │ Lauren Bacall        │ 1924      │ 2014      │ actress,miscellane…  │ tt0037382,tt0075213,tt…  │
│ nm0000003 │ Brigitte Bardot      │ 1934      │ 2025      │ actress,music_depa…  │ tt0057345,tt0049189,tt…  │
│ nm0000004 │ John Belushi         │ 1949      │ 1982      │ actor,writer,music…  │ tt0072562,tt0077975,tt…  │
│ nm0000005 │ Ingmar Bergman       │ 1918      │ 2007      │ writer,director,ac…  │ tt0050986,tt0069467,tt…  │
│ nm0000006 │ Ingrid Bergman       │ 1915      │ 1982      │ actress,producer,s…  │ tt0034583,tt0038109,tt…  │
│ nm0000007 │ Humphrey Bogart      │ 1899      │ 1957      │ actor,producer,mis…  │ tt0034583,tt0043265,tt…  │
│ nm0000008 │ Marlon Brando        │ 1924      │ 2004      │ actor,director,wri…  │ tt0078788,tt0068646,tt…  │
│ nm0000009 │ Richard Burton       │ 1925      │ 1984      │ actor,producer,dir…  │ tt0061184,tt0087803,tt…  │
│ nm0000010 │ James Cagney         │ 1899      │ 1986      │ actor,director,pro…  │ tt0029870,tt0031867,tt…  │
│     ·     │      ·               │ ·         │ ·         │          ·           │            ·             │
│     ·     │      ·               │ ·         │ ·         │          ·           │            ·             │
│     ·     │      ·               │ ·         │ ·         │          ·           │            ·             │
│ nm0010173 │ Carmen Acosta Iraola │ \N        │ \N        │ costume_department…  │ tt0260772,tt0305205,tt…  │
│ nm0010174 │ Casimiro Acosta      │ \N        │ \N        │ transportation_dep…  │ tt0094768,tt0107582,tt…  │
│ nm0010175 │ Cayetano Acosta      │ \N        │ \N        │ actor                │ tt0106307                │
│ nm0010176 │ Cesar Acosta         │ \N        │ \N        │ actor                │ tt0125931                │
│ nm0010177 │ Charles Acosta       │ \N        │ \N        │ producer             │ tt0259497,tt27558199,t…  │
│ nm0010178 │ Christina Acosta     │ \N        │ \N        │ \N                   │ \N                       │
│ nm0010179 │ Danny Acosta         │ \N        │ \N        │ director,writer,ed…  │ tt0136998                │
│ nm0010180 │ David Acosta         │ \N        │ \N        │ actor                │ tt0119832,tt2387618,tt…  │
│ nm0010181 │ Dennis Acosta        │ \N        │ \N        │ actor                │ tt0209441                │
│ nm0010182 │ Eleuterio Acosta     │ \N        │ \N        │ actor                │ tt0145293                │
├───────────┴──────────────────────┴───────────┴───────────┴──────────────────────┴──────────────────────────┤
│ ? rows (>9999 rows, 20 shown)                                                                    6 columns │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

(15056031, 6)
```

<br><br><br>

### Wrangling the OpenFlights Data 

This public dataset is from the OpenFlights project.
It contains airports, airlines, routes, planes, and countries.
It's not very clean, however, as it has no header rows, some of the columns
are null, and there are multiple character sets.

See the **openflights()** method of **main-wrangling.py**

<br><br><br>

### Augmenting the OpenFlights Data with Address information

This is derived from the latitude and longitude of the airports with the **geopy** library.

See the **augment_openflights_airports()** method of **main-wrangling.py**

<br><br><br>

## Links

- [duckdb](https://pypi.org/project/duckdb/)
- [polars](https://pola.rs)
- [geopy](https://geopy.readthedocs.io/en/stable/)
- [toon](https://toonformat.dev)
- [ANSI Standard for SQL](https://blog.ansi.org/ansi/sql-standard-iso-iec-9075-2023-ansi-x3-135/)
- [sqlite3](https://sqlite.org)

<br><br><br>
---
<br><br><br>

[Home](../README.md)

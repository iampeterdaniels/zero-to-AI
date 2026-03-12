"""
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
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, 3Cloud/Cognizant, 2026

import asyncio
import json
import logging
import sys
import os
import time
import traceback
import uuid

from typing import Any

import duckdb

import polars as pl

from docopt import docopt
from dotenv import load_dotenv

from geopy.geocoders import Nominatim

from toon import encode

from src.ai.aoai_util import AOAIUtil
from src.io.fs import FS
from src.os.env import Env
from src.util.counter import Counter
from src.util.uv_parser import UVParser


def print_options():
    arguments = docopt(__doc__, version="1.0.0")
    print(arguments)


def postal_codes_nc_csv_to_json():
    """
    Read a local CSV file with DuckDB.
    Then query it with SQL.
    Then transform the CSV data into a JSON file.
    """
    infile = "data/postal_codes/postal_codes_nc.csv"
    rel = duckdb.read_csv(infile)
    rel.show()
    print(rel.shape)  # (1080, 7)
    print(str(type(rel)))  # <class 'duckdb.duckdb.DuckDBPyRelation'>

    # In this SQL, 'rel' refers to the above python variable name!  Clever.
    davidson = duckdb.sql("SELECT postal_cd, city_name FROM rel WHERE postal_cd = 28036")
    davidson.show()
    print(rel.df().columns.tolist())

    # Transform the CSV data into a JSON file.
    # DuckDB has some dataframe methods - df().
    outfile = "data/postal_codes/postal_codes_nc.json"
    rel.df().to_json(outfile, orient="records", lines=True)
    print(f"file written: {outfile}")


"""
Prompt to Cursor:
Complete the 'center_of_nc_with_polars' method using Polars.
Calculate the average latitude and longitude of the postal codes
in North Carolina by processing the df variable.
Display the average latitude and longitude of the state.
"""


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
    print(
        f"North Carolina center (avg of postal codes): latitude={avg_lat:.6f}, longitude={avg_lon:.6f}"
    )


"""
Prompt to Cursor:
Complete the 'postal_codes_nc_csv_to_toon' method using the toon-python library.
Read the given CSV file and write the corresponding Toon file in the
same directory.
"""


def postal_codes_nc_csv_to_toon():
    infile = "data/postal_codes/postal_codes_nc.csv"
    outfile = "data/postal_codes/postal_codes_nc.toon"

    df = pl.read_csv(infile)
    rows = df.to_dicts()
    data = {"postal_codes": rows}
    toon_str = encode(data)
    FS.write(toon_str, outfile)
    print(f"file written: {outfile}")


def imdb():
    data = duckdb.read_csv("https://datasets.imdbws.com/name.basics.tsv.gz")
    data.show()
    print(data.shape)  # (15003543, 6) <-- 15-million+ rows!

    # See https://developer.imdb.com/non-commercial-datasets/
    # name.basics.tsv.gz
    # title.akas.tsv.gz
    # title.basics.tsv.gz
    # title.crew.tsv.gz
    # title.episode.tsv.gz
    # title.principals.tsv.gz
    # title.ratings.tsv.gz


def openflights():
    """
    Read the OpenFlights dataset from a remote URL with DuckDB,
    parse each, and save each to a JSON file.
    See https://openflights.org/data.html
    """
    dataset_names = openflights_dataset_names()
    for idx, dataset_name in enumerate(dataset_names):
        if idx < 5:
            rel = read_remote_openflights_csv(dataset_name)
            rel.show(max_width=100)
            print(rel.shape)
            print(rel.df().columns.tolist())
            save_openflights_relation_to_json(rel, dataset_name)


def openflights_dataset_names():
    """
    Return the names of the OpenFlights datasets that are of interest to us.
    These are used in the openflights_url() method to form the URLs for each dataset.
    See https://openflights.org/data.html
    """
    return [
        "airports",
        "airlines",
        "routes",
        "planes",
        "countries",
    ]


def openflights_url(dataset_name: str):
    return f"https://raw.githubusercontent.com/jpatokal/openflights/master/data/{dataset_name}.dat"


def read_remote_openflights_csv(dataset_name: str):
    """
    Read a remote OpenFlights CSV file into a DuckDB relation.
    The remote CSV files do NOT have headers, so we need to specify the columns.
    See https://openflights.org/data.html
    """
    url = openflights_url(dataset_name)
    columns = openflights_colnames(dataset_name)
    return duckdb.read_csv(
        url,
        header=False,
        delimiter=",",
        columns=columns,
        strict_mode=False,
        ignore_errors=True,
        encoding="utf-8",
    )


def openflights_colnames(dataset_name: str):
    """
    Return the column names for each OpenFlights dataset since the remote CSV files do NOT have headers.
    See https://openflights.org/data.html
    """
    if dataset_name == "airports":
        return {
            "airport_id": "string",
            "name": "string",
            "city": "string",
            "country": "string",
            "iata_code": "string",
            "icao_code": "string",
            "latitude": "string",
            "longitude": "string",
            "altitude": "string",
            "timezone_code": "string",
            "dst": "string",
            "tz_database_time_zone": "string",
            "type": "string",
            "source": "string",
        }
    elif dataset_name == "airlines":
        return {
            "airline_id": "string",
            "name": "string",
            "alias": "string",
            "iata_code": "string",
            "icao_code": "string",
            "callsign": "string",
            "country": "string",
            "active": "string",
        }
    elif dataset_name == "routes":
        return {
            "airline_iata": "string",
            "airline_id": "string",
            "from_airport_iata": "string",
            "from_airport_id": "string",
            "to_airport_iata": "string",
            "to_airport_id": "string",
            "codeshare": "string",
            "stops": "string",
            "equipment": "string",
        }
    elif dataset_name == "planes":
        # "Airbus A319neo","31N","A19N"
        return {
            "name": "string",
            "iata_code": "string",
            "icao_code": "string",
        }
    elif dataset_name == "countries":
        return {
            "name": "string",
            "iso_code": "string",
            "dafif_code": "string",
        }
    else:
        return {}


def save_openflights_relation_to_json(rel, dataset_name: str):
    """
    Write the given DuckDB relation to a JSON file with one object-per-line.
    Then read it back and transform it into one big JSON object instead of object-per-line.
    """
    outfile1 = f"tmp/openflights_{dataset_name}_lines.json"
    rel.df().to_json(outfile1, orient="records", lines=True)
    print(f"file written: {outfile1}")

    outfile2 = f"tmp/openflights_{dataset_name}.json"
    lines = FS.read_lines(outfile1)
    objects = list()
    for line in lines:
        objects.append(json.loads(line))
    FS.write_json(objects, outfile2)


def augment_openflights_airports():
    """
    Augment each airport object with an address and and emptyembedding.
    The address is geocoded using the latitude and longitude with the geopy library.
    Bypass the airports with invalid IATA codes.
    This method reads and writes the same file multiple times, due to geopy rate limiting,
    to ensure that all airports are augmented correctly.
    """
    infile = "tmp/openflights_airports.json"
    objects = FS.read_json(infile)
    airport_count = len(objects)
    print(f"{airport_count} airports read from file {infile}")
    user_agent = "zero-to-AI-{}".format(int(time.time()))
    geolocator = Nominatim(user_agent=user_agent)
    time.sleep(10)
    exception_count, with_address_count, bypassed_count = 0, 0, 0

    for idx, obj in enumerate(objects):
        seq = idx + 1
        try:
            obj["embedding"] = list[float]()
            if exception_count < 100:
                iata_code = str(obj["iata_code"]).strip()
                if is_valid_iata_code(iata_code):
                    if "address" in obj.keys():
                        with_address_count += 1
                        print(f"{seq}/{airport_count}: {iata_code} already has an address")
                    else:
                        time.sleep(1.2)
                        latitude = float(obj["latitude"])
                        longitude = float(obj["longitude"])
                        location = geolocator.reverse(
                            (latitude, longitude), language="en", exactly_one=True
                        )
                        address = location.address
                        obj["address"] = address
                        print(f"{seq}/{airport_count}: {iata_code} --> {address}")
                        objects[idx] = obj
                else:
                    bypassed_count += 1
                    obj["address"] = "bypassed"
                    objects[idx] = obj
        except Exception as e:
            exception_count += 1
            print(f"Exception: {exception_count}: {e} on obj: {obj}")
            print(traceback.format_exc())

    print(f"with_address_count: {with_address_count}")
    print(f"bypassed_count:     {bypassed_count}")
    print(f"objects_count:      {len(objects)}")
    print(f"exception_count:    {exception_count}")
    FS.write_json(objects, infile)
    print(f"file written: {infile}")


def is_valid_iata_code(iata_code: str) -> bool:
    result: bool = True
    if len(iata_code) == 3:
        if "/" in iata_code:  # n/a, N/A
            result = False
        elif "\\" in iata_code:  # \N
            result = False
    else:
        result = False
    print(f"is_valid_iata_code: {iata_code} -> {result}")
    return result


def gen_pypi_download_lib_json_script():
    pip_list_lines = FS.read_lines("data/uv/uv-pip-list.txt")
    lib_names = list[str]()
    script_lines = list[str]()
    script_lines.append("#!/bin/bash")
    script_lines.append("")
    script_lines.append(
        "# This script downloads the JSON metadata for each library in the uv-pip-list.txt file."
    )
    script_lines.append(
        "# It then saves the JSON to a library-specific file in the data/pypi directory."
    )
    script_lines.append("# Chris Joakim, 3Cloud/Cognizant, 2026")
    script_lines.append("")

    in_data = False
    for pip_line in pip_list_lines:
        if in_data:
            tokens = pip_line.strip().split()
            lib_names.append(tokens[0].strip())
        if "----------" in pip_line:
            in_data = True

    FS.write_json(lib_names, "data/pypi/pypi_lib_names.json")

    lib_count = len(lib_names)
    for idx, name in enumerate(sorted(lib_names)):
        script_lines.append(f'echo "{idx + 1}/{lib_count}: {name}"')
        script_lines.append(
            f"curl -s -L https://pypi.python.org/pypi/{name}/json | jq > data/pypi_libs/{name}.json"
        )
        script_lines.append("sleep 1")
        script_lines.append("")

    script_lines.append("")
    FS.write_lines(script_lines, "pypi_download_lib_json.sh")


def explore_downloaded_pypi_libs():
    """
    Explore the downloaded JSON files in the data/pypi_libs directory.
    """
    files = FS.list_files_in_dir("data/pypi_libs")
    c = Counter()
    for idx, file in enumerate(sorted(files)):
        try:
            infile = f"data/pypi_libs/{file}"
            data = FS.read_json(infile)
            print(f"{idx + 1}/{len(files)}: {file}")

            for key in data.keys():
                c.increment(key)
            for key in data["info"].keys():
                c.increment(f"info/{key}")
        except Exception as e:
            print(f"Error: {e} on file: {file}")
            print(traceback.format_exc())

    FS.write_json(c.get_data(), "data/pypi/pypi_libs_attr_counter.json")


async def create_cosmosdb_pypi_lib_documents():
    """
    Create CosmosDB documents from the downloaded JSON files in the data/pypi_libs directory.
    """
    files = FS.list_files_in_dir("data/pypi_libs")

    for idx, file in enumerate(sorted(files)):
        try:
            if idx < 999999:
                infile = f"data/pypi_libs/{file}"
                data = FS.read_json(infile)
                doc = dict()
                name = data["info"]["name"]
                # doc["id"] = <-- can be automatically populated by cosmosdb
                doc["id"] = None
                doc["pk"] = "pypi"
                doc["name"] = name
                doc["author"] = str(data["info"]["author"])
                doc["author_email"] = str(data["info"]["author_email"])
                classifiers = data["info"]["classifiers"]
                doc["classifiers"] = prune_classifiers(classifiers)
                doc["description"] = str(data["info"]["description"])[0:1000]
                doc["docs_url"] = str(data["info"]["docs_url"])
                doc["downloads"] = str(data["info"]["downloads"])
                doc["home_page"] = str(data["info"]["home_page"])
                doc["keywords"] = str(data["info"]["keywords"])
                doc["maintainer"] = str(data["info"]["maintainer"])
                doc["maintainer_email"] = str(data["info"]["maintainer_email"])
                doc["requires_python"] = str(data["info"]["requires_python"])
                doc["summary"] = str(data["info"]["summary"])
                doc["version"] = str(data["info"]["version"])
                doc["release_count"] = len(data["releases"])

                model_max_context_length = 8192
                doc = truncate_cosmosdb_document(doc, model_max_context_length)
                if len(json.dumps(doc)) > model_max_context_length:
                    raise Exception(f"Document is too long: {name}")
                doc["id"] = str(uuid.uuid4())
                FS.write_json(doc, f"data/cosmosdb/{name}.json", sort_keys=False)
        except Exception as e:
            print(f"Error: {e} on name: {name}")
            print(traceback.format_exc())


def prune_classifiers(classifiers: list) -> list:
    if isinstance(classifiers, list):
        new_list = list()
        for classifier in classifiers:
            if "Intended Audience" in classifier:
                new_list.append(classifier)
            elif "Topic" in classifier:
                new_list.append(classifier)
            elif "Development Status" in classifier:
                new_list.append(classifier)
        return new_list
    else:
        return list()


async def add_embeddings_to_cosmosdb_documents():
    ai_util = AOAIUtil()
    files = FS.list_files_in_dir("data/cosmosdb")
    for idx, file in enumerate(sorted(files)):
        try:
            if idx < 999999:
                infile = f"data/cosmosdb/{file}"
                doc = FS.read_json(infile)
                if "embedding" not in doc.keys():
                    print(f"Generating embedding for {infile}")
                    id = doc["id"]
                    doc["id"] = ""  # not appropriate for semantic search
                    jstr = json.dumps(doc, sort_keys=False)
                    doc["embedding"] = await ai_util.generate_embeddings(jstr)
                    doc["id"] = id
                    FS.write_json(doc, infile, sort_keys=False)
                    asyncio.sleep(4.0)  # to avoid LLM throttling and 429 errors
        except Exception as e:
            print(f"Error: {e} on infile: {infile}")
            print(traceback.format_exc())


def truncate_cosmosdb_document(doc: dict, max_length: int) -> dict:
    jstr_len = len(json.dumps(doc))
    continue_to_process, loop_count = True, 0
    while continue_to_process:
        loop_count = loop_count + 1
        jstr = json.dumps(doc)
        if len(jstr) > max_length:
            doc.popitem("classifiers")
        if loop_count > 5:
            continue_to_process = False
    return doc


async def uv_parse():
    try:
        uv_parser = UVParser()
        uv_parser.parse_tree()
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())


def gen_graph_data():
    infile = "data/uv/uv-tree-libs.json"
    outfile = "data/rdf/graph-libs.json"
    libs_list = FS.read_json(infile)
    libs_dict = dict()
    for lib in libs_list:
        libs_dict[lib["name"]] = dict()

    FS.write_json(libs_dict, outfile)


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print_options()
        else:
            load_dotenv(override=True)
            logging.getLogger().setLevel(logging.WARNING)
            func = sys.argv[1].lower()
            if func == "postal_codes_nc_csv_to_json":
                postal_codes_nc_csv_to_json()
            elif func == "center_of_nc_with_polars":
                center_of_nc_with_polars()
            elif func == "postal_codes_nc_csv_to_toon":
                postal_codes_nc_csv_to_toon()
            elif func == "imdb":
                imdb()
            elif func == "openflights":
                openflights()
            elif func == "augment_openflights_airports":
                augment_openflights_airports()
            elif func == "gen_pypi_download_lib_json_script":
                gen_pypi_download_lib_json_script()
            elif func == "explore_downloaded_pypi_libs":
                explore_downloaded_pypi_libs()
            elif func == "create_cosmosdb_pypi_lib_documents":
                asyncio.run(create_cosmosdb_pypi_lib_documents())
            elif func == "add_embeddings_to_cosmosdb_documents":
                asyncio.run(add_embeddings_to_cosmosdb_documents())
            elif func == "uv_parse":
                asyncio.run(uv_parse())
            elif func == "gen_graph_data":
                gen_graph_data()
            else:
                print_options()
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())

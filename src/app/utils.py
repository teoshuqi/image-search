import json
from typing import Optional, Tuple

import pandas as pd

from src.config import WEBSCRAPER_CONFIG
from src.database.sql_models import ItemDB
from src.database.vector_models import VectorDB
from src.etl.extract import scrape_all_websites
from src.etl.load import insert_items_into_sql, insert_items_into_vectordb


def initialise_database() -> Tuple[ItemDB, VectorDB]:
    """
    Initializes the Flask application with database connections.

    This function creates connections to the PostgreSQL and vector databases
    using the provided models.

    Returns:
        tuple[ItemDB, VectorDB]: A tuple containing instances of ItemDB and VectorDB
            for interacting with the respective databases.
    """

    # Database configuration (replace with your actual settings)
    db = ItemDB()
    vector_db = VectorDB()
    return db, vector_db


def verify_databases(item_db: ItemDB, vector_db: VectorDB) -> Tuple[int, int]:
    """
    Count number of vectors and items in databases.

    Args:
        item_db (ItemDB): An instance of the ItemDB class for interacting with the PostgreSQL database.
        vector_db (VectorDB): An instance of the VectorDB class for interacting with the vector database.

    Returns:
        Tuple[int, int] : A tuple containing two integers - the count of items in the item database and vector database

    """
    num_items = item_db.count_items()  # Adjust indexing based on your setup
    num_vectors = vector_db.number_of_vectors()  # Adjust indexing based on your setup
    return num_items, num_vectors


def update_database(item_db: ItemDB, vector_db: VectorDB, pages: Optional[int] = 100) -> Tuple[ItemDB, VectorDB]:
    """
    Runs the ETL pipeline to scrape websites and update both databases

    Args:
        item_db (ItemDB): An instance of the ItemDB class for interacting with the PostgreSQL database.
        vector_db (VectorDB): An instance of the VectorDB class for interacting with the vector database.

    Returns:
        Tuple[ItemDB, VectorDB]: A tuple containing the same ItemDB and VectorDB instances
            used for deletion.

    """

    with open(WEBSCRAPER_CONFIG) as json_file:
        website_configs = json.load(json_file)

    scraped_products = scrape_all_websites(website_configs, pages=pages)
    print(f"scraped {len(scraped_products)} items from websites")

    # Insert data into SQL database
    insert_items_into_sql(item_db, scraped_products)
    insert_items_into_vectordb(item_db, vector_db)
    print("finished inserting items into db")

    return item_db, vector_db


def query_image_from_sqldb(item_db: ItemDB, ids_list: list[int]) -> pd.DataFrame:
    """
    Queries images from the PostgreSQL database based on IDs.

    This function retrieves information about images (items) from the database
    given a list of IDs. It returns a Pandas DataFrame for easy manipulation.

    Args:
        item_db (ItemDB): An instance of the ItemDB class for interacting with the PostgreSQL database.
        ids_list (list[int]): A list of integer IDs for the items to retrieve.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing details about the queried images.
            Columns include ID, title, brand, URL, and filepath.
    """

    items = item_db.read_item_by_ids(ids_list)
    result = {item.id: {"title": item.title, "brand": item.brand, "url": item.url, "imgpath": item.filepath} for item in items}
    result_df = pd.DataFrame(result).T
    return result_df


def search_images_by_imgpath(item_db: ItemDB, vector_db: VectorDB, img_path: str, n: int = 10) -> pd.DataFrame:
    """
    Searches for similar images using a reference image path.

    This function searches for images in the vector database based on the similarity
    to a provided image path. It retrieves data on the closest matches (n) from
    the PostgreSQL database and returns a Pandas DataFrame.

    Args:
        item_db (ItemDB): An instance of the ItemDB class for interacting with the PostgreSQL database.
        vector_db (VectorDB): An instance of the VectorDB class for interacting with the vector database.
        img_path (str): The path to the reference image used for the search.
        n (int, optional): The number of closest matches to retrieve (default: 10).

    Returns:
        pd.DataFrame: A Pandas DataFrame containing details about the similar images
            found. Columns include ID, title, brand, URL, filepath, and distance (similarity score).
    """

    raw_result = vector_db.query_with_image(img_path, n=n)
    result_df = query_image_from_sqldb(item_db, raw_result["ids"][0])
    result_df["distance"] = raw_result["distances"][0]
    return result_df


def search_images_by_text(item_db: ItemDB, vector_db: VectorDB, text: str, n: int = 10) -> pd.DataFrame:
    """
    Searches for similar images using a text description.

    This function searches for images in the vector database based on the similarity
    to a provided image path. It retrieves data on the closest matches (n) from
    the PostgreSQL database and returns a Pandas DataFrame.

    Args:
        item_db (ItemDB): An instance of the ItemDB class for interacting with the PostgreSQL database.
        vector_db (VectorDB): An instance of the VectorDB class for interacting with the vector database.
        text (str): The text description used for the search.
        n (int, optional): The number of closest matches to retrieve (default: 10).

    Returns:
        pd.DataFrame: A Pandas DataFrame containing details about the similar images
            found. Columns include ID, title, brand, URL, filepath, and distance (similarity score).
    """
    raw_result = vector_db.query_with_text(text, n=n)
    result_df = query_image_from_sqldb(item_db, raw_result["ids"][0])
    result_df = result_df.reset_index(drop=True)
    result_df["distance"] = raw_result["distances"][0]
    return result_df

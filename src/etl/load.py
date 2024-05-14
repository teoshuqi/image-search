from typing import List

from src.database.sql_models import (  # Assuming you have an Item model defined elsewhere
    Item,
    ItemDB,
)
from src.database.vector_models import VectorDB

from .product import Product


def insert_items_into_sql(item_db: ItemDB, product_info: List[Product]) -> None:
    """
    Inserts new items into the SQL database, avoiding duplicates.

    Args:
        item_db (ProductDB): An instance of the ProductDB class for interacting with the database.
        item_info (List[Item]): A list of Item objects representing the items to insert.

    Returns:
        None
    """

    for prd in product_info:
        item = Item(
            filepath=prd.imgName,
            title=prd.title,
            url=prd.url,
            brand=prd.brand,
            updated_vectordb=False,
            scraped_time=prd.processed_time,
        )
        # Check for existing item with same title and brand before inserting
        item_attributes = {"title": item.title, "brand": item.brand}
        existing_items = item_db.filter_items_by_charfields(item_attributes)
        if not existing_items:
            item_db.create_item(item)


def insert_items_into_vectordb(
    item_db: ItemDB,
    vector_db: VectorDB,
) -> None:
    """
    Inserts new item vectors into the vector database.

    Args:
        item_db (ProductDB): An instance of the ProductDB class for interacting with the database.
        vector_operations (object): An object with methods to interact with the vector database.
                                     (Specific type depends on your implementation)

    Returns:
        None
    """

    existing_ids = set(vector_db.get_all_data()["ids"])
    items_to_insert = [item for item in item_db.read_items() if (str(item.id) not in existing_ids) and (item.filepath != "")]

    print(f"Inserting {len(items_to_insert)} items into vectordb")
    if items_to_insert:
        vector_db.insert_data(items_to_insert)

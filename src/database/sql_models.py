from typing import Dict, List

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import (  # Import required variables from config.py
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_PWD,
    POSTGRES_USER,
)

# Define database table model
Base = declarative_base()


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    filepath = Column(String)
    title = Column(String)
    url = Column(String)
    brand = Column(String)
    updated_vectordb = Column(Boolean)
    scraped_time = Column(DateTime)

    def __repr__(self):
        return f"Item(id={self.id}, title='{self.title}',\
                brand='{self.brand}')"


class ItemDB:
    """
    A class for interacting with a PostgreSQL database containing item data.

    This class provides methods to create, read, update, and delete item
    information using SQLAlchemy.
    """

    def __init__(self) -> None:
        """
        Initializes the ItemDB object.

        Args:
            url: A SQLAlchemy connection URL string.
        """
        db_url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        self.engine = create_engine(db_url)
        Item.__table__.create(bind=self.engine, checkfirst=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_item(self, item: Item) -> None:
        """
        Creates a new item in the database.

        Args:
            item: A Item object representing the item to create.
        """
        session = self.Session()
        session.add(item)
        session.commit()
        # print(f"Item '{item}' added successfully!")
        session.close()

    def read_item_by_ids(self, id_List: List[int]) -> List[Item]:
        """
        Retrieves items from the database based on a List of IDs.

        Args:
            id_List: A List of integer IDs for the items to retrieve.

        Returns:
            A List of Item objects matching the provided IDs.
        """
        session = self.Session()
        items = session.query(Item).filter(Item.id.in_(id_List)).all()
        session.close()
        return items

    def read_items(self) -> List[Item]:
        """
        Retrieves all items from the database.

        Returns:
            A List of all Item objects in the database.
        """
        session = self.Session()
        items = session.query(Item).all()
        session.close()
        return items

    def count_items(self) -> int:
        """
        Counts the number of items in the database.

        Returns:
            An integer representing the total number of items.
        """
        session = self.Session()
        count = session.query(Item).count()
        session.close()
        return count

    def filter_items_by_charfields(self, criterias: Dict[str, str]) -> List[Item]:
        """
        Filters items based on criteria for character fields.

        Args:
            criterias: A Dictionary containing criteria for filtering.
                        Keys are item attribute names, values are strings
                        to match with the 'like' operator.

        Returns:
            A List of Item objects matching the specified filter criteria.
        """
        session = self.Session()
        q = session.query(Item)
        for attr, value in criterias.items():
            q = q.filter(getattr(Item, attr).like("%%%s%%" % value))
        filtered = q.all()
        session.close()
        return filtered

    def update_item(self, item_id: int, update_data: Dict[str, any]) -> None:
        """
        Updates an existing item in the database.

        Args:
            item_id: The ID of the item to update.
            update_data: A Dictionary containing key-value pairs for updated fields.
        """
        session = self.Session()
        item = session.get(Item, item_id)
        if item:
            for field, value in update_data.items():
                setattr(item, field, value)
            session.commit()
            print(f"Item ID {item_id} updated successfully!")
        else:
            print(f"Item ID {item_id} not found!")
        session.close()

    def delete_item(self, item_id: int) -> None:
        """
        Deletes a item from the database.

        Args:
            item_id: The ID of the item to delete.
        """
        session = self.Session()
        item = session.get(Item, item_id)
        if isinstance(item, Item):
            session.delete(item)
            print(f"Item ID {item_id} deleted successfully!")
        else:
            print(f"Item ID {item_id} not available!")
        session.commit()
        session.close()

    def delete_all(self) -> None:
        """
        Truncates the item database.

        """
        session = self.Session()

        session.query(Item).delete()
        print("deleting items db ....")

        session.commit()  # Commit the changes
        session.close()  # Close the session


if __name__ == "__main__":
    itemdb = ItemDB()
    count = itemdb.count_items()
    print(f"item db has {count} items")
    items = itemdb.read_items()
    print(items)

from typing import Dict, List, Optional

from src.database.sql_models import Item

from .product import (
    ACWProduct,
    LBProduct,
    Product,
    SSDProduct,
    TTRProduct,
    TWLProduct,
)
from .scraper import WebsiteScraper


def select_product_class(name: str) -> Product:
    product_classes = {"TWLProduct": TWLProduct, "TTRProduct": TTRProduct, "SSDProduct": SSDProduct, "ACWProduct": ACWProduct, "LBProduct": LBProduct}
    return product_classes.get(name)


def load_product_class_into_config(config):
    try:
        class_name = config["product_class"]
        product_class = select_product_class(class_name)
        config["product_class"] = product_class
        return config
    except (ImportError, AttributeError):
        raise ValueError(f"Invalid scraper class: {class_name}")


def scrape_product_from_website(config: Dict[str, str], pages=100) -> List[Item]:
    """
    Scrapes product information from a single website.

    This function takes a configuration dictionary containing website details
    and returns a list of dictionaries, each representing a scraped product.

    Args:
        config (Dict[str, str]): A dictionary containing website configuration.
            Keys should include 'base_url' (the website's base URL).

    Returns:
        List[Item]: A list of Items with scraped information.
    """
    config = load_product_class_into_config(config)
    scraper = WebsiteScraper(**config)
    products = scraper.get_all_product_info(max_pages=pages)
    print(f"Scrapped {len(products)} products from {config['base_url']}.")
    return products


def scrape_all_websites(website_configs, pages: Optional[int] = 100):
    """
    Scrapes product information from the given websites.
    Args:
        website_configs: A list of dictionaries containing configuration
        for each website.
    Returns:
        A list of product information dictionaries.
    """

    product_info = []
    for _, config in website_configs.items():
        product_info += scrape_product_from_website(config, pages=pages)
    return product_info

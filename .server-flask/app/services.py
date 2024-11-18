import logging
from app.models import (
    get_all_items, get_item_by_id, create_item, update_item, delete_item
)

logger = logging.getLogger(__name__)

def list_items():
    logger.info("Fetching all items")
    return get_all_items()

def retrieve_item(item_id):
    logger.info(f"Fetching item with id {item_id}")
    return get_item_by_id(item_id)

def add_item(item):
    logger.info(f"Adding item: {item.dict()}")
    return create_item(item)

def modify_item(item_id, item):
    logger.info(f"Updating item with id {item_id}: {item.dict()}")
    update_item(item_id, item)

def remove_item(item_id):
    logger.info(f"Deleting item with id {item_id}")
    delete_item(item_id)

from fastapi import FastAPI, HTTPException, Request
from typing import List
from config import logging
from config import database
from config import models
import os
import dotenv

dotenv.load_dotenv()

# Initialize logger
logger = logging.setup_logging()

# Initialize FastAPI app
async def lifespan(app: FastAPI):
    await database.connect_db()
    logger.info("Database database.connected.")
    yield
    await database.close_db()
    logger.info("Database database.connection closed.")

app = FastAPI(lifespan=lifespan)

@app.post("/items/", response_model=models.ItemResponse)
def create_item(item: models.Item):
    """Create a new item."""
    try:
        cursor = database.database.conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
            (item.name, item.description, item.price, item.quantity),
        )
        database.database.conn.commit()
        logger.info(f"Item created: {item.dict()}")
        return models.database.ItemResponse(id=cursor.lastrowid, **item.dict())
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Error creating item.")


@app.get("/items/", response_model=List[models.ItemResponse])
def get_items():
    """Retrieve all items."""
    try:
        cursor = database.database.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        logger.info(f"Retrieved {len(rows)} items.")
        return rows
    except Exception as e:
        logger.error(f"Error retrieving items: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving items.")


@app.get("/items/{item_id}", response_model=models.ItemResponse)
def get_item(item_id: int):
    """Retrieve a single item by ID."""
    try:
        cursor = database.database.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        row = cursor.fetchone()
        if not row:
            logger.warning(f"Item with ID {item_id} not found.")
            raise HTTPException(status_code=404, detail="Item not found")
        logger.info(f"Retrieved item: {row}")
        return row
    except Exception as e:
        logger.error(f"Error retrieving item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving item.")


@app.put("/items/{item_id}", response_model=models.ItemResponse)
def update_item(item_id: int, item: models.Item):
    """Update an item."""
    try:
        cursor = database.conn.cursor()
        cursor.execute(
            "UPDATE items SET name = %s, description = %s, price = %s, quantity = %s WHERE id = %s",
            (item.name, item.description, item.price, item.quantity, item_id),
        )
        database.conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Item with ID {item_id} not found for update.")
            raise HTTPException(status_code=404, detail="Item not found")
        logger.info(f"Updated item {item_id}: {item.dict()}")
        return database.ItemResponse(id=item_id, **item.dict())
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating item.")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item and resequence IDs."""
    try:
        cursor = database.conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        database.conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Item with ID {item_id} not found for deletion.")
            raise HTTPException(status_code=404, detail="Item not found")
        resequence_ids()
        logger.info(f"Deleted item {item_id} and resequenced IDs.")
        return {"message": "Item deleted and IDs resequenced"}
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting item.")


def resequence_ids():
    """Resequence IDs to maintain sequential order."""
    try:
        cursor = database.conn.cursor()
        cursor.execute("SET @new_id = 0;")
        cursor.execute(
            """
            UPDATE items SET id = (@new_id := @new_id + 1) ORDER BY id;
            """
        )
        database.conn.commit()
        cursor.execute("ALTER TABLE items AUTO_INCREMENT = 1;")
        database.conn.commit()
        logger.info("Resequenced IDs successfully.")
    except Exception as e:
        logger.error(f"Error resequencing IDs: {e}")
        raise


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all incoming requests."""
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT"))

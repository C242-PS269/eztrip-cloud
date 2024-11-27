import os
import dotenv
import uvicorn

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

from config import logging

# load environment variables
dotenv.load_dotenv()
# initialize logging
logging = logging.log()

# initialize FastAPI app
app = FastAPI()

# Root route
@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the EzTrip ML-Model Server",
    }

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT"))
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as rng_router
from routes import collection_name
from db_var import ip_address, database_name
# config = dotenv_values(".env")
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This allows incoming connections from all addresses to prevent CORS error.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    # allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ip_address)
    app.database = app.mongodb_client[database_name]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(rng_router, tags=["rng"], prefix="/rng")

import os
import traceback

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from .models import Query
from .utils import (
    initialise_database,
    search_images_by_imgpath,
    search_images_by_text,
    update_database,
    verify_databases,
)

router = APIRouter()


@router.get("/healthcheck")
def healthcheck():
    return JSONResponse(content={"message": "connected!"}, status_code=200)


@router.post("/update/{pages}")
async def update_db(pages: int, databases: tuple = Depends(initialise_database)):
    """
    Triggers the ETL pipeline to update databases asynchronously.

    This function takes the following parameters:

    - **pages (int):** The number of pages to scrape for each website during the update.
    - **databases (Tuple[Any, Any], optional):** A tuple containing database
      connection objects, obtained through the `initialise_database` dependency.

    It attempts to update the databases using the `update_database` function and
    then verifies the number of items and vectors in both databases using
    `verify_databases`. Upon success, it returns a JSON response with a success
    message containing the number of items and vectors.

    Raises:

    - **HTTPException (500):** If any exception occurs during the update or
      verification process. The detailed error message is included in the response.
    """
    try:
        _, _ = update_database(pages=pages, *databases)
        num_items, num_vectors = verify_databases(*databases)
        message = f"ETL pipeline trigger successful. {num_items} in Items DB. {num_vectors} in Vector DB."
        return JSONResponse(content={"message": message})
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        raise HTTPException(status_code=500, detail=f"Error triggering ETL pipeline: {str(e)}")


@router.post("/search")
def search_data(query: Query, databases: tuple = Depends(initialise_database)):
    if query.type == "text":
        result_df = search_images_by_text(*databases, query.text, n=10)
    elif query.type == "image":
        if os.path.isfile(query.text):  # Check for image path safety
            result_df = search_images_by_imgpath(*databases, query.text, n=10)  # Use unpacking
        else:
            return JSONResponse(content={"error": "Image path invalid"}, status_code=400)
    else:
        return JSONResponse(content={"error": "Invalid query type"}, status_code=400)

    return JSONResponse(content=result_df.to_dict(orient="records"))

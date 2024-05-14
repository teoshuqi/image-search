from pydantic import BaseModel


class Query(BaseModel):
    """
    Represents a search query to be used with the `/search` endpoint.

    This model is used to validate and parse query parameters sent to the
    `/search` endpoint in your FastAPI application. It defines two fields:

    - **text (str):** The text string to be searched for. This is a required field.
    - **type (Optional[str]):** An optional field to specify the type of search.
      Valid options depend on your specific implementation, but common examples
      might include "products", "articles", or "users".

    By using this model, you can ensure that your API receives well-structured
    query parameters, improving data validation and making your code more robust.
    """

    text: str
    type: str

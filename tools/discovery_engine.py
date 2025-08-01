
import os
from typing import List, Dict, Any
from google.cloud import discoveryengine_v1beta
from google.api_core.client_options import ClientOptions
from google.protobuf.json_format import MessageToDict

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION") 
DATASTORE_ID = os.getenv("DATASTORE_ID") # Make sure to set this in your .env



if not PROJECT_ID or not DATASTORE_ID:
    raise ValueError(
        "Please set GOOGLE_CLOUD_PROJECT and YOUR_DATASTORE_ID "
        "environment variables in your .env file."
    )

# Construct the serving config name for data store

SERVING_CONFIG_NAME = (
    f"projects/{PROJECT_ID}/locations/{LOCATION}/dataStores/{DATASTORE_ID}/servingConfigs/default_config"
)

# Initialize the Discovery Engine client
# The endpoint depends on your location. For 'global', it's 'discoveryengine.googleapis.com'.
# For regional, it's '{location}-discoveryengine.googleapis.com'.
client_options = ClientOptions(api_endpoint=f"{LOCATION}-discoveryengine.googleapis.com")
search_client = discoveryengine_v1beta.SearchServiceClient(client_options=client_options)


def retrieve_product_details_from_search(query: str, max_results: int = 10) -> str:
    """
    Searches the Vertex AI Search data store for products relevant to the query
    and retrieves their titles and image URLs.

    This tool is useful when the user asks for product details that include
    visuals or specific product names.

    Args:
        query (str): The search query, e.g., "laptops with good battery life"
                     or "images of product XYZ".
        max_results (int): The maximum number of product details to retrieve.
                           Defaults to 3.

    Returns:
        str: A formatted string containing the titles and image URLs of the
             retrieved products, or a message if no results are found.
    """
    if not query:
        return "Please provide a query to search for product details."

    try:
        request = discoveryengine_v1beta.SearchRequest(
            serving_config=SERVING_CONFIG_NAME,
            query=query,
            page_size=max_results,
        )

        response = search_client.search(request=request)

        product_details = []
        for result in response.results:
            document = result.document
            # For structured data, the fields are usually in document.struct_data
            structured_data = MessageToDict(document._pb.struct_data) # Convert protobuf struct to dict

            title = structured_data.get('title_y', 'N/A')
            image_url = structured_data.get('main_image_url', 'N/A') 
           

            product_details.append(
                f"Title: {title}\n"
                f"Image URL: {image_url}\n"
            )

        if product_details:
            return "Found the following product details:\n\n" + "\n---\n".join(product_details)
        else:
            return "No relevant product details found in the data store for your query."

    except Exception as e:
        print(f"Error calling Vertex AI Search: {e}")
        return f"An error occurred while searching for product details: {str(e)}"


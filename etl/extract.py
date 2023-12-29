import requests
import logging

logger = logging.getLogger(__name__)

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        extracted_data = response.text  # Extract the data from the response
        return extracted_data
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error: {e}")
        return None


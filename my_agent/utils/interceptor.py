import httpx
import http.client as http_client
import logging
import requests
from requests.models import Response

def log_request_and_response(response: Response, *args, **kwargs):
    """Logs the request and response details."""
    logging.debug(f"Request: {response.request.method} {response.request.url}")
    logging.debug(f"Request Headers: {response.request.headers}")
    if response.request.body:
        logging.debug(f"Request Body: {response.request.body}")
    
    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Headers: {response.headers}")
    logging.debug(f"Response Body: {response.text}")

def enable_request_logging():
    # Enable HTTPConnection debug logs
    http_client.HTTPConnection.debuglevel = 1

    # Initialize logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    # Create a session and attach the response hook
    session = requests.Session()
    session.hooks['response'] = [log_request_and_response]

    # Replace the default session used by requests with this one
    requests.sessions.default_session = session

# Function to log response in httpx
def log_httpx_response(response):
    logging.debug(f"HTTPX Request URL: {response.request.url}")
    logging.debug(f"HTTPX Request Headers: {response.request.headers}")
    if response.request.content:
        logging.debug(f"HTTPX Request Body: {response.request.content}")
    
    logging.debug(f"HTTPX Response Status: {response.status_code}")
    logging.debug(f"HTTPX Response Headers: {response.headers}")
    logging.debug(f"HTTPX Response Body: {response.text}")

def enable_httpx_logging():
    http_client.HTTPConnection.debuglevel = 1

    # Initialize logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Create an httpx client with a hook for logging responses
    client = httpx.Client()
    
    # Wrapping httpx response
    def wrapped_send(request, *args, **kwargs):
        response = client.send(request, *args, **kwargs)
        log_httpx_response(response)
        return response
    
    # Use the custom wrapped_send method to capture and log responses
    httpx.Client.send = wrapped_send

enable_httpx_logging()

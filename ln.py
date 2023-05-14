import requests
import os

# bitcoin lightning vars
LND_API_ENDPOINT = os.getenv("LND_API_ENDPOINT")
MACAROON = os.getenv("MACAROON")


def fetch(url, method="GET", headers=None, params=None, data=None):
    # Set default headers
    default_headers = {"Grpc-Metadata-Macaroon": MACAROON}
    if headers is not None:
        default_headers.update(headers)

    # Make request
    response = requests.request(
        method=method,
        url=url,
        headers=default_headers,
        params=params,
        json=data,
        # NOTE: Do not use verify=False in production!
        # TODO: only use verify=False in dev
        verify=False,
    )

    # Check for errors
    response.raise_for_status()

    # Return JSON data
    return response.json()


def add_invoice(amount, memo):
    # Construct the request
    url = f"{LND_API_ENDPOINT}/v1/invoices"
    data = {"value": amount, "memo": memo}

    # Make the request
    return fetch(url, method="POST", data=data)


def lookup_invoice(r_hash):
    # Construct the request
    url = f"{LND_API_ENDPOINT}/v1/invoice/{r_hash}"
    # Make the request
    return fetch(url)

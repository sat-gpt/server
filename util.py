import codecs

def price(query, sat_per_token=1):
    """Calculate the price of a query in satoshis based on the query's length."""
    return len(query) * sat_per_token

def base64_to_hex(base64_string):
    decoded_bytes = codecs.decode(base64_string.encode('utf-8'), 'base64')
    hex_string = codecs.encode(decoded_bytes, 'hex').decode()
    return hex_string
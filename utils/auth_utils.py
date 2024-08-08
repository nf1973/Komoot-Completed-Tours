from datetime import datetime

def has_cookie_expired(cookie: str) -> bool:
    """Check if the cookie has expired based on the included expiration timestamp."""
    expire = int(extract_expiration_timestamp(cookie))
    expire_seconds = expire / 1000
    expiration_date = datetime.fromtimestamp(expire_seconds)
    return expiration_date < datetime.now()

def extract_expiration_timestamp(cookie: str) -> str:
    """Extract the expiration timestamp from the cookie string."""
    expire_str = '&expire='
    start_pos = cookie.find(expire_str)
    if start_pos == -1:
        raise ValueError("Expiration timestamp not found in cookie string")
    # Extract the substring from '&expire=' to the end
    expire_substring = cookie[start_pos + len(expire_str):]
    return expire_substring
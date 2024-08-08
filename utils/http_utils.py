import httpx
import sys

def set_headers(user_id: str, cookie: str) -> dict:
    """Set headers for the HTTP requests."""
    return {
        "Accept": "application/hal+json,application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Cache-Control": "no-cache",
        "Cookie": cookie, 
        "Pragma": "no-cache",
        "Referer": f"https://www.komoot.com/user/{user_id}?tab=tours", 
        "Sec-Ch-Ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
        }

def extract_tours(headers: dict, user_id: str, page_num: int) -> list:
    """Extract tours from the API."""
    url = f"https://www.komoot.com/api/v007/users/{user_id}/tours/"
    params = {
        'sport_types': '',
        'type': 'tour_recorded',
        'sort_field': 'date',
        'sort_direction': 'asc',
        'name': '',
        'status': '',
        'hl': 'en',
        'page': page_num,
        'limit': 24
        }
    
    with httpx.Client(http2=True) as client:
        try:
            response = client.get(url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()['_embedded']['tours']
            else:
                display_response_code_text(response.status_code, response.text)
        except Exception as e:
            return []
        
def display_response_code_text(status_code: int, text: str) -> None:
    """Display the status code and text of an HTTP response."""
    if status_code == 401:
        print(f"401 Unauthorized: Check your authentication credentials.")
    elif status_code == 403:
        print(f"403 Forbidden: You do not have permission to access this resource.")
    elif status_code == 404:
        print(f"404 Not Found")
    else:
        print(f"Error {status_code}: {text}")
    sys.exit(1)
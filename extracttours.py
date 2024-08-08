import sys
from time import sleep
import httpx
import os
from datetime import datetime
import math
import json
from tour import Tour

def get_existing_tour_ids(filename: str) -> list:
    if os.path.exists(filename):
        with open("tours.json", "r", encoding="utf-8") as f:
            existing_tours = json.load(f).get("completed_tours", [])
            tour_ids = [tour.get("tour_id") for tour in existing_tours]
            print (f"Found {len(tour_ids)} tours already in {filename}")
        return tour_ids
    else:
        return []

def set_headers(user_id: str, cookie: str) -> dict:
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

def get_connection_data(f: str,prompt: str) -> str:
    if os.path.exists(f):
        with open(f,'r') as file:
            return file.read().rstrip('\n')
    else:
        return input(prompt)

def has_cookie_expired(cookie: str) -> bool:
    expire = int(extract_expiration_timestamp(cookie))
    expire_seconds = expire / 1000
    expiration_date = datetime.fromtimestamp(expire_seconds)
    return expiration_date < datetime.now()

def extract_expiration_timestamp(cookie: str) -> str:
    expire_str = '&expire='
    start_pos = cookie.find(expire_str)
    if start_pos == -1:
        raise ValueError("Expiration timestamp not found in cookie string")
    # Extract the substring from '&expire=' to the end
    expire_substring = cookie[start_pos + len(expire_str):]
    return expire_substring


def display_response_code_text(status_code: int, text: str) -> None:
    if status_code == 401:
        print(f"401 Unauthorized: Check your authentication credentials.")
    elif status_code == 403:
        print(f"403 Forbidden: You do not have permission to access this resource.")
    elif status_code == 404:
        print(f"404 Not Found")
    else:
        print(f"Error {status_code}: {text}")
    sys.exit(1)

def extract_tours(headers: dict, user_id: str, page_num: int) -> list:
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
   
def write_tours_to_file(all_objects: list, filename: str, root_object: str) -> None:
    # Load existing data if the file already exists
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}  # Handle case where file is empty or not valid JSON
    else:
        existing_data = {}

    # Update the existing data with new objects
    if root_object in existing_data:
        existing_data[root_object].extend([obj.__dict__ for obj in all_objects])
    else:
        existing_data[root_object] = [obj.__dict__ for obj in all_objects]

    # Write the updated data back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    
    delay = 1 # seconds
    filename = "tours.json"
    
    # Get user ID and cookie
    user_id = get_connection_data("user_id.dat", "Enter your user ID: ")
    cookie = get_connection_data("cookie.dat", "Enter your cookie: ")
    headers = set_headers(user_id, cookie)

    # Get existing tours from file so that we can check if we already have them
    existing_tour_ids = get_existing_tour_ids(filename)
        
    # Check if cookie has expired and if not extract tours
    if not has_cookie_expired(cookie):
        page_num = 0
        already_got_last_page = False
        all_tours = []

        while not already_got_last_page:
            sleep(delay) # Add delay to avoid risk of rate limiting
            extracted_tours = extract_tours(headers, user_id, page_num)
            page_num += 1

            if extracted_tours: 
                for tour in extracted_tours:
                    if tour['id'] not in existing_tour_ids:
                        this_tour = Tour(tour)
                        all_tours.append(this_tour)
                        print (f"Will add tour {this_tour.tour_id} ({this_tour.date} {this_tour.name})")
            else:
                already_got_last_page = True
                
    else:   
        print(f"Your cookie has expired. Please generate a new one.")
        sys.exit(1)


    # Write tours to file   
    if len(all_tours) > 0:
        write_tours_to_file(all_tours, "tours.json", "completed_tours")
        print(f"Added {len(all_tours)} tours to {filename}")
    else:
        print(f"No new tours to add to {filename}")
  


# Developed by @neilf73 on GitHub

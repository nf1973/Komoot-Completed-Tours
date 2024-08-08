import sys
from time import sleep
from datetime import datetime

from tour import Tour
from http_utils import set_headers, extract_tours
from file_utils import get_connection_data, get_existing_tour_ids, write_tours_to_file

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
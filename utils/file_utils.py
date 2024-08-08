import os
import json


def get_connection_data(f: str,prompt: str) -> str:
    if os.path.exists(f):
        with open(f,'r') as file:
            return file.read().rstrip('\n')
    else:
        return input(prompt)
    
def get_existing_tour_ids(filename: str) -> list:
    if os.path.exists(filename):
        with open("tours.json", "r", encoding="utf-8") as f:
            existing_tours = json.load(f).get("completed_tours", [])
            tour_ids = [tour.get("tour_id") for tour in existing_tours]
            print (f"Found {len(tour_ids)} tours already in {filename}")
        return tour_ids
    else:
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

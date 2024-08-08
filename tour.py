from datetime import datetime
from typing import Dict, Any
import math

class Tour:
    def __init__(self, tour: Dict[str, Any]):
        dt = self._extract_datetime(tour['date'])
        self.tour_id = tour['id']
        self.date = dt.strftime('%Y-%m-%d')
        self.time = dt.strftime('%H:%M:%S')
        self.distance = self._format_distance(tour['distance'])
        self.name = tour['name']
        self.start_lat = tour['start_point']['lat']
        self.start_lng = tour['start_point']['lng']
        self.start_alt = tour['start_point']['alt']
        self.duration_in_seconds = tour['duration']
        self.elevation_up = tour['elevation_up']
        self.elevation_down = tour['elevation_down']
        self.sport = tour['sport']
        self.time_moving = tour['time_in_motion']
        self.map_url = self._remove_query_parameters(
            tour.get('vector_map_image', {}).get('src') or tour.get('map_image', {}).get('src')
        )
        self.tour_url = f"https://www.komoot.com/tour/{self.tour_id}"

    def _extract_datetime(self, iso_string: str) -> datetime:
        return datetime.fromisoformat(iso_string.replace("Z", "+00:00"))

    def _format_distance(self, distance: int) -> float:
        return math.floor(distance / 100) / 10
    
    def _remove_query_parameters(self, url: str) -> str:
        return url.split('?')[0]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.tour_id,
            'date': self.date,
            'time': self.time,
            'distance': self.distance,
            'name': self.name,
            'start_lat': self.start_lat,
            'start_lng': self.start_lng,
            'start_alt': self.start_alt,
            'duration_in_seconds': self.duration_in_seconds,
            'elevation_up': self.elevation_up,
            'elevation_down': self.elevation_down,
            'sport': self.sport,
            'time_moving': self.time_moving,
            'map_url': self.map_url,
            'tour_url': self.tour_url
        }
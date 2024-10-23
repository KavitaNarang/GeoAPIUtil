import os
import click
import requests
import warnings
from typing import Dict, Optional
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/geo/1.0"

def process_location(location) -> Optional[Dict]:
    """
    Process a location string and retrieve its geo information.
 
    Args:
        location (str): Location string, either city, state or zip code

    Returns:
        Optional[Dict]: Dictionary containing location information if found, None otherwise.
            Keys include: name, state, country, lat, lon, zip (for ZIP code queries)
    """
    if ',' in location:
        result = get_location_by_cityState(location)
    else:
        result = get_location_by_zipcode(location)   
    if result:
        return {
            'name': result.get('name'),
            'state': result.get('state', None),
            'country': result.get('country'),
            'lat': result.get('lat'),
            'lon': result.get('lon'),
            'zip': result.get('zip', None)
        }
    return None

def get_location_by_cityState(location) -> Optional[Dict]:
    """
    Retrieve geo location information using city and state.

    Args:
        location (str): Location string in the format "City, State" (e.g., "Madison, WI")

    Returns:
        Optional[Dict]: Dictionary containing location information if found, None otherwise.
            Keys include: name, state, country, lat, lon
 
    Raises:
        requests.exceptions.RequestException: If the API request fails
        ValueError: If the location string is not in the correct format
    """
    city, state = location.split(',')
    url = f"{BASE_URL}/direct?q={city},{state},US&limit=1&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None
    except ValueError:
        click.echo(f"Error: City,State '{location}' is not in the correct format. Use 'City, State'")
        return None
    except requests.exceptions.RequestException as err:
        click.echo(f"Error accessing API for '{location}': {str(err)}")
        return None
    
def get_location_by_zipcode(zipcode) -> Optional[Dict]:
    """
    Retrieve geo location information using zipcode.
 
    Args:
        zipcode (str): US ZIP code
 
    Returns:
        Optional[Dict]: Dictionary containing location information if found, None otherwise.
            Keys include: name, state, country, lat, lon, zip
  
    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    url = f"{BASE_URL}/zip?zip={zipcode},US&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  
        return data
    except requests.exceptions.RequestException as err:
        click.echo(f"Error accessing API for ZIP code '{zipcode}'")
        return None

@click.command()
@click.option('--locations', multiple=True, help='List of locations (city, state or zip code)') 
@click.argument('location_args', nargs=-1) 
def geoloc_util(locations, location_args):
    """
    Command-line utility for retrieving location information.

    Supports two input formats:
    1. Using --locations option: --locations "Madison, WI" "12345"
    2. Using positional arguments: "Madison, WI" "12345"

    For city/state format, use: "City, State" (e.g., "Madison, WI")
    For ZIP codes, use: "12345"

    All locations must be within the United States.
    """
    all_locations = locations + location_args
    for location in all_locations:
        if not location.strip():
            click.echo(f"Empty location provided: '{location}'")
            continue
        if not all_locations or all(location.strip() == '' for location in all_locations):
            click.echo("No valid locations provided.")
            return
        print(f"Location: {location}")
        result = process_location(location)
        if result:
            click.echo(f"Location: {location}")
            click.echo(f"Name: {result['name']}")
            click.echo(f"State: {result['state']}")
            click.echo(f"Country: {result['country']}")
            click.echo(f"Latitude: {result['lat']}")
            click.echo(f"Longitude: {result['lon']}")
            if result.get('zip'):
                click.echo(f"Zip: {result['zip']}")
        else:
            click.echo(f"No results found for location: {location}")

if __name__ == '__main__':
    geoloc_util()
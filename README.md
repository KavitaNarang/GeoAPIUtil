# geoLoc Utility

A command-line utility for retrieving location information (latitude, longitude, city, state, country from OpenWeatherMap's Geo API.

## How to run the command line geoLoc Util

### Clone Repository

Clone the repository: `git clone ___`
 
### Create Virtual Environment

1. Create and activate a virtual environment to isolate dependencies
`python -m venv venv`

2. Activate virtual environment
`source venv/bin/activate`

### Install Dependencies

Install dependencies using command: `pip install -r requirements.txt`

### Set API Key in environment variable

Create a `.env` file under `src` folder and add the OpenWeatherMap API key value in the `.env` file
`API_KEY={api_key_value}`

### Usage
`python3 src/geoLoc.py --help`

```
Usage: geoLoc.py [OPTIONS] [LOCATION_ARGS]...

  Command-line utility for retrieving location information.

  Supports two input formats: 1. Using --locations option: --locations
  "Madison, WI" "12345" 2. Using positional arguments: "Madison, WI" "12345"

  For city/state format, use: "City, State" (e.g., "Madison, WI") For ZIP
  codes, use: "12345"

  All locations must be within the United States.

Options:
  --locations TEXT  List of locations (city, state or zip code)
  --help            Show this message and exit.
```

### Examples
`python3 src/geoLoc.py --locations "Madison, WI" "12345"`

`python3 src/geoLoc.py "Madison, WI"`

`python3 src/geoLoc.py "Madison, WI" "12345" "Chicago, IL" "10001"`

### Run Integration Tests
`python3 -m unittest discover src/tests`
import argparse
import requests
import sys
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Constants
API_BASE_URL = "https://weao.xyz/api"
HEADERS = {
    "User-Agent": "WEAO-3PService"
}
PUBLIC_DIR = "public"
DATA_FILE = os.path.join(PUBLIC_DIR, "data.json")

def make_api_request(endpoint):
    """
    Makes a GET request to a specified API endpoint.
    """
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for endpoint '{endpoint}': {http_err}", file=sys.stderr)
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred for endpoint '{endpoint}': {req_err}", file=sys.stderr)
    except Exception as err:
        print(f"An unexpected error occurred for endpoint '{endpoint}': {err}", file=sys.stderr)
    return None

def handle_list_versions(args):
    """
    Handles the 'list' command to fetch and display versions.
    """
    category = args.category
    if category not in ['current', 'future', 'past', 'android']:
        print(f"Error: Invalid category '{category}'. Choose from 'current', 'future', 'past', 'android'.", file=sys.stderr)
        return

    endpoint = f"versions/{category}"
    data = make_api_request(endpoint)

    if data:
        print(f"--- Roblox Versions: {category.capitalize()} ---")
        if not data:
            print("No data received from the API.")
            return
        
        for key, value in data.items():
            print(f"{key:<12}: {value}")
        print("---------------------------------")

def handle_get_version_string(args):
    """
    Handles the 'get-version-string' command to retrieve a specific version string.
    """
    platform = args.platform.capitalize()
    data = make_api_request("versions/current")

    if data:
        key = 'Windows' if platform.lower() == 'windows' else 'Mac'
        if key in data:
            print(data[key])
        else:
            print(f"Error: Platform '{platform}' not found in the 'current' versions data.", file=sys.stderr)
            print(f"Available platforms: {', '.join(data.keys())}", file=sys.stderr)

def handle_generate_json(args):
    """
    Handles the 'generate-json' command to fetch all data and write to a JSON file.
    """
    print("Fetching all version data from WEAO API...")
    
    endpoints = {
        "current": "versions/current",
        "future": "versions/future",
        "past": "versions/past",
        "android": "versions/android"
    }
    
    all_data = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_endpoint = {executor.submit(make_api_request, ep): name for name, ep in endpoints.items()}
        for future in future_to_endpoint:
            name = future_to_endpoint[future]
            try:
                data = future.result()
                all_data[name] = data if data else {}
            except Exception as exc:
                print(f"'{name}' generated an exception: {exc}", file=sys.stderr)
                all_data[name] = {}

    if not os.path.exists(PUBLIC_DIR):
        os.makedirs(PUBLIC_DIR)
        print(f"Created directory: ./{PUBLIC_DIR}")

    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(all_data, f, indent=4)
        print(f"Successfully wrote updated data to {DATA_FILE}")
    except IOError as e:
        print(f"Error writing to file {DATA_FILE}: {e}", file=sys.stderr)


def main():
    """
    Main function to parse arguments and execute commands.
    """
    parser = argparse.ArgumentParser(
        description="A multitool to fetch Roblox version information using the WEAO API.",
        epilog="Use 'generate-json' to update data for the web UI."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # 'list' command parser
    parser_list = subparsers.add_parser('list', help='List Roblox versions by category in the console.')
    parser_list.add_argument(
        'category',
        choices=['current', 'future', 'past', 'android'],
        help='The category of versions to list.'
    )
    parser_list.set_defaults(func=handle_list_versions)

    # 'get-version-string' command parser
    parser_get = subparsers.add_parser('get-version-string', help='Get a specific version string from the current versions.')
    parser_get.add_argument(
        'platform',
        choices=['Windows', 'Mac'],
        help='The platform (Windows or Mac) to get the version string for.'
    )
    parser_get.set_defaults(func=handle_get_version_string)

    # 'generate-json' command parser
    parser_generate = subparsers.add_parser('generate-json', help='Fetch all data and save it to public/data.json for the UI.')
    parser_generate.set_defaults(func=handle_generate_json)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
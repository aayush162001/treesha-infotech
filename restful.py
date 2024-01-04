import requests
import argparse
import json
import csv

BASE_URL = "https://jsonplaceholder.typicode.com"

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "get":
            response = requests.get(url)
        elif method == "post":
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(data), headers=headers)
        else:
            raise ValueError("Invalid method. Supported methods: get, post")

        response.raise_for_status()  # Check for HTTP errors

        return response.json()

    except requests.exceptions.RequestException as e:
        print("Error making method request to url")
        return None

def save_to_file(data, outfile):
    try:
        if outfile.endswith(".json"):
            with open(outfile, "w") as json_file:
                json.dump(data, json_file, indent=2)
        elif outfile.endswith(".csv"):
            with open(outfile, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            raise ValueError("Invalid output file format. Supported formats: json, csv")

        print("Data successfully saved to outfile")

    except (IOError, ValueError) as e:
        print("Error saving data to outfile")

def restful():
    parser = argparse.ArgumentParser(description="Simple REST client for JSONPlaceholder")
    parser.add_argument("method", choices=["get", "post"], help="HTTP method to use (get or post)")
    parser.add_argument("endpoint", help="URI fragment (e.g., /posts/1)")
    parser.add_argument("-o", "--output", help="Output file (optional)")

    args = parser.parse_args()

    if args.method == "get":
        response_data = make_request(args.method, args.endpoint)
    elif args.method == "post":
        try:
            data = json.loads(input("Enter JSON data for POST request: "))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            return

        response_data = make_request(args.method, args.endpoint, data)

    if response_data is not None and args.output:
        save_to_file(response_data, args.output)
    elif response_data is not None:
        print(json.dumps(response_data, indent=2))

if __name__ == "__main__":
    restful()

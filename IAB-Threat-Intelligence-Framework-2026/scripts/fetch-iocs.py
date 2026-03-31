# sys mod allows access to system-specific parameters and func like CLI arg
import sys
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv('key.env')
API_KEY = os.getenv("OTX_API_KEY")
OTX_BASE_URL = "https://otx.alienvault.com/api/v1/search/pulses/"


# == == REQUEST WRAPPER == == 
# fetch data from API and handle connectivity issues without crashing the script
def data_fetcher(OTX_BASE_URL, headers, params):
    print("\nQuerying OTX Search URL with Keyword: ")
    try:
        # request.get() sends and HTTP GET request to the URL
        response = requests.get(OTX_BASE_URL, headers=headers, params=params)

        # Error Handling: .raise_for_status() checks if the HTTP REQ was successful
        # -- If it returns 4xx or 5xx error code, it raises and exception
        response.raise_for_status()

        # Parsing: .json() parses the raw text of the HTTP response, and convet it in a native python dict
        api_data_dict = response.json()

        print("\n[SUCCESS] API data retrieved and converted to Python dictionary.")


        return api_data_dict
        
    # Error Handling: any HTTP or network realated error makes you safely exit the script upon failure
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Could not fetch data from API: {e}")
        print("\nNote: A 401 error means your API key is invalid or missing. A 404 or 403 means the resource is not found or forbidden.")
        return None



# == == NORMALIZER == ==
# takes the API data and turns it into a clean list of normalized records
# standarized dictionary format for the final report
def normalize_ioc(ioc_raw, pulse_id):
    # flatten tags into a single sting for better CSV compatibility
    tags_list = ioc_raw.get('tags', [])
    tags_string = ", ".join(tags_list)

    # provides a timestamp for when this specific record was collected
    current_time = datetime.now().isoformat()

    # Normalization: Func take one IOC dict and returns a clean, normalized dict
    normalized_record = {
        "collected_at": current_time,
        "source": "AlienVault OTX",
        "pulse_id": pulse_id,
        "ioc_type": ioc_raw.get('type'),
        "ioc_value": ioc_raw.get('indicator'),
        "description": ioc_raw.get('description', 'No description provided'),
        "tags": tags_string,
        "raw_json_link": f"{OTX_BASE_URL}",
    }
    return normalized_record


# == == PROCESSOR == ==
# unpacks the json structures and navigate trough the pulses to build a clean list of records
def result_processor(raw_data):
    clean_iocs = []
    pulses = raw_data.get('results', [])

    for pulse in pulses:
        pulse_id = pulse.get('id', 'N/A')
        indicators = pulse.get('indicators', [])

        for ioc in indicators:
            normalized = normalize_ioc(ioc, pulse_id)
            clean_iocs.append(normalized)

    return clean_iocs


# == == CSV WRITER == ==
# stores clean data in files 
# output a simple confirmation print
def csv_writer(data_list, keyword):
    if not data_list:
        print("No data to write.")
        return
    
    # extract headers from the keys of the first dictionary
    fieldnames = data_list[0].keys()
    filename = f"collected_{keyword}.csv"

    # close the file safely even if an error occurs
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)
    print(f"File saved: {filename}")
    

# manages the secuence of operations.
def main():
    # Checks: CLI arg provided after command
    keyword = None
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        print(f"Keyword supplied: {keyword}")
    else:
        keyword = "malware"
        print("No search keyword provided. Using default")

    print("Threat Intel IOC Fetcher - Running the collection Phase.")

    # --- API Autentication and Params ---
    headers = {'X-OTX-API-KEY': API_KEY}
    params = {'q': keyword, 'limit': 50}

    raw_data = data_fetcher(OTX_BASE_URL, headers, params)
    
    if raw_data is None:
        print("Error: No data received. Aborting")
        return
    
    clean_list = result_processor(raw_data)
    csv_writer(clean_list, keyword)

    

if __name__ == "__main__":
    main()
    


import requests
import json
from pathlib import Path

def dataset_downloading(API_CALL, OPENCITATIONS_ACCESS_TOKEN, save_directory):
    """
    API_CALL: API endpoint for retrieving citation data
    OPENCITATIONS_ACCESS_TOKEN: Access token for authentication
    save_directory: Directory to save the retrieved data
    """
    HTTP_HEADERS = {"authorization": OPENCITATIONS_ACCESS_TOKEN}
    response = requests.get(API_CALL, headers=HTTP_HEADERS)

    if response.status_code == 200:
        citation_data = response.json()

        save_directory.mkdir(parents=True, exist_ok=True)

        output_file = save_directory / 'citation_data.json'

        with open(output_file, 'w') as json_file:
            json.dump(citation_data, json_file, indent=4)

        print(f"Data successfully retrieved and saved to {output_file}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    return


if __name__ == '__main__':

    API_CALL = "https://opencitations.net/index/api/v2/references/doi:10.1186/1756-8722-6-59"
    OPENCITATIONS_ACCESS_TOKEN = "4c73fa44-43a1-4ca4-a907-98e221960e2f"
    save_directory = Path("data")

    dataset_downloading(API_CALL, OPENCITATIONS_ACCESS_TOKEN, save_directory)

    print("Finish running dataset_downloading.py")

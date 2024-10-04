from data_preprocessing import dataset_downloading
from pathlib import Path

if __name__ == '__main__':
    API_CALL = "https://opencitations.net/index/api/v2/references/doi:10.1186/1756-8722-6-59"
    OPENCITATIONS_ACCESS_TOKEN = "4c73fa44-43a1-4ca4-a907-98e221960e2f"
    dataset_save_directory = Path("data")

    dataset_downloading.dataset_downloading(API_CALL, OPENCITATIONS_ACCESS_TOKEN, dataset_save_directory)
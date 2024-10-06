import requests
from pathlib import Path
import tarfile

def download_file(url, target_dir):
    # Ensure the target directory is a Path object
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Extract the filename from the URL and create the full file path
    filename = url.split('/')[-1]
    file_path = target_dir / filename

    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check for HTTP errors

    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded file saved to: {file_path}")
    return file_path  # Return the path to the downloaded file

def untar_file(tar_file, extract_to):
    # Ensure the extract_to directory is a Path object
    extract_to = Path(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)

    # Open the tar.gz file and extract its contents
    with tarfile.open(tar_file, 'r:gz') as tar:
        tar.extractall(path=extract_to)
    print(f"Extracted files to: {extract_to}")
    return

def delete_file(file_path):
    # Ensure the file_path is a Path object
    file_path = Path(file_path)
    if file_path.exists():
        file_path.unlink()  # Deletes the file
        print(f"Deleted file: {file_path}")
    else:
        print(f"File not found to be deleted: {file_path}")
    return

def download_and_extract():
    # The downloaded folder is approximately 1GB.
    AAN_DOWNLOAD_LINK = "https://clair.eecs.umich.edu/aan/downloads/aandec2014.tar.gz"
    target_directory = "data"

    # Download the raw data
    downloaded_file = download_file(AAN_DOWNLOAD_LINK, target_directory)
    untar_file(downloaded_file, target_directory)
    delete_file(downloaded_file)
    return

if __name__ == "__main__":
    download_and_extract()

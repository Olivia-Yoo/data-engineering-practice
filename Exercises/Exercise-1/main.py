import logging
import os
import warnings

from urllib.parse import urlparse
from pathlib import Path

import requests
import zipfile

#from tqdm import tqdm

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def create_downloads_directory(out_dir: str):
    
    downloads_dir = os.path.join(out_dir, "downloads")

    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        logger.info("Successfully created downloads directory in [%s]", out_dir)
    else:
        logger.info("Downloads directory already exists in [%s]", out_dir)

    return downloads_dir


def is_reachable_uri(uri: str) -> bool:
    try:
        response = requests.head(uri, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False


def download_from_uri(uri: str, out_dir: str) -> None:

    # get filename from URI
    filename = os.path.basename(uri)
    out_filename = f"{out_dir}/{filename}"

    # download file
    response = requests.get(uri)
    if response.status_code == 200:
        with open(f"{out_filename}", "wb") as f:
            f.write(response.content)
            logger.info("Successfully downloaded [%s] to [%s]", uri, f"{out_filename}")
    else:
        logger.warning("Failed to download [%s]", uri)


def unzip_file(zip_path: str) -> None:

    # unzip file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_path))
        logger.info("Successfully unzipped [%s]", zip_path )

    # delete zip file
    os.remove(zip_path)


def download_and_unzip_from_uri(uri: str, out_dir: str) -> None:

    # check that URI is valid
    if not is_reachable_uri(uri):
        logger.warning("URI [%s] is not reachable. Skipping download.", uri)
        return
    else:
        logger.info("URI [%s] is valid. Proceeding with download.", uri)

    download_from_uri(uri, out_dir)
    zip_path = f"{out_dir}/{os.path.basename(uri)}"
    unzip_file(zip_path)


def download_and_unzip_from_uris(uri_list: str, out_dir: str):
    n_uris = len(uri_list)

    for i, uri in enumerate(uri_list, start=1):
        logger.info("Processing [ %s / %s ] URI [%s]", i, n_uris, uri)
        download_and_unzip_from_uri(uri, out_dir)


def main():
    setup_logging()
    script_dir = Path(__file__).parent
    downloads_dir = create_downloads_directory(script_dir)
    download_and_unzip_from_uris(download_uris, downloads_dir)


if __name__ == "__main__":
    main()

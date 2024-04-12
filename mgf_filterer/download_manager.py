from pathlib import Path

import requests


def download_file(url: str, dest_folder: Path) -> None:
    """
    Downloads a file from the specified URL and saves it to the destination folder.

    Parameters:
    url (str): URL of the file to download.
    dest_folder (Path): Path object pointing to the destination folder where the file will be saved.

    Raises:
    requests.RequestException: For issues like network problems, invalid URL, etc.
    """
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Extract filename from URL and construct full path
        filename = url.split("/")[-1]
        dest_path = dest_folder / filename

        # Write file to the destination
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"File downloaded successfully: {dest_path}")
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")
        raise


# Example usage
if __name__ == "__main__":
    download_url = "https://external.gnps2.org/gnpslibrary/GNPS-LIBRARY.mgf"
    destination_folder = Path("/path/to/your/destination/folder")
    download_file(download_url, destination_folder)

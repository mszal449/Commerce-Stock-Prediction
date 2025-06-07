import sys
import zipfile
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

from data.data_loader import download_dataset

if __name__ == "__main__":
    try:
        # Download the Store Sales dataset to default location (data/raw)
        download_path = download_dataset()
        print(f"Dataset downloaded successfully to: {download_path}")
        
        # Find and unzip the downloaded file
        download_dir = Path(download_path)
        zip_files = list(download_dir.glob("*.zip"))
        
        if zip_files:
            zip_file = zip_files[0]
            print(f"Unzipping {zip_file.name}...")
            
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(download_dir)
            
            print(f"Files extracted to: {download_dir}")
            print(f"Extracted files: {[f.name for f in download_dir.iterdir() if f.is_file() and not f.name.endswith('.zip')]}")
        else:
            print("No zip files found to extract")
            
    except Exception as e:
        print(f"Error downloading/extracting dataset: {e}")
        sys.exit(1)
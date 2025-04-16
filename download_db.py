import gdown
import os
from pathlib import Path
import json
import logging
import sys
import argparse

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# --- End Logging Setup ---


# --- Configuration ---
# PASTE YOUR GOOGLE DRIVE SHAREABLE LINK HERE
# Make sure the link sharing is set to "Anyone with the link"
# GOOGLE_DRIVE_URL = "https://drive.google.com/file/d/12k2hLxVDriNTj3CnASmzfjc3p8q01msz/view?usp=share_link" # Removed hardcoded URL

# Define the name you want for the downloaded database file
OUTPUT_FILENAME = "DxO_Revenues_Magento_Empilement.db"

# --- Derive Table Name and Config Paths ---
# Derive table name by removing the .db extension
TABLE_NAME = Path(OUTPUT_FILENAME).stem
logging.info(f"Derived table name: {TABLE_NAME}")

# Define where to save the database (e.g., in a 'data' subdirectory)
# This will create the 'data' directory if it doesn't exist
OUTPUT_DB_DIR = Path("data")
OUTPUT_DB_PATH = OUTPUT_DB_DIR / OUTPUT_FILENAME

# Define output directory and filename for the JSON config
OUTPUT_CONFIG_DIR = Path('output')
CLAUDE_CONFIG_FILENAME = f'claude_desktop_config_{TABLE_NAME}.json'
CLAUDE_CONFIG_FILE_PATH = OUTPUT_CONFIG_DIR / CLAUDE_CONFIG_FILENAME
# --- End Configuration ---

def create_claude_config(db_abs_path: str, config_output_path: Path, table_name: str):
    """Creates the Claude Desktop JSON configuration file."""
    logging.info(f"Attempting to create Claude Desktop config file at {config_output_path.resolve()}...")

    # Construct the JSON data structure
    claude_config_data = {
        "mcpServers": {
            f"sqlite_db_{table_name}": { # Use table name in the server key
                "command": "uvx",
                "args": ["--from", "mcp-alchemy", "mcp-alchemy"],
                "env": {
                    # Use the absolute path to the downloaded DB
                    "DB_URL": f"sqlite:///{db_abs_path}"
                }
            }
        }
    }

    try:
        # Ensure the output directory exists
        logging.info(f"Ensuring output directory exists: {config_output_path.parent.resolve()}")
        config_output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_output_path, 'w', encoding='utf-8') as f:
            json.dump(claude_config_data, f, indent=2) # Use json.dump for proper formatting
        logging.info(f"Successfully saved Claude Desktop config to: {config_output_path.resolve()}")
        return True
    except Exception as e:
        logging.error(f"Could not save Claude Desktop config to file '{config_output_path.resolve()}': {e}", exc_info=True)
        return False


def download_database(url: str, output_db_path: Path):
    """
    Downloads the database file from the specified Google Drive URL.
    Returns the absolute path of the downloaded file if successful, else None.
    """
    logging.info(f"Attempting to download database from Google Drive...")
    logging.info(f"URL: {url}")

    if url == "YOUR_GOOGLE_DRIVE_SHAREABLE_LINK_HERE":
        logging.error("Please paste your actual Google Drive shareable link into the GOOGLE_DRIVE_URL variable in this script!")
        return None

    try:
        # Create the output directory if it doesn't exist
        logging.info(f"Ensuring database directory exists: {output_db_path.parent.resolve()}")
        output_db_path.parent.mkdir(parents=True, exist_ok=True)

        logging.info(f"Downloading database to: {output_db_path.resolve()}")

        # Use gdown to download the file from the URL
        # quiet=False ensures the progress bar is shown by gdown
        gdown.download(url, str(output_db_path), quiet=False, fuzzy=True)

        if output_db_path.exists():
            db_abs_path = str(output_db_path.resolve())
            logging.info(f"Successfully downloaded database to {db_abs_path}")
            return db_abs_path
        else:
            # This case might be less likely if gdown doesn't raise an exception, but good to keep
            logging.error("Download command completed, but the output file was not found.")
            return None

    except Exception as e:
        logging.error(f"An error occurred during download: {e}", exc_info=True)
        logging.error("Please check:")
        logging.error("1. Your internet connection.")
        logging.error("2. The Google Drive URL is correct and accessible ('Anyone with the link').")
        logging.error("3. You have permissions to write to the target directory.")
        return None

if __name__ == "__main__":
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Download a database from Google Drive and generate a Claude Desktop config.")
    parser.add_argument("google_drive_url", help="The shareable Google Drive URL for the database file.")
    args = parser.parse_args()
    GOOGLE_DRIVE_URL = args.google_drive_url # Get URL from args
    # --- End Argument Parsing ---

    logging.info("--- Starting Database Download and Config Script ---")
    # Pass the URL from args to the download function
    downloaded_db_path = download_database(GOOGLE_DRIVE_URL, OUTPUT_DB_PATH)

    config_created = False
    if downloaded_db_path:
        logging.info("Database download process finished successfully.")
        if create_claude_config(downloaded_db_path, CLAUDE_CONFIG_FILE_PATH, TABLE_NAME):
             logging.info("Claude config generation finished successfully.")
             config_created = True
        else:
            logging.error("Claude config generation failed. Exiting.")
            sys.exit(1)
    else:
        logging.error("Database download process failed. Exiting.")
        sys.exit(1)

    # --- Final Summary and Instructions ---
    if downloaded_db_path and config_created:
        logging.info("--- Script Finished Successfully ---")
        logging.info(f"Database file saved to: {OUTPUT_DB_PATH.resolve()}")
        logging.info(f"Claude Desktop config saved to: {CLAUDE_CONFIG_FILE_PATH.resolve()}")

        # Print the generated JSON config
        try:
            with open(CLAUDE_CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                config_content = f.read()
            print("\n" + "-" * 15 + " Claude Desktop MCP Configuration " + "-" * 15)
            print(config_content) # Print the raw JSON string
            print("-" * (30 + len(" Claude Desktop MCP Configuration ")) + "\n")
            print("Instructions for Claude Desktop:")
            print("1. Open Claude Desktop settings -> developers -> edit config")
            print("2. Copy the JSON configuration printed above.")
            print("3. Paste it into the config file.")
            print("-" * (30 + len(" Claude Desktop MCP Configuration "))) # Match the top border

        except Exception as e:
            logging.error(f"Failed to read and print the generated config file: {e}", exc_info=True)

    # No need for a final success log here as it's conditional above 
# MCP SQL Database Setup for Claude Desktop

This repository provides scripts to automatically download the required SQLite database and generate the necessary configuration for using it with Claude Desktop via the `mcp-alchemy` MCP server.

## Prerequisites

1.  **Git:** You need Git installed to clone this repository.
2.  **Python:** Python 3.8 or newer is recommended.
3.  **uv:** The `mcp-alchemy` server used by Claude Desktop requires `uv` to be installed. If you don't have it, install it globally by running the following command in your terminal:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    *Note: You might need to restart your terminal after installing `uv` for the command to be recognized.*

## Setup Instructions

1.  **Clone the Repository:**
    Open your terminal and clone this repository:
    ```bash
    git clone git@github.com:DxO-AI-Dep/DxO-MCP-SQL-BI-INSTALLER.git # Replace with the actual URL
    cd DxO-MCP-SQL-BI-INSTALLER # e.g., cd DxO-MCP-SQL
    ```

2.  **Run the Setup Script:**
    Execute the setup script, **providing the shareable Google Drive link for the database file as a command-line argument.** This will create a local Python environment, install required packages, download the database, and generate the Claude Desktop configuration.

    Replace `"YOUR_GOOGLE_DRIVE_SHAREABLE_LINK_HERE"` with the actual link (make sure it's shared with "Anyone with the link").

    ```bash
    bash setup.sh "YOUR_GOOGLE_DRIVE_SHAREABLE_LINK_HERE"
    ```

3.  **Configure Claude Desktop:**
    *   After the `setup.sh` script finishes successfully, it will print the necessary JSON configuration block for the MCP server. **Copy this entire JSON block.**

        Here is an example of what the output JSON block might look like (the `DB_URL` path will reflect your local setup):

        ```json
        {
          "mcpServers": {
            "sqlite_db_DxO_Revenues_Magento_Empilement": {
              "command": "uvx",
              "args": [
                "--from",
                "mcp-alchemy",
                "mcp-alchemy"
              ],
              "env": {
                "DB_URL": "sqlite:////path/to/your/repository/DxO-MCP-SQL-BI-INSTALLER/data/DxO_Revenues_Magento_Empilement.db"
              }
            }
          }
        }
        ```

    *   Open Claude Desktop.
    *   Click on the **Claude** menu in the menu bar (top-left of your screen) and select **Settings...** (or use the shortcut `⌘,`).
        ![Claude Menu](images/quickstart-menu.png)
    *   In the Settings window, click on **Developer** in the left-hand sidebar.
        ![Developer Settings](images/quickstart-developer.png)
    *   Click the **Edit Config** button. This will open the `claude_desktop_config.json` file in your default text editor. The file is located at:
        *   **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
        *   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
    *   If the file already contains content (like `{"mcpServers": { ... }}`), carefully paste the JSON block you copied from the script *inside* the existing `mcpServers` object, ensuring it's a valid JSON structure (pay attention to commas between server entries if others exist). If the file is empty or doesn't have `mcpServers`, you might need to wrap the copied block within `{ "mcpServers": { ... } }`. **The setup script provides the exact block to add.**
    *   **Save the `claude_desktop_config.json` file.**
    *   **Restart Claude Desktop** completely for the changes to take effect.

4.  **Use the Database in Claude:**
    *   After restarting, **ensure you are in the correct project** configured by Arthur, named **"DxO BI Data Analyst"**.
        ![Select Project](images/project_bi.png)
    *   You should see a hammer icon (🔨) in the bottom right of the chat input box. Click it to see available tools/servers, including the newly added database server (e.g., `sqlite_db_DxO_Revenues_Magento_Empilement`).
        ![MCP Enabled](images/mcp-enabled-project.png)

## How it Works

*   The `setup.sh` script automates the creation of a Python virtual environment (`.venv`) and installs dependencies from `requirements.txt`.
*   It then runs `download_db.py`, which:
    *   Downloads the necessary SQLite database file (`.db`) from Google Drive into the `data/` directory.
    *   Generates a JSON configuration file (`.json`) in the `output/` directory, pointing to the downloaded database.
*   The `mcp-alchemy` server itself is installed and run *dynamically by Claude Desktop* using `uvx` when you select the configured MCP server. You do not need to install it manually. 
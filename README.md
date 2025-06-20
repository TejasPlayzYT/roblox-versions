# WEAO Roblox Version Checker & UI

A command-line multitool and web UI to fetch and display information about various Roblox client versions using the official WEAO.xyz API.

This tool can retrieve the latest, future, and past (downgradable) version strings for the Windows and Mac clients, as well as the latest version for Android. The data can be viewed directly in the console or through a clean, modern web interface.

**Disclaimer:** This tool is for informational purposes only. The WEAO API, as documented publicly, does not provide direct download links for Roblox clients.

## Features

-   **Dual Interface**: Use the tool via the command line or view the data in a web UI.
-   **Comprehensive Data**: Fetches current, future, past, and Android Roblox version strings.
-   **Modern UI**: Clean, responsive, dark-themed UI with a custom cursor.
-   **Simple Sync**: A single command (`generate-json`) updates the data for the frontend.
-   **Lightweight**: Requires only Python and the `requests` library.

## Prerequisites

-   Python 3.6+
-   `pip` for installing packages
-   A modern web browser

## Setup

1.  **Clone the repository or download the files.**

2.  **Navigate to the project directory:**
    ```bash
    cd /path/to/project
    ```

3.  **Create and activate a virtual environment (recommended):**
    -   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

### 1. Update the Data

To populate the web UI, you must first fetch the data from the WEAO API. Run the following command in your terminal:

```bash
python roblox_version_checker.py generate-json
```

If an error resulted from this, verify your python installation or repair files from the GitHub.

Note that data from version-9bf2d7ce6a0345d5 is already present in the public/data.json file, so you can skip this step if you're using that version.

### 2. Run the Local Server

To run the local server, navigate to the project directory and run the following command:

```bash
python -m http.server --directory public 8000
```

This will start a local server on port 8000 and serve the files from the `public` directory.

### 3. Access the Web UI

Open your web browser and navigate to `http://localhost:8000` to view the web UI.

### Updating Web UI

To update the web UI, run the following command in your terminal:

```bash
python roblox_version_checker.py generate-json
```

This will update the data for the web UI.
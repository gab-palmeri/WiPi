# WiPi

**A lightweight web interface and startup script to manage Wi-Fi and monitor system metrics on Raspberry Pi, with automatic fallback to hotspot mode.**

## Overview

WiPi is a minimal Flask-based web application designed to run locally on a Raspberry Pi. It allows users to:

- Manage Wi-Fi connections via a browser
- Enable Access Point (AP) mode as a fallback or manually
- View a dashboard with key system stats: IP address, CPU load, RAM usage, temperature, and running Docker containers

The web interface is protected by a basic authentication layer, providing minimal security suitable for local network use.

## Features

- **Wi-Fi Manager**: View, connect, delete or switch between networks
- **Access Point Mode**: Fallback to AP if no connection is available
- **System Dashboard**: Real-time info on the Raspberry Pi
- **Docker Monitoring**: Lists all running Docker containers
- **Auto Startup Script**: Starts Flask server and enables hotspot if needed

## Project Structure

```
└── ./
    ├── static/           # CSS and JS files for the web app
    │   ├── css/
    │   ├── js/
    ├── templates/        # HTML templates for the web app
    │   ├── dashboard.html
    │   ├── layout.html
    │   ├── login.html
    │   └── wifi.html
    ├── utils/            # Python utility scripts
    │   ├── system.py     # Fetches system information
    │   └── wifi.py       # Manages Wi-Fi and Access Point functionalities
    ├── .env.example      # Example environment variables file
    ├── .gitignore        
    ├── app.py            # Main Flask application
    ├── wipi.sh           # Startup script to manage Wi-Fi and run the Flask server
    ├── handlers.py       # Handles Wi-Fi related requests for Flask routes
    └── requirements.txt  # Python dependencies
```
## How It Works

1. **Startup script (`wipi.sh`)** runs at boot:
   - Checks if a Wi-Fi connection is active via `nmcli`
   - If not connected, enables Access Point mode via `nmcli dev wifi hotspot`
   - Regardless of connection status, launches the Flask web server

2. **Web App (`app.py`)**:
   - Handles routing and basic authentication
   - Uses functions in `handlers.py` to respond to Wi-Fi actions
   - Renders templates from `/templates` and loads CSS and JS from `/static`

3. **Utils Module**:
   - `system.py`: Executes shell commands to fetch system info
   - `wifi.py`: Handles nmcli commands for Wi-Fi/AP management
   
## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gab-palmeri/WiPi
    cd WiPi
    ```

2.  **Install Python dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file based on `.env.example` and set your desired ENV variables:
    ```bash
    cp .env.example .env
    nano .env
    ```
    The variables are:
    - `USERNAME`: Username for basic authentication
    - `PASSWORD`: Password for basic authentication
    - `AP_NAME`: SSID for the Access Point
    - `AP_PASS`: Password for the Access Point
    - `SECRET_KEY`: Secret key for Flask sessions (can be any random string)


## Running the Application

- **Option 1: Execute the startup script with fallback hotspot:**
    ```bash
    chmod +x wipi.sh
    ./wipi.sh
    ```
- **Option 2: Run the Flask app directly:**
    ```bash
    source venv/bin/activate
    python app.py
    ```

## Automatic Startup on Boot via systemd

To automatically start WiPi on boot, follow these steps:

1.  **Create a systemd service file:**
    ```bash
    sudo nano /etc/systemd/system/wipi.service
    ```

2.  **Paste the following content into the file:**
    ```ini
    [Unit]
    Description=WiPi - Fallback Hotspot and Flask Web Server
    After=network-online.target
    Wants=network-online.target

    [Service]
    ExecStart=/bin/bash /path/to/wipi/wipi.sh
    User=root
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Enable and start the service:**
    ```bash
    sudo systemctl enable wipi.service
    sudo systemctl start wipi.service
    ```
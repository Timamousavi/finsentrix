# Installation Guide

## Windows Installation

### Option 1: Using the Installer (Recommended)
1. Download the latest installer from [Releases](https://github.com/Timamousavi/finsentrix/releases)
2. Run `FinSentrix-Setup.exe`
3. Follow the installation wizard
4. Launch FinSentrix from the Start Menu or desktop shortcut

### Option 2: Using pip
1. Open Command Prompt
2. Install using pip:
   ```bash
   pip install finsentrix
   ```
3. Run the application:
   ```bash
   finsentrix
   ```

## Web Application

### Option 1: Using Docker (Recommended)
1. Install [Docker](https://www.docker.com/products/docker-desktop)
2. Pull the image:
   ```bash
   docker pull timamousavi/finsentrix
   ```
3. Run the container:
   ```bash
   docker run -p 8000:8000 timamousavi/finsentrix
   ```
4. Access the web interface at `http://localhost:8000`

### Option 2: Local Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Timamousavi/finsentrix.git
   cd finsentrix
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   ```
4. Access the web interface at `http://localhost:8000`

## System Requirements

### Windows Application
- Windows 10 or later
- 4GB RAM minimum
- 2GB free disk space
- Internet connection

### Web Application
- Python 3.9 or later
- 4GB RAM minimum
- 2GB free disk space
- Modern web browser
- Internet connection

## Troubleshooting

### Common Issues

1. **Installation Fails**
   - Ensure you have administrator privileges
   - Check if antivirus is blocking the installation
   - Verify system requirements are met

2. **Application Won't Start**
   - Check if all dependencies are installed
   - Verify Python version (3.9 or later)
   - Check system requirements

3. **Web Interface Not Accessible**
   - Verify the server is running
   - Check if port 8000 is available
   - Ensure firewall allows the connection

### Getting Help

For installation support:
- Email: support@finsentrix.com
- Documentation: https://docs.finsentrix.com
- Issues: https://github.com/Timamousavi/finsentrix/issues 
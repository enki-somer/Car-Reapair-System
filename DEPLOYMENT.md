# Deployment Guide

## Building with PyInstaller

### Prerequisites

```bash
# Install PyInstaller
pip install pyinstaller

# Or install all development requirements
pip install -r requirements-dev.txt
```

### Building the Executable

```bash
# Build using spec file
pyinstaller mahalli.spec

# The executable will be in dist/mahalli/
```

### Installation from Executable

#### Windows

1. Copy the entire `dist/mahalli` folder to desired location
2. Create shortcut to `mahalli.exe`
3. (Optional) Add to Start Menu

#### Linux

1. Copy the executable and resources:

```bash
sudo cp -r dist/mahalli /opt/
sudo chmod +x /opt/mahalli/mahalli
```

2. Create symbolic link:

```bash
sudo ln -s /opt/mahalli/mahalli /usr/local/bin/mahalli
```

3. Install desktop file:

```bash
sudo cp auto-parts-manager.desktop /usr/share/applications/
```

## Running the Application

### Windows

- Double click `mahalli.exe`
- Or run from command prompt: `mahalli.exe`

### Linux

- Run from terminal: `mahalli`
- Or launch from application menu

## Logging Location

### Windows

Logs are stored in:

- `%APPDATA%\mahalli\logs\`

### Linux

Logs are stored in:

- `/var/log/mahalli/`

## Troubleshooting

### Common Issues

1. Missing DLLs (Windows)

   - Ensure the entire dist folder is copied
   - Install Visual C++ Redistributable if needed

2. Permission Issues (Linux)

   - Check log directory permissions
   - Ensure executable has proper permissions

3. Icon Not Showing
   - Verify icons folder is in correct location
   - Check file permissions

### Debugging

For detailed error messages, run from terminal:

```bash
# Windows
dist\mahalli\mahalli.exe --debug

# Linux
/opt/mahalli/mahalli --debug
```

## Building the Package

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install build requirements
pip install build wheel

# Build the package
python -m build

# The package will be available in dist/
```

## Installation

### System Requirements

- Python 3.8 or higher
- Qt 5.15 or higher
- SQLite 3.30 or higher

### From Package

```bash
pip install mahalli-1.0.0.tar.gz
```

### From Source

```bash
pip install -e .
```

## Post-Installation

1. Create required directories:

```bash
sudo mkdir -p /usr/share/icons/mahalli
sudo mkdir -p /var/log/mahalli
```

2. Copy application icon:

```bash
sudo cp icons/mahalli.png /usr/share/icons/mahalli/
```

3. Set permissions:

```bash
sudo chown -R $USER:$USER /var/log/mahalli
```

## Running the Application

```bash
# From command line
mahalli

# Or from desktop environment
# The application will appear in the Office category
```

## Logging and Monitoring

Logs are stored in:

- /var/log/mahalli/mahalli.log
- /var/log/mahalli/error.log

## Updating

1. Stop the application
2. Backup the database
3. Install the new version
4. Run database migrations
5. Restart the application

## Troubleshooting

See logs for detailed error messages:

```bash
tail -f /var/log/mahalli/error.log
```

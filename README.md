# Mahalli - نظام إدارة قطع غيار السيارات

<div dir="rtl">
نظام متكامل لإدارة محلات قطع غيار السيارات يشمل إدارة المخزون، المبيعات، الموظفين والتقارير
</div>

## Features

### Inventory Management

- Track auto parts inventory and stock levels
- Manage part details, pricing, and categories
- Low stock alerts and notifications
- Barcode scanning support
- Track part locations and suppliers

### Sales Management

- Process sales transactions
- Generate invoices and receipts
- Calculate profits and margins
- Track customer information
- Manage returns and exchanges

### Employee Management

- Employee information and records
- Attendance tracking
- Work schedules
- Performance tracking
- Salary management

### Reporting

- Daily and monthly sales reports
- Inventory reports
- Employee attendance reports
- Profit/loss analysis
- Export to Excel/CSV formats
- Print detailed reports

## System Requirements

### Minimum Requirements

- Operating System: Windows 10/11 or Linux (Ubuntu 20.04+)
- Processor: 2.0 GHz dual-core
- Memory: 4GB RAM
- Storage: 500MB free space
- Display: 1366x768 resolution

### Software Requirements

- Python 3.8 or higher
- Qt 5.15 or higher
- SQLite 3.30 or higher

## Installation

### Windows Installation

1. Download the latest release from the releases page
2. Run the installer: `mahalli-setup.exe`
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### Linux Installation

#### Using Package Manager

```bash
# Add repository
sudo add-apt-repository ppa:mahalli/stable
sudo apt update

# Install package
sudo apt install mahalli
```

#### Manual Installation

```bash
# Install dependencies
sudo apt install python3-pip python3-qt5 sqlite3

# Install Mahalli
pip3 install mahalli
```

### Installing from Source

```bash
# Clone repository
git clone https://github.com/yourusername/mahalli.git
cd mahalli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Configuration

### Application Settings

- Configuration file: `config/settings.ini`
- Database settings: `config/database.ini`
- Logging settings: `config/logging_config.py`

### Directory Structure

```
mahalli/
├── gui/                # User interface modules
├── database/          # Database models and setup
├── config/           # Configuration files
├── icons/            # Application icons
├── logs/            # Log files
└── tests/           # Test files
```

## Usage

### Starting the Application

```bash
# From command line
mahalli

# Or run executable directly
./mahalli  # Linux
mahalli.exe  # Windows
```

### First Time Setup

1. Launch the application
2. Create admin account
3. Configure initial settings
4. Add inventory items
5. Set up employee accounts

### Basic Operations

1. **Inventory Management**

   - Add new parts
   - Update stock levels
   - Set pricing
   - Manage categories

2. **Sales**

   - Process sales
   - Generate invoices
   - Handle returns
   - Track transactions

3. **Employee Management**

   - Add employees
   - Track attendance
   - Manage schedules
   - Process payroll

4. **Reports**
   - Generate daily reports
   - View monthly summaries
   - Export data
   - Print reports

## Development

### Setting up Development Environment

```bash
# Install development requirements
pip install -r requirements-dev.txt

# Install test requirements
pip install -r tests/requirements-test.txt
```

### Building from Source

```bash
# Using PyInstaller
pyinstaller mahalli.spec

# Or using build script
python build.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_inventory.py
```

## Deployment

### Windows Deployment

1. Build executable using PyInstaller
2. Create installer using Inno Setup
3. Distribute installer

### Linux Deployment

1. Create .deb package
2. Set up repository
3. Deploy to package manager

### Docker Deployment

```bash
# Build image
docker build -t mahalli .

# Run container
docker run -d -p 8080:8080 mahalli
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**

   - Check database file permissions
   - Verify connection settings
   - Ensure SQLite is installed

2. **UI Display Issues**

   - Update Qt libraries
   - Check display resolution
   - Verify icon files exist

3. **Performance Issues**
   - Check system resources
   - Optimize database queries
   - Clear temporary files

### Logging

Log files are located at:

- Windows: `%APPDATA%\mahalli\logs\`
- Linux: `/var/log/mahalli/`

## Support

- GitHub Issues: [Report bugs](https://github.com/yourusername/mahalli/issues)
- Documentation: [Wiki](https://github.com/yourusername/mahalli/wiki)
- Email Support: support@mahalli.com

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PyQt5 team for the GUI framework
- SQLite team for the database engine
- All contributors and testers

## Version History

- 1.0.0 (2024-03-XX)
  - Initial release
  - Basic functionality implemented
  - Core features stable

## Contact

- Project Maintainer: Your Name
- Email: your.email@example.com
- Website: https://mahalli.com

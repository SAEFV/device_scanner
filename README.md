# Device ID Scanner

A CLI tool for scanning device IDs and checking them against a CSV inventory list.

## Features

- Fast lookup of device IDs from CSV inventory
- Color-coded visual feedback (green = found, red = not found)
- Displays device details when found (Prefix, Merk, Type, MAC address)
- Session summary statistics
- Clear screen functionality

## Usage

### Basic usage:
```bash
python3 device_scanner.py <path/to/inventory.csv>
```

### Examples:
```bash
# Using hp_laptops.csv in current directory
python3 device_scanner.py hp_laptops.csv

# Using a CSV file in a different location
python3 device_scanner.py /path/to/inventory/devices.csv
```

### Make it executable (optional):
```bash
chmod +x device_scanner.py
./device_scanner.py hp_laptops.csv
```

## CSV File Format

The CSV file must have the following columns:
- **Prefix**: Device prefix (e.g., "SL")
- **Object ID**: 6-digit device ID (e.g., "051284")
- **Merk**: Brand (e.g., "HP")
- **Type**: Device model/type
- **MAC-adres**: MAC address

Example:
```csv
Prefix,Object ID,Merk,Type,MAC-adres
SL,051284,HP,450_I5_G8_1135G7(Probook),A1B2C3D4E5F6
SL,051301,HP,450_I5_G8_1135G7(Probook),A1B2C3D4E5F7
```

## During Scanning

1. The tool will display the inventory file name and total device count
2. Scan a device by entering its Object ID (e.g., "051284")
3. The tool will immediately display whether the device is found or not
4. Continue scanning - the tool is ready for the next input immediately

### Commands:
- Type device ID and press Enter to scan
- Type `quit` or `exit` to stop scanning
- Type `clear` to clear the screen
- Press `Ctrl+C` to interrupt

## Output

### Device Found (Green):
```
Scanned ID: 051284
✓ STATUS: DEVICE FOUND IN INVENTORY
├─ Prefix: SL
├─ Merk: HP
├─ Type: 450_I5_G8_1135G7(Probook)
└─ MAC: A1B2C3D4E5F6
```

### Device Not Found (Red):
```
Scanned ID: 999999
✗ STATUS: DEVICE NOT IN INVENTORY
```

### Session Summary:
At the end of the session, you'll see:
- Total scans performed
- Number of devices found
- Number of devices not found

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)
- Terminal with ANSI color support (most modern terminals)

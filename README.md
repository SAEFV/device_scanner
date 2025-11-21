# Device ID Scanner

A CLI tool for scanning device IDs and checking them against a CSV inventory list.

## Features

- **Auto-submit on 6 digits** - No need to press Enter! Scanner automatically processes when you type/scan 6 digits
- Fast lookup of device IDs from CSV inventory
- Color-coded visual feedback (green = found, red = not found)
- Displays device details when found (Prefix, Merk, Type, MAC address)
- Session summary statistics
- Clear screen functionality
- Backspace support for corrections

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
2. Type or scan a device ID (e.g., "051284")
3. **Auto-submit**: When you enter exactly 6 digits, the scan processes automatically - no Enter needed!
4. The result displays immediately with color-coded feedback
5. The tool is ready for your next scan right away

### Auto-Submit Feature

- **6-digit IDs**: Automatically submit when you type/scan the 6th digit
- **No Enter needed**: Saves time for rapid scanning operations
- **Backspace works**: Press Backspace to correct mistakes before the 6th digit
- **Manual Enter**: Still works if you prefer, or for commands

### Commands:
- Type a 6-digit device ID (auto-submits, no Enter needed)
- Type `quit` or `exit` then press Enter to stop
- Type `clear` then press Enter to clear the screen
- Press `Ctrl+C` to interrupt at any time

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
- Linux/Unix system (for auto-submit feature)
- No external dependencies (uses only standard library)
- Terminal with ANSI color support (most modern terminals)

**Note:** The auto-submit feature uses `termios` and `tty` modules, which are standard on Linux/Unix. On non-interactive terminals (piped input), the tool automatically falls back to regular input mode.

## Performance

- **Lookup Speed:** O(1) constant time using Python sets
- **Memory Usage:** Minimal - entire inventory loaded into memory for instant lookups
- **Scalability:** Can handle thousands of devices efficiently
- **Scan Speed:** Auto-submit enables ultra-fast scanning workflow

## Tips for Rapid Scanning

1. **Use a barcode scanner** that outputs 6-digit codes - they'll auto-submit instantly
2. Keep the terminal window visible while scanning
3. If you make a mistake, press Backspace before entering the 6th digit
4. Use the `clear` command to refresh the screen if needed
5. Session statistics help track scanning progress

## Workflow Example

```bash
$ python3 device_scanner.py hp_laptops.csv

============================================================
         DEVICE ID SCANNER
============================================================
Inventory File: hp_laptops.csv
Total Devices: 29
Auto-submit enabled: Scans 6-digit IDs automatically
Type 'quit' or 'exit' to stop, 'clear' to clear screen
============================================================

Scan Device ID: 051284
                    ↑↑↑ Auto-submits here (6th digit entered)

Scanned ID: 051284
✓ STATUS: DEVICE FOUND IN INVENTORY
├─ Prefix: SL
├─ Merk: HP
├─ Type: 450_I5_G8_1135G7(Probook)
└─ MAC: A1B2C3D4E5F6
------------------------------------------------------------

Scan Device ID: 999999
                    ↑↑↑ Auto-submits here

Scanned ID: 999999
✗ STATUS: DEVICE NOT IN INVENTORY
------------------------------------------------------------

Scan Device ID: quit
[Press Enter]

============================================================
SCAN SESSION SUMMARY
============================================================
Total Scans: 2
Devices Found: 1
Devices Not Found: 1
============================================================
```

## Troubleshooting

**Q: Auto-submit isn't working?**
- Make sure you're running in an interactive terminal (not piped/redirected input)
- The feature requires Linux/Unix with tty support
- For testing with piped input, the tool falls back to regular input mode

**Q: Can I still use Enter manually?**
- Yes! Enter always works for any input length or command

**Q: What if I make a typo?**
- Press Backspace to delete characters before reaching 6 digits
- After 6 digits are entered, the scan is submitted immediately

#!/usr/bin/env python3
"""
Device ID Scanner - Check scanned device IDs against CSV inventory
Usage: python3 device_scanner.py <csv_file>
"""

import csv
import sys
import os
import tty
import termios
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def get_scanner_input(prompt, auto_submit_length=6):
    """
    Get input character by character and auto-submit when reaching specified length.
    Supports backspace and manual enter for special commands.
    Falls back to regular input if not in an interactive terminal.
    """
    # Check if stdin is a terminal (tty)
    if not sys.stdin.isatty():
        # Fallback to regular input for piped/redirected input
        return input(prompt).strip()

    print(prompt, end='', flush=True)

    # Get terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        user_input = ""

        while True:
            char = sys.stdin.read(1)

            # Handle Ctrl+C
            if char == '\x03':
                raise KeyboardInterrupt

            # Handle Ctrl+D (EOF)
            if char == '\x04':
                raise EOFError

            # Handle Enter
            if char in ['\r', '\n']:
                print()  # New line
                return user_input.strip()

            # Handle Backspace (both ASCII 127 and 8)
            if char in ['\x7f', '\x08']:
                if user_input:
                    user_input = user_input[:-1]
                    # Move cursor back, print space, move back again
                    print('\b \b', end='', flush=True)
                continue

            # Handle printable characters
            if char.isprintable():
                user_input += char
                print(char, end='', flush=True)

                # Auto-submit when reaching target length (if all digits)
                if len(user_input) == auto_submit_length and user_input.isdigit():
                    print()  # New line
                    return user_input.strip()

    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def load_inventory(csv_file):
    """Load device IDs from CSV file into a set for fast lookup"""
    device_ids = set()
    device_details = {}

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                object_id = row.get('Object ID', '').strip()
                if object_id:
                    device_ids.add(object_id)
                    device_details[object_id] = {
                        'prefix': row.get('Prefix', '').strip(),
                        'merk': row.get('Merk', '').strip(),
                        'type': row.get('Type', '').strip(),
                        'mac': row.get('MAC-adres', '').strip()
                    }
        return device_ids, device_details
    except FileNotFoundError:
        print(f"{Colors.RED}Error: CSV file '{csv_file}' not found{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Error loading CSV: {e}{Colors.END}")
        sys.exit(1)

def display_header(csv_file, total_devices):
    """Display scanner header with inventory info"""
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}         DEVICE ID SCANNER{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Inventory File:{Colors.END} {csv_file}")
    print(f"{Colors.BLUE}Total Devices:{Colors.END} {total_devices}")
    print(f"{Colors.YELLOW}Auto-submit enabled: Scans 6-digit IDs automatically{Colors.END}")
    print(f"{Colors.YELLOW}Type 'quit' or 'exit' to stop, 'clear' to clear screen{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def display_result(scanned_id, found, details=None):
    """Display scan result with visual feedback"""
    print(f"\n{Colors.BOLD}Scanned ID: {scanned_id}{Colors.END}")

    if found:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ STATUS: DEVICE FOUND IN INVENTORY{Colors.END}")
        if details:
            print(f"{Colors.GREEN}├─ Prefix: {details['prefix']}{Colors.END}")
            print(f"{Colors.GREEN}├─ Merk: {details['merk']}{Colors.END}")
            print(f"{Colors.GREEN}├─ Type: {details['type']}{Colors.END}")
            print(f"{Colors.GREEN}└─ MAC: {details['mac']}{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ STATUS: DEVICE NOT IN INVENTORY{Colors.END}")

    print(f"{Colors.CYAN}{'-'*60}{Colors.END}\n")

def main():
    # Check for required CSV file argument
    if len(sys.argv) < 2:
        print(f"{Colors.RED}{Colors.BOLD}Error: CSV file path required{Colors.END}")
        print(f"{Colors.YELLOW}Usage: python3 device_scanner.py <csv_file>{Colors.END}")
        print(f"{Colors.YELLOW}Example: python3 device_scanner.py hp_laptops.csv{Colors.END}")
        sys.exit(1)

    csv_file = sys.argv[1]

    # Load inventory
    print(f"{Colors.YELLOW}Loading inventory...{Colors.END}")
    device_ids, device_details = load_inventory(csv_file)

    # Clear screen and show header
    clear_screen()
    display_header(csv_file, len(device_ids))

    # Main scanning loop
    scan_count = 0
    found_count = 0

    try:
        while True:
            # Get input with auto-submit on 6 digits
            try:
                user_input = get_scanner_input(f"{Colors.BOLD}Scan Device ID: {Colors.END}")
            except EOFError:
                break

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            # Clear screen command
            if user_input.lower() == 'clear':
                clear_screen()
                display_header(csv_file, len(device_ids))
                continue

            # Skip empty input
            if not user_input:
                continue

            # Process the scanned ID
            scanned_id = user_input.strip()
            scan_count += 1

            # Check if ID exists in inventory
            if scanned_id in device_ids:
                found_count += 1
                display_result(scanned_id, True, device_details[scanned_id])
            else:
                display_result(scanned_id, False)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Scanner interrupted by user{Colors.END}")

    # Display summary
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}SCAN SESSION SUMMARY{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"Total Scans: {scan_count}")
    print(f"Devices Found: {Colors.GREEN}{found_count}{Colors.END}")
    print(f"Devices Not Found: {Colors.RED}{scan_count - found_count}{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

if __name__ == '__main__':
    main()

import socket
import time
from datetime import datetime

def scan_port(target, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            return result == 0  # 0 means the port is open
    except socket.gaierror:
        raise
    except socket.error as error:
        raise OSError(f"Could not connect to server: {target}") from error

def validate_ports(start_port, end_port):
    if not (0 < start_port <= 65535 and 0 < end_port <= 65535):
        raise ValueError("Ports must be between 1 and 65535")
    if start_port > end_port:
        raise ValueError("Start port must be <= end port")

def parse_ports(port_input):
    port_input = port_input.strip()
    if not port_input:
        raise ValueError("Port input cannot be blank")

    if "-" in port_input:
        parts = port_input.split("-")
        if len(parts) != 2:
            raise ValueError("Use a range such as 1-1000")
        start_port, end_port = (int(part.strip()) for part in parts)
        validate_ports(start_port, end_port)
        return list(range(start_port, end_port + 1))

    ports = []
    for value in port_input.split(","):
        port = int(value.strip())
        validate_ports(port, port)
        ports.append(port)

    return sorted(set(ports))

def run_scan(target, ports, timeout=1, delay=0.05):
    if not target.strip():
        raise ValueError("Target cannot be blank")
    if timeout <= 0:
        raise ValueError("Timeout must be greater than 0")
    if delay < 0:
        raise ValueError("Delay cannot be negative")
    if not ports:
        raise ValueError("At least one port is required")
    print(f"[*] Starting scan on {target} at {datetime.now()}")
    print(f"[*] Scanning ports {', '.join(map(str, ports))}")
    open_ports = []

    for index, port in enumerate(ports):
        if scan_port(target, port, timeout):
            open_ports.append(port)
            print(f"[+] Port {port}: OPEN")
        if index < len(ports) - 1:
            time.sleep(delay)

    print(f"[*] Scan completed at {datetime.now()}")
    print(f"[*] Open ports found: {open_ports}")

if __name__ == "__main__":
    try:
        target_host = input("Target (127.0.0.1 or scanme.nmap.org): ").strip()
        ports = parse_ports(input("Ports (example: 1-1000 or 20,21,22,80,443): "))
        run_scan(target_host, ports)
    except socket.gaierror:
        print(f"[!] Hostname could not be resolved: {target_host}")
    except ValueError as e:
        print(f"[!] Invalid input: {e}")
    except OSError as e:
        print(f"[!] Network error: {e}")
    except KeyboardInterrupt:
        print("\n[!] Scan cancelled by user")

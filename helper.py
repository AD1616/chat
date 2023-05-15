import subprocess
import netifaces


def get_non_loopback_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for address in addresses[netifaces.AF_INET]:
                ip = address['addr']
                if not ip.startswith('127.'):
                    return ip
    return None


def extract_port_numbers(ip_address):
    command = f"netstat -a | awk '$6 == \"ESTABLISHED\" && $4 ~ /^{ip_address}/ {{print $4}}'"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    port_numbers = [int(port.split('.')[4]) for port in output.strip().split('\n')]
    return port_numbers


def validate_port(port):
    bad_ports = [63342]
    if port not in bad_ports:
        return True
    return False


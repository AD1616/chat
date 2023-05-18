import subprocess
import netifaces
import socket

def get_non_loopback_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo' or interface.startswith('vbox'):
            continue
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for address in addresses[netifaces.AF_INET]:
                ip = address['addr']
                if not ip.startswith('127.'):
                    return ip


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


def known_ports():
    possible_allowed = [64667, 64692, 64691, 64690, 64689, 64688, 64685, 64675, 64674]
    return possible_allowed

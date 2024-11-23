from scapy.all import *

def list_network_interfaces():
    print("Available Network Interfaces:")
    print("-" * 50)
    for iface in get_working_ifaces():
        print(f"Name: {iface.name}")
        print(f"Description: {iface.description}")
        print(f"MAC: {iface.mac}")
        print(f"IP: {iface.ip}")
        print("-" * 50)

if __name__ == "__main__":
    list_network_interfaces() 
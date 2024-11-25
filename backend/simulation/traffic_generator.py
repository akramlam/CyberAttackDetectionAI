import random
import time
import threading
from scapy.all import IP, TCP, UDP, ICMP, send
from datetime import datetime

class TrafficGenerator:
    def __init__(self):
        self.running = False
        self.thread = None
        self.protocols = [TCP, UDP, ICMP]
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._generate_traffic)
        self.thread.start()
        print("Traffic generation started")
        
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("Traffic generation stopped")
        
    def _generate_normal_traffic(self):
        """Generate normal network traffic"""
        src_ip = f"192.168.1.{random.randint(2, 100)}"
        dst_ip = f"192.168.1.{random.randint(2, 100)}"
        protocol = random.choice(self.protocols)
        
        packet = IP(src=src_ip, dst=dst_ip)
        if protocol == TCP:
            packet = packet/TCP(sport=random.randint(1024, 65535), 
                              dport=random.randint(1024, 65535))
        elif protocol == UDP:
            packet = packet/UDP(sport=random.randint(1024, 65535), 
                              dport=random.randint(1024, 65535))
        else:
            packet = packet/ICMP()
            
        return packet
        
    def _generate_attack_traffic(self):
        """Generate suspicious/attack traffic"""
        attack_types = ['port_scan', 'ddos', 'data_exfiltration']
        attack = random.choice(attack_types)
        
        if attack == 'port_scan':
            src_ip = f"192.168.1.{random.randint(2, 100)}"
            dst_ip = "192.168.1.1"
            packet = IP(src=src_ip, dst=dst_ip)/TCP(dport=random.randint(1, 1024))
            
        elif attack == 'ddos':
            src_ip = f"192.168.1.{random.randint(2, 100)}"
            dst_ip = "192.168.1.1"
            packet = IP(src=src_ip, dst=dst_ip)/UDP(dport=53)/("X"*1400)
            
        else:  # data_exfiltration
            src_ip = "192.168.1.100"
            dst_ip = "8.8.8.8"
            packet = IP(src=src_ip, dst=dst_ip)/TCP(dport=443)/("CONFIDENTIAL_DATA"*100)
            
        return packet
        
    def _generate_traffic(self):
        """Main traffic generation loop"""
        while self.running:
            try:
                # 90% normal traffic, 10% attack traffic
                if random.random() < 0.9:
                    packet = self._generate_normal_traffic()
                else:
                    packet = self._generate_attack_traffic()
                    
                send(packet, verbose=False)
                time.sleep(random.uniform(0.1, 0.5))  # Random delay between packets
                
            except Exception as e:
                print(f"Error generating traffic: {e}")
                time.sleep(1) 
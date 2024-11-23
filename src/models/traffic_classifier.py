import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, List

class TrafficClassifier(nn.Module):
    def __init__(self):
        super(TrafficClassifier, self).__init__()
        self.conv1 = nn.Conv1d(1, 32, 3)
        self.conv2 = nn.Conv1d(32, 64, 3)
        self.conv3 = nn.Conv1d(64, 128, 3)
        self.pool = nn.MaxPool1d(2)
        self.fc1 = nn.Linear(128 * 4, 512)
        self.fc2 = nn.Linear(512, 10)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * 4)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)
        
    def classify_traffic(self, packet_sequence: torch.Tensor) -> List[str]:
        """Classify network traffic into detailed categories"""
        with torch.no_grad():
            predictions = self(packet_sequence)
            
        categories = [
            'Normal Traffic',
            'DDoS Attack',
            'Port Scanning',
            'SQL Injection',
            'XSS Attack',
            'Data Exfiltration',
            'Command Injection',
            'Malware Communication',
            'Cryptomining',
            'Zero-day Attack'
        ]
        
        return [categories[i] for i in predictions.argmax(dim=1)] 
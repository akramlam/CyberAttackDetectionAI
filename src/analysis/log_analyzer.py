from transformers import pipeline
import re
from typing import List, Dict
import pandas as pd
from collections import defaultdict
import spacy
from datetime import datetime

class LogAnalyzer:
    def __init__(self):
        # Load NLP models
        self.nlp = spacy.load("en_core_web_sm")
        self.classifier = pipeline("zero-shot-classification")
        self.anomaly_labels = [
            "authentication failure",
            "network scan",
            "data exfiltration",
            "malware activity",
            "denial of service"
        ]
        
    def extract_patterns(self, log_entry: str) -> Dict:
        """Extract key information using NLP"""
        doc = self.nlp(log_entry)
        
        # Extract IPs
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, log_entry)
        
        # Extract timestamps
        timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        timestamps = re.findall(timestamp_pattern, log_entry)
        
        # Extract named entities
        entities = {ent.label_: ent.text for ent in doc.ents}
        
        return {
            'ips': ips,
            'timestamps': timestamps,
            'entities': entities
        }
        
    def classify_log_entry(self, log_entry: str) -> Dict:
        """Classify log entry using zero-shot learning"""
        result = self.classifier(
            log_entry,
            candidate_labels=self.anomaly_labels,
            multi_label=True
        )
        
        return {
            'labels': result['labels'],
            'scores': result['scores']
        }
        
    def analyze_log_sequence(self, logs: List[str]) -> Dict:
        """Analyze a sequence of log entries for patterns"""
        analysis = {
            'event_sequences': defaultdict(list),
            'ip_frequencies': defaultdict(int),
            'anomaly_types': defaultdict(int),
            'temporal_patterns': []
        }
        
        for log in logs:
            # Extract and classify
            patterns = self.extract_patterns(log)
            classification = self.classify_log_entry(log)
            
            # Update IP frequencies
            for ip in patterns['ips']:
                analysis['ip_frequencies'][ip] += 1
                
            # Update anomaly types
            for label, score in zip(classification['labels'], classification['scores']):
                if score > 0.5:
                    analysis['anomaly_types'][label] += 1
                    
            # Analyze temporal patterns
            if patterns['timestamps']:
                analysis['temporal_patterns'].append({
                    'timestamp': datetime.strptime(patterns['timestamps'][0], 
                                                 '%Y-%m-%d %H:%M:%S'),
                    'event_type': classification['labels'][0]
                })
                
        # Sort temporal patterns
        analysis['temporal_patterns'].sort(key=lambda x: x['timestamp'])
        
        return analysis
        
    def generate_insights(self, analysis: Dict) -> List[str]:
        """Generate human-readable insights from analysis"""
        insights = []
        
        # IP-based insights
        suspicious_ips = {ip: freq for ip, freq in analysis['ip_frequencies'].items() 
                         if freq > 10}
        if suspicious_ips:
            insights.append(f"Found {len(suspicious_ips)} IPs with high activity frequency")
            
        # Anomaly patterns
        common_anomalies = sorted(analysis['anomaly_types'].items(), 
                                key=lambda x: x[1], reverse=True)
        if common_anomalies:
            insights.append(f"Most common anomaly type: {common_anomalies[0][0]}")
            
        # Temporal insights
        if analysis['temporal_patterns']:
            time_diffs = []
            for i in range(1, len(analysis['temporal_patterns'])):
                diff = (analysis['temporal_patterns'][i]['timestamp'] - 
                       analysis['temporal_patterns'][i-1]['timestamp']).total_seconds()
                time_diffs.append(diff)
            if time_diffs:
                avg_time = sum(time_diffs) / len(time_diffs)
                insights.append(f"Average time between events: {avg_time:.2f} seconds")
                
        return insights 
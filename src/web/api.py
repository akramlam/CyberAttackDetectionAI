from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from typing import List, Dict
import requests
import ipaddress
from collections import Counter
import os

api = Blueprint('api', __name__)

class ThreatIntelligence:
    def __init__(self):
        # API Keys
        self.abuse_ipdb_key = "3c300b5522020aa77eae7a0a811636fd2f70dcdd1105197057bd4ca56d0eabd6de5942cb761b67c1"
        self.virustotal_key = "921b2ce9e4a88c15e211cfe1b2dd50d3288b32507e28cd3acd4f2fea82832883"
        
    def check_ip(self, ip: str) -> Dict:
        """
        Check IP against both AbuseIPDB and VirusTotal
        """
        results = {
            'is_malicious': False,
            'threat_score': 0,
            'reports': []
        }
        
        # Skip if IP is None or invalid
        if not ip or ip == 'None':
            return results
        
        try:
            if ipaddress.ip_address(ip).is_private:
                return results
        except:
            return results
            
        # Check AbuseIPDB
        try:
            url = 'https://api.abuseipdb.com/api/v2/check'
            headers = {
                'Accept': 'application/json',
                'Key': self.abuse_ipdb_key
            }
            params = {
                'ipAddress': ip,
                'maxAgeInDays': 30,
                'verbose': True
            }
            
            response = requests.get(
                url=url,
                headers=headers,
                params=params,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()['data']
                abuse_score = data['abuseConfidenceScore']
                results['reports'].append(f"AbuseIPDB Score: {abuse_score}%")
                
                if abuse_score > 50:
                    results['is_malicious'] = True
                    results['threat_score'] = max(results['threat_score'], abuse_score/100)
                    results['reports'].extend([
                        f"Total Reports: {data['totalReports']}",
                        f"Last Reported: {data.get('lastReportedAt', 'N/A')}",
                        f"Country: {data.get('countryCode', 'Unknown')}"
                    ])
                    
        except Exception as e:
            results['reports'].append(f"AbuseIPDB check failed: {str(e)}")
            
        # Check VirusTotal
        try:
            url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
            headers = {
                'x-apikey': self.virustotal_key
            }
            
            response = requests.get(
                url=url,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()['data']['attributes']
                
                # Get reputation score
                reputation = data.get('reputation', 0)
                vt_score = abs(min(reputation, 0)) / 100  # Convert negative reputation to positive score
                
                results['reports'].append(f"VirusTotal Reputation: {reputation}")
                
                if vt_score > 0.5:  # If reputation is significantly negative
                    results['is_malicious'] = True
                    results['threat_score'] = max(results['threat_score'], vt_score)
                    
                    # Add last analysis stats
                    stats = data.get('last_analysis_stats', {})
                    if stats:
                        results['reports'].append(
                            f"VirusTotal Analysis: "
                            f"Malicious: {stats.get('malicious', 0)}, "
                            f"Suspicious: {stats.get('suspicious', 0)}"
                        )
                        
        except Exception as e:
            results['reports'].append(f"VirusTotal check failed: {str(e)}")
            
        return results

# Create a single instance
threat_intel = ThreatIntelligence()

@api.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    from src.utils.metrics import performance_monitor
    
    return jsonify({
        'uptime': str(datetime.now() - START_TIME),
        'alerts_today': len([a for a in ALERTS if a['timestamp'].date() == datetime.now().date()]),
        'anomaly_rate': performance_monitor.get_average('anomaly_scores'),
        'processing_time': performance_monitor.get_average('processing_time'),
        'packets_processed': performance_monitor.get_average('packets_processed')
    })

@api.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    limit = request.args.get('limit', 100, type=int)
    from src.models.database import db
    
    alerts = db.get_recent_events(limit)
    return jsonify([{
        'timestamp': str(a.timestamp),
        'source_ip': a.source_ip,
        'alert_level': a.alert_level,
        'anomaly_score': a.anomaly_score
    } for a in alerts])

@api.route('/api/threat-intel/<ip>', methods=['GET'])
def check_ip(ip):
    """Check IP against threat intelligence databases"""
    results = threat_intel.check_ip(ip)
    return jsonify(results)

@api.route('/api/network-stats', methods=['GET'])
def get_network_stats():
    """Get network statistics"""
    from src.data.data_collector import collector
    
    return jsonify({
        'total_packets': len(collector.packets),
        'unique_ips': len(set(p['source_ip'] for p in collector.packets if p['source_ip'])),
        'protocols': dict(Counter(p['protocol'] for p in collector.packets if p['protocol'])),
        'top_talkers': get_top_talkers()
    })

def get_top_talkers(limit: int = 10) -> List[Dict]:
    """Get top IP addresses by traffic volume"""
    from src.data.data_collector import collector
    from collections import Counter
    
    ip_counts = Counter(p['source_ip'] for p in collector.packets if p['source_ip'])
    return [{'ip': ip, 'count': count} for ip, count in ip_counts.most_common(limit)]
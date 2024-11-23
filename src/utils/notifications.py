import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import logging
from .logger import setup_logger

logger = setup_logger(__name__)

class EmailNotifier:
    def __init__(self, smtp_config: Dict[str, str]):
        self.smtp_server = smtp_config.get('server', 'smtp.gmail.com')
        self.smtp_port = smtp_config.get('port', 587)
        self.sender_email = smtp_config.get('email')
        self.password = smtp_config.get('password')
        self.recipient_emails = smtp_config.get('recipients', [])
        
    def send_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Send email alert for critical events"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            msg['Subject'] = f"CRITICAL ALERT - IDS Detection {alert_data['source_ip']}"
            
            body = f"""
            Critical Security Alert Detected
            
            Time: {alert_data['timestamp']}
            Source IP: {alert_data['source_ip']}
            Threat Score: {alert_data.get('threat_info', {}).get('threat_score', 'N/A')}
            
            Details:
            {alert_data.get('details', 'No additional details')}
            
            Automated Actions Taken:
            - IP has been blocked
            - Additional monitoring enabled
            
            Please investigate immediately.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
                
            logger.info(f"Alert email sent for IP: {alert_data['source_ip']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alert email: {str(e)}")
            return False 
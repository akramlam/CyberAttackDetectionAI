import pandas as pd
from typing import List, Dict
import json
from datetime import datetime
import csv
import os

class ReportExporter:
    def __init__(self, export_dir: str = 'exports'):
        self.export_dir = export_dir
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            
    def export_alerts(self, alerts: List[Dict], format: str = 'csv') -> str:
        """Export alerts to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'alerts_{timestamp}.{format}'
        filepath = os.path.join(self.export_dir, filename)
        
        df = pd.DataFrame(alerts)
        
        if format == 'csv':
            df.to_csv(filepath, index=False)
        elif format == 'json':
            df.to_json(filepath, orient='records')
        elif format == 'excel':
            df.to_excel(filepath, index=False)
            
        return filepath 
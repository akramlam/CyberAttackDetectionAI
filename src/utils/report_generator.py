from typing import List, Dict
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import plotly.io as pio
import os

class ReportGenerator:
    def __init__(self, export_dir: str = 'reports'):
        self.export_dir = export_dir
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            
    def generate_pdf_report(self, alerts: List[Dict], system_stats: Dict) -> str:
        """Generate a PDF report with alerts and system statistics"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'security_report_{timestamp}.pdf'
        filepath = os.path.join(self.export_dir, filename)
        
        # Create DataFrame
        df = pd.DataFrame(alerts)
        
        # Create visualizations
        fig1 = go.Figure(data=[
            go.Scatter(x=df['timestamp'], y=df['anomaly_score'])
        ])
        fig1.update_layout(title='Anomaly Scores Over Time')
        
        fig2 = go.Figure(data=[
            go.Pie(labels=df['alert_level'].value_counts().index,
                  values=df['alert_level'].value_counts().values)
        ])
        fig2.update_layout(title='Alert Level Distribution')
        
        # Save figures as images
        pio.write_image(fig1, 'temp_fig1.png')
        pio.write_image(fig2, 'temp_fig2.png')
        
        # Create PDF report
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        story.append(Paragraph('Security Report', styles['Title']))
        story.append(Spacer(1, 12))
        
        # Add summary
        story.append(Paragraph('Alert Summary:', styles['Heading1']))
        story.append(Paragraph(f'Total Alerts: {len(alerts)}', styles['Normal']))
        story.append(Paragraph(f'Critical Alerts: {len(df[df["alert_level"] == 2])}', styles['Normal']))
        
        # Add visualizations
        story.append(Image('temp_fig1.png', width=400, height=300))
        story.append(Image('temp_fig2.png', width=400, height=300))
        
        # Build PDF
        doc.build(story)
        
        # Clean up temporary files
        os.remove('temp_fig1.png')
        os.remove('temp_fig2.png')
        
        return filepath 
import plotly.graph_objs as go
from typing import List, Dict
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

class DashboardVisualizer:
    @staticmethod
    def create_threat_map(alerts: List[Dict]) -> go.Figure:
        """Create a world map showing threat origins"""
        df = pd.DataFrame(alerts)
        
        fig = px.scatter_geo(
            df,
            lat='latitude',
            lon='longitude',
            color='threat_score',
            hover_name='source_ip',
            size='alert_count',
            projection='natural earth',
            title='Global Threat Distribution'
        )
        
        return fig
        
    @staticmethod
    def create_timeline(alerts: List[Dict]) -> go.Figure:
        """Create an interactive timeline of alerts"""
        df = pd.DataFrame(alerts)
        
        fig = go.Figure()
        
        # Add different traces for each alert level
        for level in df['alert_level'].unique():
            level_data = df[df['alert_level'] == level]
            fig.add_trace(go.Scatter(
                x=level_data['timestamp'],
                y=level_data['anomaly_score'],
                mode='markers',
                name=f'Level {level}',
                marker=dict(
                    size=10,
                    symbol='circle',
                    line=dict(width=1)
                ),
                text=level_data['source_ip'],
                hovertemplate=(
                    '<b>IP:</b> %{text}<br>'
                    '<b>Score:</b> %{y:.2f}<br>'
                    '<b>Time:</b> %{x}<br>'
                    '<extra></extra>'
                )
            ))
        
        fig.update_layout(
            title='Alert Timeline',
            xaxis_title='Time',
            yaxis_title='Anomaly Score',
            hovermode='closest'
        )
        
        return fig
        
    @staticmethod
    def create_threat_summary(alerts: List[Dict]) -> go.Figure:
        """Create a summary of threat statistics"""
        df = pd.DataFrame(alerts)
        
        # Create subplots
        fig = go.Figure()
        
        # Add alert level distribution
        fig.add_trace(go.Pie(
            labels=['Critical', 'Warning', 'Info'],
            values=df['alert_level'].value_counts(),
            domain=dict(x=[0, 0.5], y=[0, 1]),
            name='Alert Levels'
        ))
        
        # Add threat score distribution
        fig.add_trace(go.Histogram(
            x=df['threat_score'],
            nbinsx=20,
            domain=dict(x=[0.6, 1], y=[0, 1]),
            name='Threat Scores'
        ))
        
        fig.update_layout(
            title='Threat Analysis Summary',
            showlegend=True
        )
        
        return fig
        
    @staticmethod
    def create_3d_network_map(alerts: List[Dict]) -> go.Figure:
        """Create an interactive 3D network traffic visualization"""
        df = pd.DataFrame(alerts)
        
        # Create 3D graph
        fig = go.Figure()
        
        # Add nodes (IPs)
        fig.add_trace(go.Scatter3d(
            x=df['x_coord'],  # Using geolocation data
            y=df['y_coord'],
            z=df['anomaly_score'],
            mode='markers',
            marker=dict(
                size=8,
                color=df['alert_level'],
                colorscale='Viridis',
                opacity=0.8
            ),
            text=df['source_ip'],
            hoverinfo='text'
        ))
        
        # Add edges (connections)
        for _, row in df.iterrows():
            fig.add_trace(go.Scatter3d(
                x=[row['src_x'], row['dst_x']],
                y=[row['src_y'], row['dst_y']],
                z=[row['src_z'], row['dst_z']],
                mode='lines',
                line=dict(
                    color='red' if row['alert_level'] == 2 else 'blue',
                    width=2
                ),
                opacity=0.5
            ))
        
        fig.update_layout(
            title='3D Network Traffic Visualization',
            scene=dict(
                xaxis_title='Longitude',
                yaxis_title='Latitude',
                zaxis_title='Anomaly Score',
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            showlegend=False
        )
        
        return fig
from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime, timedelta
import pandas as pd
from ..models.database import DatabaseManager
import logging
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/',
                    suppress_callback_exceptions=True)

# Initialize database
db = DatabaseManager('postgresql://ids_user:123@localhost:5432/ids_db')

# Dashboard layout
dash_app.layout = html.Div([
    # Navigation bar
    html.Nav([
        html.A('← Back to Main', href='/', className='nav-link'),
        html.H1('Network Intrusion Detection System Dashboard')
    ], className='dash-nav'),
    
    # Loading component
    dcc.Loading(
        id="loading-graphs",
        type="circle",
        children=[
            # Tabs
            dcc.Tabs([
                dcc.Tab(label='Real-time Monitoring', children=[
                    html.Div([
                        dcc.Graph(
                            id='live-traffic-graph',
                            figure=go.Figure().add_annotation(
                                text="Waiting for data...",
                                xref="paper",
                                yref="paper",
                                x=0.5,
                                y=0.5,
                                showarrow=False,
                                font=dict(size=20)
                            )
                        ),
                        dcc.Graph(
                            id='anomaly-distribution',
                            figure=go.Figure().add_annotation(
                                text="Waiting for data...",
                                xref="paper",
                                yref="paper",
                                x=0.5,
                                y=0.5,
                                showarrow=False,
                                font=dict(size=20)
                            )
                        ),
                    ])
                ]),
                dcc.Tab(label='Network Statistics', children=[
                    html.Div([
                        dcc.Graph(id='protocol-distribution'),
                        dcc.Graph(id='top-talkers'),
                    ])
                ])
            ])
        ]
    ),
    
    # Interval component
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0
    ),
    
    # Store component for data
    dcc.Store(id='graph-data-store')
])

# Update callback
@dash_app.callback(
    [Output('live-traffic-graph', 'figure'),
     Output('anomaly-distribution', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    try:
        # Get recent events from database
        events = db.get_recent_events(1000)
        
        # Create empty graphs if no data
        if not events:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text="No data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=20)
            )
            empty_fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return empty_fig, empty_fig
        
        # Create dataframe from events
        df = pd.DataFrame([{
            'timestamp': e.timestamp,
            'anomaly_score': e.anomaly_score,
            'alert_level': e.alert_level
        } for e in events])
        
        # Create traffic graph
        traffic_fig = go.Figure()
        traffic_fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['anomaly_score'],
            mode='lines+markers',
            name='Anomaly Score',
            marker=dict(
                size=8,
                color=df['alert_level'],
                colorscale='Viridis',
                showscale=True
            )
        ))
        traffic_fig.update_layout(
            title="Network Traffic Analysis",
            xaxis_title="Time",
            yaxis_title="Anomaly Score",
            template="plotly_dark",
            hovermode='closest'
        )
        
        # Create anomaly distribution
        dist_fig = go.Figure()
        dist_fig.add_trace(go.Histogram(
            x=df['anomaly_score'],
            nbinsx=30,
            name='Anomaly Distribution',
            marker_color='rgb(55, 83, 109)'
        ))
        dist_fig.update_layout(
            title="Anomaly Distribution",
            xaxis_title="Anomaly Score",
            yaxis_title="Count",
            template="plotly_dark",
            bargap=0.1
        )
        
        return traffic_fig, dist_fig
        
    except Exception as e:
        logger.error(f"Error updating graphs: {str(e)}")
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="Error loading data",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=20)
        )
        empty_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return empty_fig, empty_fig

@app.route('/to-dashboard')
def to_dashboard():
    return redirect('/dashboard/')

@app.route('/')
def index():
    return render_template('index.html')

def start_web_server(host='0.0.0.0', port=5000):
    socketio.run(app, host=host, port=port, debug=True) 
from flask import Blueprint, jsonify
from ..utils.performance import SystemMonitor
import psutil
import time

system_bp = Blueprint('system', __name__)
system_monitor = SystemMonitor()

@system_bp.route('/api/system/stats')
def get_system_stats():
    stats = system_monitor.get_system_metrics()
    return jsonify({
        'cpu': stats['cpu_percent'],
        'memory': stats['memory_percent'],
        'disk': stats['disk_usage'],
        'network': {
            'bytes_sent': stats['network_io']['bytes_sent'],
            'bytes_recv': stats['network_io']['bytes_recv']
        }
    }) 
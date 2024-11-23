from flask import Blueprint, jsonify
from threading import Event
import logging
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

control_bp = Blueprint('control', __name__)

# Global control flag
system_running = Event()

@control_bp.route('/control/start', methods=['POST'])
def start_system():
    """Start the monitoring system"""
    if not system_running.is_set():
        system_running.set()
        logger.info("System monitoring started")
        return jsonify({'success': True, 'message': 'System started'})
    return jsonify({'success': False, 'message': 'System already running'})

@control_bp.route('/control/stop', methods=['POST'])
def stop_system():
    """Stop the monitoring system"""
    if system_running.is_set():
        system_running.clear()
        logger.info("System monitoring stopped")
        return jsonify({'success': True, 'message': 'System stopped'})
    return jsonify({'success': False, 'message': 'System already stopped'})

@control_bp.route('/control/status', methods=['GET'])
def get_status():
    """Get current system status"""
    status = 'Running' if system_running.is_set() else 'Stopped'
    return jsonify({'status': status}) 
from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            response = {
                'error': e.name,
                'message': e.description,
                'status_code': e.code
            }
        else:
            response = {
                'error': 'Internal Server Error',
                'message': str(e),
                'status_code': 500
            }
        return jsonify(response), response['status_code'] 
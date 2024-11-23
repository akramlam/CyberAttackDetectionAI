from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from ..auth.auth import AuthManager

auth_bp = Blueprint('auth', __name__)
auth_manager = AuthManager()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if auth_manager.verify_password(username, password):
            user = auth_manager.get_user(username)
            login_user(user)
            return redirect(url_for('dashboard'))
            
        return render_template('login.html', error="Invalid credentials")
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 
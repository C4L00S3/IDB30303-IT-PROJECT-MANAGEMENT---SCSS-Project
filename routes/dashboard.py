from flask import Blueprint, render_template, session, redirect, url_for
from database import get_db_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/student')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings WHERE user_id = ? ORDER BY id DESC', (session['user_id'],)).fetchall()
    maintenance = conn.execute('SELECT * FROM maintenance_requests WHERE user_id = ? ORDER BY id DESC', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard_student.html', bookings=bookings, maintenance=maintenance)

@dashboard_bp.route('/lecturer')
def lecturer_dashboard():
    if session.get('role') != 'lecturer':
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings WHERE user_id = ? ORDER BY id DESC', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard_lecturer.html', bookings=bookings)

@dashboard_bp.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    # Get all bookings with user details
    bookings = conn.execute('''
        SELECT b.*, u.name as user_name 
        FROM bookings b 
        JOIN users u ON b.user_id = u.id 
        ORDER BY b.id DESC
    ''').fetchall()
    
    # Get all maintenance requests with user details
    maintenance = conn.execute('''
        SELECT m.*, u.name as user_name 
        FROM maintenance_requests m 
        JOIN users u ON m.user_id = u.id 
        ORDER BY m.id DESC
    ''').fetchall()
    conn.close()
    
    return render_template('dashboard_admin.html', bookings=bookings, maintenance=maintenance)

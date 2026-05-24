from flask import Blueprint, request, redirect, url_for, session, flash, abort
from database import get_db_connection

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/maintenance/submit', methods=['POST'])
def submit_request():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    room = request.form['room']
    category = request.form['category']
    description = request.form['description']
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO maintenance_requests (user_id, room, category, description) VALUES (?, ?, ?, ?)',
        (session['user_id'], room, category, description)
    )
    conn.commit()
    conn.close()
    
    flash('Maintenance request submitted successfully.', 'success')
    return redirect(url_for(f'dashboard.{session["role"]}_dashboard'))

@maintenance_bp.route('/admin/maintenance/assign/<int:request_id>', methods=['POST'])
def assign_technician(request_id):
    """
    INTENTIONAL LIMITATION / SIMULATED BUG FOR MILESTONE 4 (MONITORING & CONTROLLING)
    This route simulates a 500 Internal Server Error due to a "Database Transaction Lock" 
    or "Missing Security Clearance" module.
    """
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    # We purposefully throw an abort 500 to simulate the issue log for Milestone 4.
    # The error will be caught by a generic error handler or just display the default 500 page.
    # To make it clear in the logs:
    print(f"ERROR: Administrator attempted to assign technician to request {request_id}")
    print("Database transaction lock - Technician assignment module requires security clearance.")
    
    abort(500, description="Database transaction lock - Technician assignment module requires security clearance. Please log this issue for Milestone 4.")

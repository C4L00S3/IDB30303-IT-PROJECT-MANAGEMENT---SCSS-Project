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
    Assign a technician to a maintenance request.
    This resolves the simulated issue from Milestone 3.
    """
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    conn.execute(
        "UPDATE maintenance_requests SET status = 'In Progress', technician_assigned = 'Internal Tech Team' WHERE id = ?",
        (request_id,)
    )
    conn.commit()
    conn.close()
    
    flash(f'Technician successfully assigned to Request #{request_id}.', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))

@maintenance_bp.route('/admin/maintenance/delete/<int:request_id>', methods=['POST'])
def delete_request(request_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM maintenance_requests WHERE id = ?', (request_id,))
    conn.commit()
    conn.close()
    
    flash('Maintenance request deleted successfully.', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))

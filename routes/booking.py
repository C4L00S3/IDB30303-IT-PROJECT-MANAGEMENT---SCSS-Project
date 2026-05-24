from flask import Blueprint, request, redirect, url_for, session, flash
from database import get_db_connection

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book', methods=['POST'])
def book_room():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    room = request.form['room']
    date = request.form['date']
    time_slot = request.form['time_slot']
    
    conn = get_db_connection()
    
    # Conflict Detection: Check if the room is already booked for this date and time
    existing = conn.execute(
        'SELECT * FROM bookings WHERE room = ? AND date = ? AND time_slot = ?',
        (room, date, time_slot)
    ).fetchone()
    
    if existing:
        flash(f'Conflict Detected: {room} is already booked on {date} at {time_slot}. Please select another slot.', 'danger')
    else:
        conn.execute(
            'INSERT INTO bookings (user_id, room, date, time_slot) VALUES (?, ?, ?, ?)',
            (session['user_id'], room, date, time_slot)
        )
        conn.commit()
        flash(f'Success: {room} has been successfully booked for {date} at {time_slot}.', 'success')
        
    conn.close()
    
    return redirect(url_for(f'dashboard.{session["role"]}_dashboard'))

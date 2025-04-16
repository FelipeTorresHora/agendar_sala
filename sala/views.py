
from django.shortcuts import render, redirect
import uuid

# Mock users (could be read from a file or environment variable)
USERS = {
    'user@example.com': 'password123',
}

# In-memory storage for sessions and bookings
SESSIONS = {}
BOOKINGS = {}

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if USERS.get(email) == password:
            # Create a session token
            session_id = str(uuid.uuid4())
            SESSIONS[session_id] = {'user': email}
            
            # Set a cookie with the session ID
            response = redirect('agenda')
            response.set_cookie('session_id', session_id)
            return response
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'login.html')


def schedule_view(request):
    # Get session ID from cookie
    session_id = request.COOKIES.get('session_id')
    
    # Check if session exists
    if not session_id or session_id not in SESSIONS:
        return redirect('login')
    
    user = SESSIONS[session_id]['user']
    
    if request.method == 'POST':
        # Store booking information
        booking = {
            'user': user,
            'date': request.POST.get('date'),
            'time': request.POST.get('time'),
            'duration': request.POST.get('duration'),
            'room': request.POST.get('room'),
        }
        
        booking_id = str(uuid.uuid4())
        BOOKINGS[booking_id] = booking
        
        # Store booking reference in session
        if 'bookings' not in SESSIONS[session_id]:
            SESSIONS[session_id]['bookings'] = []
        SESSIONS[session_id]['bookings'].append(booking_id)
        
        return render(request, 'agenda.html', {'success': True})
    
    return render(request, 'agenda.html')


def logout_view(request):
    # Get session ID from cookie
    session_id = request.COOKIES.get('session_id')
    
    # Remove session if it exists
    if session_id and session_id in SESSIONS:
        del SESSIONS[session_id]
    
    # Clear the cookie
    response = redirect('login')
    response.delete_cookie('session_id')
    return response
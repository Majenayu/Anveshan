from flask import Flask, render_template_string, request, redirect, url_for, jsonify, session, send_from_directory
import pymongo
from datetime import datetime, timedelta
from collections import defaultdict
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change in production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# MongoDB connection
db_connected = False
try:
    client = pymongo.MongoClient("mongodb+srv://anv:anv@anv.thrp6za.mongodb.net/?appName=anv")
    db = client.get_database("face_auth")
    users = db.users
    client.admin.command('ping')
    print("✓ MongoDB connected successfully")
    db_connected = True
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    print("App will run without DB (profile features disabled)")

# Updated INDEX_HTML (with /home redirects)
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AsanaMind - Login or Register</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-effect {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .dark .glass-effect { background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); }
        .fade-in { animation: fadeIn 0.6s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .slide-in { animation: slideIn 0.4s ease-out; }
        @keyframes slideIn { from { transform: translateX(-20px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        .pulse-button { transition: all 0.3s ease; }
        .pulse-button:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2); }
    </style>
</head>
<body class="gradient-bg min-h-screen flex items-center justify-center px-4">
    <!-- Loader -->
    <div class="loader-wrap fixed inset-0 flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900 z-50 hidden" id="loader">
        <div class="relative">
            <div class="w-16 h-16 border-4 border-white/20 border-t-white rounded-full animate-spin"></div>
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full animate-pulse"></div>
        </div>
    </div>
    <!-- Main Container -->
    <div class="w-full max-w-md fade-in">
        <!-- Header -->
        <div class="text-center mb-8">
            <div class="inline-block p-4 rounded-full glass-effect mb-4">
                <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
                </svg>
            </div>
            <h1 class="text-4xl font-bold text-white mb-2">Welcome to AsanaMind</h1>
            <p class="text-white/70 text-lg">Your Yoga Journey Begins Here</p>
        </div>
        <!-- Forms Container -->
        <div class="glass-effect rounded-2xl p-8 shadow-2xl">
            <!-- Login Form -->
            <div id="login-form" class="space-y-6">
                <div class="text-center mb-6">
                    <h2 class="text-2xl font-bold text-white mb-2">Login</h2>
                    <div class="w-20 h-1 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full mx-auto"></div>
                </div>
                <form id="login-form-submit" class="space-y-5">
                    <input id="login-name" type="text" placeholder="Enter your name" required
                        class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400">
                    <input id="login-email" type="email" placeholder="Enter your email" required
                        class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400">
                    <button type="submit" class="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-xl pulse-button">Login</button>
                </form>
                <div class="text-center">
                    <span class="text-white/70">Don't have an account?</span>
                    <button id="show-register" class="text-blue-300 hover:text-blue-200 font-semibold ml-2">Register</button>
                </div>
                <p id="login-error" class="text-center text-red-300 hidden bg-red-500/20 py-2 px-4 rounded-lg"></p>
            </div>
            <!-- Register Form -->
            <div id="register-form" class="space-y-6 hidden">
                <div class="text-center mb-6">
                    <h2 class="text-2xl font-bold text-white mb-2">Register</h2>
                    <div class="w-20 h-1 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full mx-auto"></div>
                </div>
                <form id="register-form-submit" class="space-y-5">
                    <input id="register-name" type="text" placeholder="Enter your name" required
                        class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-400">
                    <input id="register-email" type="email" placeholder="Enter your email" required
                        class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-400">
                    <button type="submit" class="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white font-semibold rounded-xl pulse-button">Register</button>
                </form>
                <div class="text-center">
                    <span class="text-white/70">Already have an account?</span>
                    <button id="show-login" class="text-purple-300 hover:text-purple-200 font-semibold ml-2">Login</button>
                </div>
                <p id="register-error" class="text-center text-red-300 hidden bg-red-500/20 py-2 px-4 rounded-lg"></p>
            </div>
        </div>
    </div>
    <script>
        function toggleForm(showRegister) {
            document.getElementById('login-form').classList.toggle('hidden', showRegister);
            document.getElementById('register-form').classList.toggle('hidden', !showRegister);
        }
        document.getElementById('show-register').addEventListener('click', () => toggleForm(true));
        document.getElementById('show-login').addEventListener('click', () => toggleForm(false));
        function toggleLoader(show) {
            document.getElementById('loader').classList.toggle('hidden', !show);
        }
        // Handle login (redirect to /home)
        document.getElementById('login-form-submit').addEventListener('submit', async (e) => {
            e.preventDefault();
            toggleLoader(true);
            const name = document.getElementById('login-name').value;
            const email = document.getElementById('login-email').value;
            const errorEl = document.getElementById('login-error');
            try {
                const res = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email })
                });
                const data = await res.json();
                toggleLoader(false);
                if (data.success) {
                    window.location.href = '/home';
                } else {
                    errorEl.textContent = data.error || 'Login failed';
                    errorEl.classList.remove('hidden');
                }
            } catch {
                toggleLoader(false);
                errorEl.textContent = 'Login failed. Please try again.';
                errorEl.classList.remove('hidden');
            }
        });
        // Handle register (redirect to /home)
        document.getElementById('register-form-submit').addEventListener('submit', async (e) => {
            e.preventDefault();
            toggleLoader(true);
            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const errorEl = document.getElementById('register-error');
            try {
                const res = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email })
                });
                const data = await res.json();
                toggleLoader(false);
                if (data.success) {
                    window.location.href = '/home';
                } else {
                    errorEl.textContent = data.error || 'Registration failed';
                    errorEl.classList.remove('hidden');
                }
            } catch {
                toggleLoader(false);
                errorEl.textContent = 'Registration failed. Please try again.';
                errorEl.classList.remove('hidden');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/main')
def main_alias():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    if not os.path.exists('main.html'):
        return "Error: main.html not found in app directory. Place it here.", 500
    return send_from_directory('.', 'main.html')

@app.route('/profile')
def profile_page():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    if not os.path.exists('profile.html'):
        return "Error: profile.html not found in app directory. Place it here.", 500
    return send_from_directory('.', 'profile.html')

@app.route('/register', methods=['POST'])
def register():
    if not db_connected:
        return jsonify({'success': False, 'error': 'Database not available'}), 500
    
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({'success': False, 'error': 'Name and email are required'}), 400
    
    existing_user = users.find_one({'email': email})
    if existing_user:
        return jsonify({'success': False, 'error': 'User already registered with this email'}), 400
    
    today = datetime.now().strftime('%Y-%m-%d')
    user_data = {
        'name': name,
        'email': email,
        'created_at': datetime.utcnow(),
        'activity_log': [today],  # Init with today
        'completed_asanas': {}    # Dynamic object for counts
    }
    result = users.insert_one(user_data)
    
    if result.inserted_id:
        session['logged_in'] = True
        session['user_email'] = email
        session['user_name'] = name
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
def login():
    if not db_connected:
        return jsonify({'success': False, 'error': 'Database not available'}), 500
    
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({'success': False, 'error': 'Name and email are required'}), 400
    
    user = users.find_one({'email': email})
    if not user:
        return jsonify({'success': False, 'error': 'No user found with this email'}), 400
    
    if user['name'] != name:
        return jsonify({'success': False, 'error': 'Name does not match registered user'}), 400
    
    # Add today to activity_log if not exists
    today = datetime.now().strftime('%Y-%m-%d')
    users.update_one({'email': email}, {'$addToSet': {'activity_log': today}})
    
    session['logged_in'] = True
    session['user_email'] = email
    session['user_name'] = name
    return jsonify({'success': True})

@app.route('/api/profile')
def profile():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    email = session['user_email']
    user = users.find_one({'email': email})
    if user:
        # Sort activity_log for frontend
        activity_log = sorted(user.get('activity_log', []))
        total_active_days = len(activity_log)
        return jsonify({
            'name': user['name'],
            'email': user['email'],
            'created_at': user['created_at'].isoformat() if 'created_at' in user else None,
            'activity_log': activity_log,
            'completed_asanas': user.get('completed_asanas', {}),
            'total_active_days': total_active_days
        })
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/complete_pose', methods=['POST'])
def complete_pose():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not db_connected:
        return jsonify({'success': False, 'error': 'Database not available'}), 500
    
    data = request.get_json()
    pose_name = data.get('pose_name')
    accuracy = data.get('accuracy', 0)
    time_held = data.get('time_held', 0)
    
    if time_held < 10:
        return jsonify({'success': True, 'message': 'Pose logged but not counted as successful (under 10s)'})
    
    email = session['user_email']
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Update: Inc count and add date
    users.update_one(
        {'email': email},
        {
            '$inc': {f'completed_asanas.{pose_name}': 1},
            '$addToSet': {'activity_log': today}
        }
    )
    return jsonify({'success': True, 'message': f'{pose_name} completed successfully!'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Serve static assets
@app.route('/assets/<path:filename>')
def serve_asset(filename):
    try:
        return send_from_directory('assets', filename)
    except FileNotFoundError:
        return "Asset not found.", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2'  # Change this to a secure random key

# Configuration
HTML_FILE = 'ind.html'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'phonk@root'  # Change this to a secure password

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid credentials!', 'error')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Login</title>
        <style>
            body { 
                background: #0a0a10; 
                color: #0f0; 
                font-family: 'Courier New', monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .login-box {
                background: rgba(0, 10, 20, 0.9);
                padding: 30px;
                border: 2px solid #0f0;
                border-radius: 5px;
                box-shadow: 0 0 15px #0f0;
            }
            input {
                background: #05050a;
                border: 1px solid #0f0;
                color: #0f0;
                padding: 10px;
                margin: 10px 0;
                width: 100%;
            }
            button {
                background: #0f0;
                color: #000;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                width: 100%;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>SYSTEM ADMIN ACCESS</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">LOGIN</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/panel')
def admin_panel():
    # Check if user is logged in (simple session check)
    if not request.args.get('authenticated'):
        return redirect(url_for('admin_login'))
    
    # Read current HTML content
    try:
        with open(HTML_FILE, 'r') as file:
            html_content = file.read()
    except:
        html_content = 'Error reading file'
    
    return render_template('admin_panel.html', html_content=html_content)

@app.route('/admin/save', methods=['POST'])
def save_changes():
    if not request.args.get('authenticated'):
        return redirect(url_for('admin_login'))
    
    new_content = request.form.get('html_content')
    
    try:
        with open(HTML_FILE, 'w') as file:
            file.write(new_content)
        flash('Changes saved successfully!', 'success')
    except Exception as e:
        flash(f'Error saving changes: {str(e)}', 'error')
    
    return redirect(url_for('admin_panel', authenticated='true'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

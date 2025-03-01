from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for, send_file
from flask_cors import CORS
import subprocess
import random
import firebase_admin
from firebase_admin import credentials, db
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

app = Flask(__name__)
CORS(app)


# Tools dictionary
tools = {
    "nmap": "nmap {target}",
    "nmap_vuln": "nmap --script vuln {target}",
    "hydra": "hydra -L /usr/share/wordlists/users.txt -P /usr/share/wordlists/passwords.txt {target} ssh",
    "john": "john --wordlist=/usr/share/wordlists/rockyou.txt {target}",
    "wpscan": "wpscan --url {target}",
    "sublist3r": "sublist3r -d {target}",
    "theharvester": "theharvester -d {target} -l 500 -b google",
    "dnsrecon": "dnsrecon -d {target}",
    "nslookup": "nslookup {target}",
    "nikto": "nikto -h {target}",
    "gobuster": "gobuster dir -u {target} -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt",
    "whatweb": "whatweb {target}",
    "dnsenum": "dnsenum {target}",
    "nmap_script": "nmap -T4 -sC -A {target}",
    "live_hosts": "fping -a -g {target}",
    "smb_version": "crackmapexec smb {target} -u '/usr/share/wordlists/metasploit/unix_users.txt' -p '/usr/share/wordlists/metasploit/unix_passwords.txt'",
    "msfconsole": 'msfconsole -q -x "use auxiliary/scanner/portscan/tcp; set RHOSTS {target}; run"'
}

# Serve static files (CSS, JS, etc.)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('', filename)

# Home route (Login/Registration page)
@app.route('/')
def home():
    return render_template('index.html')  # Login/registration page


@app.route('/help.html')
def help():
    return render_template('help.html')

# Register user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Check Firebase database for existing email
    ref = db.reference('userdatabase')
    users = ref.get()

    for user_id, user_data in users.items():
        if user_data['registerEmail'] == email:
            return jsonify({'error': 'Email already registered'}), 400

    # Store user info in Firebase
    ref.push({
        'registerEmail': email,
        'password': password
    })

    return jsonify({'message': 'Registration successful'}), 200

# Analyze tools
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    option = data.get('option')
    target_url = data.get('target_url')

    if not option or not target_url:
        return jsonify({'error': 'Both option and target URL are required'}), 400

    if option not in tools:
        return jsonify({'error': 'Invalid tool selected'}), 400

    command = tools[option].format(target=target_url)
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return jsonify({'result': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Error: {e.output.strip()}'}), 500

# Send OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    otp = random.randint(100000, 999999)
    session['otp'] = otp
    session['email'] = email

    try:
        msg = Message('Your OTP Code', sender=app.config["MAIL_USERNAME"], recipients=[email])
        msg.body = f'Your OTP code is {otp}.'
        mail.send(msg)
        return jsonify({'message': 'OTP sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send OTP: {str(e)}'}), 500

# Verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    entered_otp = data.get('otp')

    if str(entered_otp) == str(session.get('otp')):  # Verify OTP
        session.pop('otp', None)
        session['logged_in'] = True
        return jsonify({'message': 'OTP verified successfully!', 'redirect': url_for('main')}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 400

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415  # Unsupported Media Type

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    ref = db.reference('userdatabase')
    users = ref.get() or {}

    for user_id, user_data in users.items():
        if user_data.get('registerEmail') == email and user_data.get('password') == password:
            session['logged_in'] = True
            return jsonify({'message': 'Login successful!'}), 200

    return jsonify({'error': 'Invalid email or password'}), 400



# Main page route
@app.route('/main')
def main():
    if 'logged_in' not in session:
        return redirect(url_for('home'))  # Redirect to login page if not logged in
    return render_template('main.html')  # Render the main.html page

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            return jsonify({'error': 'All fields are required'}), 400
        return jsonify({'message': 'Message received'}), 200
    return render_template('contact.html')


@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('home'))  # Redirect to login if not authenticated
    return render_template('dashboard.html')  # Render the dashboard.html page

@app.route('/run_tool', methods=['POST'])
def run_tool():
    tool = request.form.get('tool')
    target = request.form.get('target')

    if not tool or not target:
        return jsonify({'error': 'Tool and target are required.'}), 400

    if tool not in tools:
        return jsonify({'error': 'Invalid tool specified.'}), 400

    command = tools[tool].format(target=target)

    try:
        # Execute the command and capture the output
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)

        # Clean up the output by removing unnecessary lines
        filtered_results = []
        for line in result.splitlines():
            line = line.strip()
            # Only include relevant lines (no error or irrelevant lines)
            if line and not line.startswith(('!', '#', '---', 'Error')):
                filtered_results.append({"command": command, "output": line})

    except subprocess.CalledProcessError as e:
        filtered_results = [{"command": command, "output": f"Error: {e.output.strip()}"}]

    return render_template('result.html', tool=tool, target=target, results=filtered_results)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

@app.route('/download_report', methods=['POST'])
def download_report():
    tool_name = request.form.get('tool')
    target = request.form.get('target')
    results = request.form.getlist('results')  # Fetch the results from the form

    # Create a PDF in memory
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle("ReconXpert Tool Report")

    # Add Header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "ReconXpert Tool Report")

    # Add Tool Name and Target
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 700, f"Tool Name: {tool_name}")
    pdf.drawString(50, 680, f"Target: {target}")

    # Add Table Header
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 640, "Command")
    pdf.drawString(300, 640, "Output")
    pdf.line(50, 630, 550, 630)  # Draw a line under the header

    # Add Command and Output Rows
    pdf.setFont("Helvetica", 10)
    y_position = 610  # Start position for rows
    for result in results:
        if y_position < 50:  # Create a new page if out of space
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y_position = 750

        pdf.drawString(50, y_position, tool_name)
        pdf.drawString(300, y_position, result[:200])  # Truncate long outputs to fit
        y_position -= 20

    # Add Footer
    page_width = letter[0]  # Get page width
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(page_width / 2, y_position - 30, "Thank you for using our Advanced Recon Suite")


    # Save the PDF
    pdf.save()
    pdf_buffer.seek(0)

    # Send the PDF as a response
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{tool_name}_report.pdf",
        mimetype='application/pdf'
    )


if __name__ == '__main__':
    app.run(debug=True)

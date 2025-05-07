from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, session
import os, datetime

app = Flask(__name__)
app.secret_key = "trhacknon_secret_key"  # Pour sessions

USERNAME = "trhacknon"
PASSWORD = "trh@ckn0n"
LOG_FILE = "clicks.log"
MAIL_DIR = "mails"
TRACK_BASE_URL = "https://trackmail-8wik.onrender.com/track"  # À adapter

os.makedirs(MAIL_DIR, exist_ok=True)

def create_mail(track_id):
    track_url = f"{TRACK_BASE_URL}/{track_id}"
    html_content = f"""
    <html>
    <body style="background:#111;color:#eee;font-family:sans-serif;padding:20px;">
        <h1 style="color:#0f0;">Tirage au sort Anongame !</h1>
        <p>Participez dès maintenant à notre grand tirage au sort et tentez de gagner <strong>de nombreux cadeaux exclusifs</strong> !</p>
        <p>Cliquez sur le lien ci-dessous pour valider votre participation :</p>
        <a href="{track_url}" style="color:#0ff;font-size:18px;">{track_url}</a>
        <hr>
        <small>Organisé par Anongame - {datetime.datetime.now().strftime('%Y-%m-%d')}</small>
    </body>
    </html>
    """
    return html_content, track_url

def save_mail(content, track_id):
    filename = os.path.join(MAIL_DIR, f"mail_{track_id}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

@app.route('/track/<track_id>')
def track(track_id):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[{timestamp}] ID: {track_id} | IP: {ip}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log)
    print(log.strip())
    return render_template_string("""
    <body style="background:#000;color:#0f0;font-family:monospace;padding:40px;text-align:center;">
        <h1>Merci !</h1><p>Votre participation au tirage au sort est bien prise en compte. Nous vous souhaitons bonne chance et reviendront vers vous en cas de gain.</p>
    </body>
    """)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get("username") == USERNAME and request.form.get("password") == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template_string("""
    <body style="background:#000;color:#0f0;font-family:monospace;text-align:center;padding-top:100px;">
        <h1>trhacknon - Mail Tracker</h1>
        <form method="post">
            <input name="username" placeholder="Username" style="padding:10px;"><br><br>
            <input type="password" name="password" placeholder="Password" style="padding:10px;"><br><br>
            <button type="submit" style="padding:10px 20px;background:#0f0;color:#000;">Login</button>
        </form>
    </body>
    """)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    files = [f for f in os.listdir(MAIL_DIR) if f.endswith(".html")]
    mail_links = [f'<li><a style="color:#0ff;" href="/mails/view/{f}">{f}</a></li>' for f in files]

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.read().splitlines()
    else:
        logs = []

    return render_template_string(f"""
    <body style="background:#111;color:#fff;font-family:sans-serif;padding:30px;">
        <h2 style="color:#0f0;">Dashboard - trhacknon</h2>
        <a href="/generate" style="color:#ff0;">[+] Générer un nouveau mail</a><br><br>

        <h3 style="color:#0ff;">Mails générés</h3>
        <ul>{''.join(mail_links)}</ul>

        <h3 style="color:#f66;">Clics détectés</h3>
        <pre style="background:#000;padding:10px;color:#0f0;">{chr(10).join(logs)}</pre>
    </body>
    """)

@app.route('/generate')
def generate():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    track_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    html, link = create_mail(track_id)
    file = save_mail(html, track_id)
    return redirect(url_for('dashboard'))

@app.route('/mails/view/<filename>')
def view_mail(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory(MAIL_DIR, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

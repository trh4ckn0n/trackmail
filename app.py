from flask import Flask, request, send_from_directory, render_template_string
import os, datetime

app = Flask(__name__)
LOG_FILE = "clicks.log"
MAIL_DIR = "mails"
TRACK_BASE_URL = "https://yourdomain.onrender.com/track"

# Création du dossier mails si absent
os.makedirs(MAIL_DIR, exist_ok=True)

def create_mail(track_id):
    track_url = f"{TRACK_BASE_URL}/{track_id}"
    html_content = f"""
    <html>
    <body style="background:#111;color:#eee;font-family:sans-serif;padding:20px;">
        <h1 style="color:#0f0;">Bonjour !</h1>
        <p>Cliquez sur le lien ci-dessous :</p>
        <a href="{track_url}" style="color:#0ff;">{track_url}</a>
        <hr><small>trhacknon tracking mail - {datetime.datetime.now().strftime('%Y-%m-%d')}</small>
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
            <h1>Merci !</h1><p>Votre clic a bien été enregistré.</p>
        </body>
    """)

@app.route('/generate')
def generate():
    track_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    html, link = create_mail(track_id)
    file = save_mail(html, track_id)
    return f"""
    <body style="background:#000;color:#fff;padding:30px;font-family:sans-serif;">
        <h2 style="color:#0ff;">Mail généré</h2>
        <p><b>Track ID:</b> {track_id}</p>
        <p><b>Lien de tracking:</b> <a style='color:#0f0;' href="{link}">{link}</a></p>
        <p><b>Fichier HTML:</b> <a style='color:#0ff;' href="/mails/view/{os.path.basename(file)}">{os.path.basename(file)}</a></p>
        <a href="/mails" style="color:#ff0;">Voir tous les mails</a>
    </body>
    """

@app.route('/mails')
def list_mails():
    files = [f for f in os.listdir(MAIL_DIR) if f.endswith(".html")]
    links = [f'<li><a style="color:#0ff;" href="/mails/view/{f}">{f}</a></li>' for f in files]
    return f"""
    <body style="background:#111;color:#fff;padding:30px;">
        <h2 style="color:#0f0;">Emails générés :</h2>
        <ul>{''.join(links)}</ul>
        <a href="/generate" style="color:#ff0;">Générer un nouveau mail</a>
    </body>
    """

@app.route('/mails/view/<filename>')
def view_mail(filename):
    return send_from_directory(MAIL_DIR, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

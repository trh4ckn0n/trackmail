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
    
    # Contenu HTML principal
    html_content = f"""
    <html>
    <body style="background:#111;color:#eee;font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;padding:30px;line-height:1.6;">
        <div style="max-width:600px;margin:auto;border:2px solid #0f0;padding:20px;border-radius:10px;background:#000;">
            <h1 style="color:#0f0;text-align:center;">Gagnez gros avec Anongame !</h1>
            <p style="font-size:16px;">Vous avez été sélectionné pour participer à notre <strong style="color:#ff0;">grand tirage au sort exclusif</strong> !</p>
            <p style="font-size:16px;">De nombreux lots sont à gagner, dont :</p>
            <ul style="color:#0ff;font-size:15px;">
                <li>Cartes cadeaux Amazon, PlayStation, Steam...</li>
                <li>Crypto-monnaie (BTC, ETH...)</li>
                <li>Équipements gaming, accessoires tech</li>
                <li>Et bien plus encore !</li>
            </ul>
            <p style="margin-top:30px;font-size:16px;">Pour participer, il vous suffit de cliquer sur le lien ci-dessous :</p>
            <div style="text-align:center;margin:30px 0;">
                <a href="{track_url}" style="background:#0f0;color:#000;padding:12px 25px;text-decoration:none;font-weight:bold;border-radius:5px;font-size:18px;">Je participe maintenant</a>
            </div>
            <p style="color:#aaa;font-size:14px;">Faites vite, les places sont limitées et le tirage aura lieu dans moins de 48h !</p>
            <hr style="border:1px solid #333;">
            <small style="color:#666;">Organisé par Anongame | {datetime.datetime.now().strftime('%Y-%m-%d')}</small>
        </div>
    </body>
    </html>
    """

    # HTML pour affichage dans un <textarea>
    html_textarea = f"""
    <div style="max-width:600px;margin:auto;margin-top:40px;text-align:center;">
        <h2 style="color:#0f0;">Copiez le code source HTML du mail</h2>
        <textarea id="html_code" style="width:100%;height:200px;background:#222;color:#0f0;border:1px solid #0f0;padding:10px;border-radius:5px;font-family:monospace;font-size:14px;">{html_content}</textarea><br><br>
        <button onclick="copyToClipboard()" style="background:#0f0;color:#000;padding:10px 20px;border:none;border-radius:5px;font-size:16px;">Copier le code</button>
    </div>
    
    <script>
    function copyToClipboard() {{
        var copyText = document.getElementById("html_code");
        copyText.select();
        copyText.setSelectionRange(0, 99999); // Pour mobile
        document.execCommand("copy");
        alert("Code HTML copié dans le presse-papier !");
    }}
    </script>
    """
    
    # Combiner le contenu HTML principal et l'élément textarea
    full_html = html_content + html_textarea
    
    return full_html, track_url

def save_mail(content, track_id):
    filename = os.path.join(MAIL_DIR, f"mail_{track_id}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

@app.route('/track/<track_id>')
def track(track_id):
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ID: {track_id} | IP: {visitor_ip}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    print(log_entry.strip())

    return f"""
    <html>
    <body style="background:#111;color:#eee;font-family:sans-serif;text-align:center;padding:50px;">
        <h1 style="color:#0f0;">Participation enregistrée !</h1>
        <p>Merci d'avoir cliqué sur le lien.</p>
        <p>Votre participation au tirage au sort <strong>Anongame</strong> a bien été prise en compte.</p>
        <p>Bonne chance !</p>
        <hr>
        <small style="color:#666;">Votre IP : {visitor_ip} | {timestamp}</small>
    </body>
    </html>
"""

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

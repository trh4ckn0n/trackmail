from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, session
import os, datetime

app = Flask(__name__)
app.secret_key = "trhacknon_secret_2025"
LOG_FILE = "clicks.log"
MAIL_DIR = "mails"
PASSWORD = "trknmail"  # change ici ton mot de passe

# HTML STYLES
STYLE = """
<style>
  body {
    background-color: #0d0d0d;
    color: #39ff14;
    font-family: monospace;
    padding: 30px;
  }
  h1, h2 {
    color: #00ffff;
  }
  ul {
    list-style: none;
    padding-left: 0;
  }
  li {
    margin-bottom: 10px;
  }
  a {
    color: #ff00ff;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
  .form-group {
    margin: 10px 0;
  }
  input[type="password"] {
    padding: 5px;
    background: #111;
    color: #39ff14;
    border: 1px solid #39ff14;
  }
  button {
    background: #39ff14;
    color: #000;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
  }
</style>
"""

@app.route('/track/<track_id>')
def track(track_id):
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ID: {track_id} | IP: {visitor_ip}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    print(log_entry.strip())
    return f"{STYLE}<h1>Merci !</h1><p>Votre lien a été enregistré.</p>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for('list_mails'))
        else:
            return f"{STYLE}<h2>Mot de passe incorrect.</h2><a href='/login'>Réessayer</a>"
    
    return f"""
    {STYLE}
    <h1>Connexion</h1>
    <form method="POST">
        <div class="form-group">
            <input type="password" name="password" placeholder="Mot de passe" required>
        </div>
        <button type="submit">Se connecter</button>
    </form>
    """

@app.route('/mails')
def list_mails():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    files = os.listdir(MAIL_DIR)
    files = [f for f in files if f.endswith(".html")]
    links = [f'<li><a href="/mails/view/{f}">{f}</a></li>' for f in files]
    return f"{STYLE}<h2>Emails générés :</h2><ul>{''.join(links)}</ul>"

@app.route('/mails/view/<filename>')
def view_mail(filename):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return send_from_directory(MAIL_DIR, filename)

if __name__ == '__main__':
    os.makedirs(MAIL_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=5000)

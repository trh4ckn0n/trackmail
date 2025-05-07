import os
from datetime import datetime

MAIL_DIR = "mails"
BASE_URL = "http://your-server-ip-or-domain:5000/track"
TRACK_ID = datetime.now().strftime("%Y%m%d%H%M%S")

def create_mail(track_id, recipient_name=""):
    url = f"{BASE_URL}/{track_id}"
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Message</title>
</head>
<body style="background:#0d0d0d;color:#39ff14;font-family:monospace;padding:30px">
  <h1 style="color:#00ffff">Bonjour {recipient_name or 'utilisateur'} !</h1>
  <p>Nous avons une information importante pour vous.</p>
  <p><a href="{url}" style="color:#ff00ff">Cliquez ici pour consulter</a></p>
  <hr>
  <small style="color:#888">Lien de tracking : {url}</small>
</body>
</html>"""
    return html, url

def save_mail(html, track_id):
    os.makedirs(MAIL_DIR, exist_ok=True)
    filepath = os.path.join(MAIL_DIR, f"track_{track_id}.html")
    with open(filepath, "w") as f:
        f.write(html)
    return filepath

if __name__ == "__main__":
    print("=== Générateur d'email avec lien tracké ===")
    name = input("Nom du destinataire (optionnel) : ").strip()
    track_id = TRACK_ID
    html, url = create_mail(track_id, name)
    path = save_mail(html, track_id)

    print(f"\nMail enregistré dans : {path}")
    print(f"Lien à envoyer : {url}")

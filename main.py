import requests
import smtplib, ssl
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

to_addr=os.getenv("destination_email")
from_addr=os.getenv("my_email")
app_password = os.getenv("password")

print(f"from: {from_addr}, pass length: {len(app_password) if app_password else 'NONE'}")

def send_email(subject, body, to_addr, from_addr, app_password):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    context=ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_addr, app_password)
        server.sendmail(from_addr, to_addr, msg.as_string())

def get_top_games(limit):
    response = requests.get("https://steamspy.com/api.php?request=top100in2weeks")
    data = response.json()
    top_games = sorted(data.values(), key=lambda x: x["ccu"], reverse=True)[:limit]
    return top_games

def format_games(top_games):
    body = "" 
    for game in top_games:
        body += f"{game['name']}: {game['ccu']:,} players<br>"
    return body

if __name__ == "__main__":
    games = get_top_games(limit=20)
    body = format_games(games)
    send_email("Top 10 Steam Games Today", body, to_addr=to_addr, from_addr=from_addr, app_password=app_password)

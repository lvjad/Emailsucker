import smtplib
import sys
import time
from email.mime.text import MIMEText
from getpass import getpass

BANNER = r"""
▄▄▄█████▓ ██░ ██ ▓█████  ███▄    █ ▓█████▄  ▒█████  
▓  ██▒ ▓▒▓██░ ██▒▓█   ▀  ██ ▀█   █ ▒██▀ ██▌▒██▒  ██▒
▒ ▓██░ ▒░▒██▀▀██░▒███   ▓██  ▀█ ██▒░██   █▌▒██░  ██▒
░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ ▓██▒  ▐▌██▒░▓█▄   ▌▒██   ██░
  ▒██▒ ░ ░▓█▒░██▓░▒████▒▒██░   ▓██░░▒████▓ ░ ████▓▒░
  ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ 
    ░     ▒ ░▒░ ░ ░ ░  ░░ ░░   ░ ▒░ ░ ▒  ▒   ░ ▒ ▒░ 
  ░       ░  ░░ ░   ░      ░   ░ ░  ░ ░  ░ ░ ░ ░ ▒  
          ░  ░  ░   ░  ░         ░    ░        ░ ░  
                                    ░              
"""

print(BANNER)


smtp_server   = input("SMTP server (e.g. smtp.gmail.com): ").strip()
smtp_port     = int(input("SMTP port (465=SSL, 587=STARTTLS): ").strip() or 465)
username      = input("SMTP username (your e-mail): ").strip()
password      = getpass("SMTP password / app-password: ").strip()
recipient     = input("Recipient (leave blank = same as username): ").strip() or username
subject       = "THENDO FOUND YOU"
body_text     = "This is test message #{i} of {total}"
count         = int(input("How many e-mails to send? ").strip() or 1000)
delay_seconds = float(input("Delay between sends (seconds, 0 = no wait): ").strip() or 0)


try:
    if smtp_port == 465:
        server = smtplib.SMTP_SSL(smtp_server, 465)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
    server.login(username, password)
except Exception as e:
    sys.exit(f"SMTP login failed: {e}")

print("\n[+] Connected. Sending …")

for i in range(1, count + 1):
    msg = MIMEText(body_text.format(i=i, total=count))
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = recipient
    try:
        server.sendmail(username, [recipient], msg.as_string())
        print(f"Sent {i}/{count}", end="\r")
    except Exception as e:
        print(f"\nSend failed at {i}: {e}")
        break
    if delay_seconds > 0:
        time.sleep(delay_seconds)

server.quit()

print("\nDone. Check your inbox .")

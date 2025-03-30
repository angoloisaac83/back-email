import os
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS  # 🛠 Fixes CORS issue
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)  # 🔥 Enable CORS for all requests

# 🔹 SMTP Configuration
SMTP_SERVER = "mail.primelend.online"
SMTP_PORT = 465
SMTP_USER = "supportken@primelend.online"
SMTP_PASSWORD = "your-email-password"

# 🔹 Email Sending Function
def send_email(to_email, subject, body):
    real_from_email = SMTP_USER
    fake_from_name = "Namecheap Support"
    fake_from_email = "support@namecheap.org"

    msg = MIMEMultipart()
    msg["From"] = f"{fake_from_name} <{real_from_email}>"
    msg["Reply-To"] = fake_from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(real_from_email, to_email, msg.as_string())
        server.quit()
        return {"success": True, "message": "✅ Email sent successfully!"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# 🔹 API Route to Send Emails
@app.route("/send-email", methods=["POST"])
def send_email_api():
    data = request.json
    to_email = data.get("to_email")
    subject = data.get("subject", "Test Email")
    body = data.get("body", "This is a test email.")

    if not to_email:
        return jsonify({"error": "❌ Missing 'to_email' parameter"}), 400

    result = send_email(to_email, subject, body)
    return jsonify(result)

# 🔹 Fix for Render Deployment
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

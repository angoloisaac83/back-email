from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# SMTP Configuration
SMTP_SERVER = "mail.primelend.online"
SMTP_PORT = 465
SMTP_USER = "supportken@primelend.online"
SMTP_PASSWORD = "123Junior$$"

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        to_email = data["to_email"]
        message_body = data["message"]

        # Create Email
        msg = MIMEMultipart()
        msg["From"] = f"Support <{SMTP_USER}>"  # Your domain email
        msg["To"] = to_email
        msg["Subject"] = "Message from Web App"
        msg.attach(MIMEText(message_body, "plain"))

        # Send Email
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()

        return jsonify({"message": "Email sent successfully!"})

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

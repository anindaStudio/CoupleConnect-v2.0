import requests

SERVICE_ID = "service_sj3eyf4"      # তোমারটা
TEMPLATE_ID = "YOUR_TEMPLATE_ID"    # EmailJS থেকে
PUBLIC_KEY = "YOUR_PUBLIC_KEY"      # EmailJS → Account → API Keys

def send_email_invite(to_email, sender_email):
    url = "https://api.emailjs.com/api/v1.0/email/send"

    payload = {
        "service_id": SERVICE_ID,
        "template_id": TEMPLATE_ID,
        "user_id": PUBLIC_KEY,
        "template_params": {
            "to_email": to_email,      # ⚠️ template-এ {{to_email}} থাকতে হবে
            "from_name": sender_email  # ⚠️ template-এ {{from_name}} থাকতে হবে
        }
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        # debug চাইলে:
        # print(res.status_code, res.text)
        return res.status_code == 200
    except Exception as e:
        print("Email error:", e)
        return False
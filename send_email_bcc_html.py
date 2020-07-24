#!/usr/bin/env python3

try:
    import smtplib
    import email.message
except ImportError:
    raise Exception('Missing Python3 modules')

smtp_server = "smtp.example.com"
port = 25
sender = "joro@example.com"
recepients = ["john_doe@example.net"]
bcc_folks  = ["jane_doe@example.net", "janie_doe@example.edu"]
subject = 'Important accounts migration'

email_content = """
<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<body>
<font face="Arial" size="3">
<p>[bcc: Users on these two servers]<br />
<p><a href="https://someurlhere.com/projects/42815</a></p>
<p>We will be moving all users on ServerA and ServerB to a different machines starting Feb 21 at 00:00 and ending Feb 24 at 08:00.</p>
<p>In the next months, we plan to redeploy all servers to version XXX.</p>
<p>Your hostname and path will be changed. We will automatically change your files to match the new paths. All of your data will be preserved and moved.</p>
<p>Regards,<br />DevOps team</p>
</font>
</body>
</html>
"""
msg = email.message.Message()
msg.add_header('Content-Type', 'text/html')
msg['Subject'] = subject
msg.set_payload(email_content)

try:
    s = smtplib.SMTP(smtp_server,port)
    s.ehlo()
    s.sendmail(sender, recepients + bcc_folks, msg.as_string())
except Exception as e:
    print(e)
finally:
    s.quit()

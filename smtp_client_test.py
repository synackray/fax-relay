#!/usr/bin/env python3

import smtplib

senders = ["bad@example.org", "good@example.com"]
rcpts = ["victim@example.net", "6158675309@example.org"]

message = """Subject: Test

This is a test message.
"""

for sender in senders:
    try:
       smtpObj = smtplib.SMTP("localhost", 1025)
       smtpObj.sendmail(sender, rcpts, message)
       print(f"Successfully sent email from {sender} to {rcpts}.")
       smtpObj.quit()
    except smtplib.SMTPException as e:
       print(f"Error: {e}.")

#!/usr/bin/env python3

import smtplib

SENDERS = ["bad@example.org", "good@example.com"]
RCPTS = ["victim@example.net", "6158675309@example.org"]

MESSAGE = """Subject: Test

This is a test message.
"""

for sender in SENDERS:
    try:
        smtpObj = smtplib.SMTP("localhost", 1025)
        smtpObj.sendmail(sender, RCPTS, MESSAGE)
        print(f"Successfully sent email from {sender} to {RCPTS}.")
        smtpObj.quit()
    except smtplib.SMTPException as error:
        print(f"Error: {error}.")

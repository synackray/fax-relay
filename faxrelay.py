#!/usr/bin/env python

'''
Fax Relay Server
Version: 1.0.1
Author: Raymond Beaudoin

Usage: This script acts as a mail server. It accepts incoming connections,
formats the recipient(s) to the format expected by the fax server, and
relays the message to the fax server.
'''

import asyncore
import logging
import re
import smtpd
import smtplib

# Modifiable Variables
PERMITTED_SENDERS = ["example.com"]
PERMITTED_RECIPIENT_DOMAINS = ["example.org"]
FAX_SERVER = "192.0.2.1"
LOG_DIRECTORY = "logs/faxrelay.log"

# Do not modify anything below

logging.basicConfig(filename=LOG_DIRECTORY, level=logging.INFO, \
format='%(asctime)s %(message)s')

class CustomSMTPServer(smtpd.SMTPServer):
    """SMTP Relay with sender and recepient parsing, message formatting, and
    forwarding to destination fax server.
    """
    logging.info("Fax relay server enabled. Listening for incoming emails.")

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        logging.info(
            "Received message from %s, to %s, with message length %s.",
            mailfrom, rcpttos, len(data))

        # Run for every recipient in the message
        for recipient in rcpttos:
            sender = mailfrom.split('@')[1].lower()
            recipient_name = recipient.split('@')[0]
            recipient_domain = recipient.split('@')[1].lower()
            # Verify sender is permitted and recipient is 10-digit number
            if sender not in PERMITTED_SENDERS:
                logging.info(
                    "Sender %s is not permitted. Message discarded.",
                    mailfrom)
            # If send tries to sends to anything besides 10-digit.
            elif sender in PERMITTED_SENDERS and \
            re.match('^[0-9]{10,10}$', recipient_name) is None:
                logging.info(
                    "Sender %s is trying to send to non 10-digit destination "
                    "%s. Message discarded.", mailfrom, recipient)
            # If match, set new recipient to Fax expected format
            elif sender in PERMITTED_SENDERS and \
            re.match('^[0-9]{10,10}$', recipient_name) is not None \
            and recipient_domain in PERMITTED_RECIPIENT_DOMAINS:
                relay_recipient = "IMCEAFAX-%s@%s" % (recipient_name, \
                    recipient_domain)
                logging.info(
                    "Sending message from %s to %s at %s.", mailfrom,
                    relay_recipient, FAX_SERVER)
                # Take received message and send it to fax server
                # with formated to address
                smtp_server = smtplib.SMTP(FAX_SERVER)
                # Uncomment to debug messages being sent to the fax system
                #smtp_server.set_debuglevel(1)
                smtp_server.sendmail(mailfrom, relay_recipient, data)
                smtp_server.quit()
            else:
                logging.info(
                    "Unknown error with message from %s to %s. "
                    "Message discarded.", mailfrom, recipient)


SERVER = CustomSMTPServer(('0.0.0.0', 1025), None)
asyncore.loop()

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
import sys

# Modifiable Variables
permitted_senders = ["example.com"]
permitted_recipient_domains = ["example.org"]
fax_server = "192.0.2.1"
log_directory = "logs/faxrelay.log"

# Do not modify anything below

logging.basicConfig(filename=log_directory, level=logging.INFO, \
format='%(asctime)s %(message)s')

class CustomSMTPServer(smtpd.SMTPServer):
    logging.info("Fax relay server enabled. Listening for incoming emails.")

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        logging.info("Received message from %s, to %s, with message length %s." \
        % (mailfrom, rcpttos, len(data)))

        # Run for every recipient in the message
        for recipient in rcpttos:
            sender = mailfrom.split('@')[1].lower()
            recipient_name = recipient.split('@')[0]
            recipient_domain = recipient.split('@')[1].lower()
            # Verify sender is permitted and recipient is 10-digit number
            if sender not in permitted_senders:
                logging.info("Sender %s is not permitted. Message discarded." \
                % (mailfrom))
            # If send tries to sends to anything besides 10-digit.
            elif sender in permitted_senders and \
            re.match('^[0-9]{10,10}$', recipient_name) is None:
                logging.info("Sender %s is trying to send to non 10-digit "
                    "destination %s. Message discarded." \
                % (mailfrom, recipient))
            # If match, set new recipient to Fax expected format
            elif sender in permitted_senders and \
            re.match('^[0-9]{10,10}$', recipient_name) is not None \
            and recipient_domain in permitted_recipient_domains:
                relay_recipient = "IMCEAFAX-%s@%s" % (recipient_name, \
                    recipient_domain)
                logging.info("Sending message from %s to %s at %s." \
                % (mailfrom, relay_recipient, fax_server))
                # Take received message and send it to fax server
                # with formated to address
                smtp_server = smtplib.SMTP(fax_server)
                # Uncomment to debug messages being sent to the fax system
                #smtp_server.set_debuglevel(1)
                smtp_server.sendmail(mailfrom, relay_recipient, data)
                smtp_server.quit()
            else:
                logging.info("Unknown error with message from %s to %s. "
                    "Message discarded." \
                    % (mailfrom, recipient))


server = CustomSMTPServer(('0.0.0.0', 1025), None)
asyncore.loop()

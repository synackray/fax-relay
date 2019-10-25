# fax-relay

Fax Relay is a SMTP server which listens for inbound e-mails and converts them to IMCEAFAX formatted messages to a fax server. Basic security features are included to ensure only particular source and destination domains are accepted.

All requests are logged and output as "faxrelay.log". A statistics script is included to generate JSON formatted output of daily usage statistics based on the log file.

## Installation

**Method 1 - Run the Script**
1. Run the script! There are no dependencies other than Python3.

**Method 2 - Create a Python Venv**
1. Browse to the project folder.
2. Create Python Virtual Environment [(venv)](https://docs.python.org/3/library/venv.html) and activate it.
4. Run the script!

```
cd fax-relay
python3 -m venv .
python faxrelay.py
```

## Usage

The server listens on tcp/1025 by default to avoid needing to be ran as root. Once activated it listens for incoming messages, validates the sender and recipient domains, and then passes the message to the fax server.

```
user@demo ~ $ python3 faxrelay.py &
2019-09-03 17:46:02,688 Fax relay server enabled. Listening for incoming emails.
2019-09-03 17:46:32,851 Received message from user@gooddomain.com, to ['1234567890@example.com'], with message length 241662.
2019-09-03 17:46:33,178 Sending message from user@gooddomain.com to IMCEAFAX-1234567890@example.com at 192.0.2.1.
2019-08-29 17:51:02,584 Received message from user@baddomain.com, to ['1234567890@example.com'], with message length 302967.
2019-08-29 17:51:02,875 Sender user@baddomain.com is not permitted. Message discarded.
```

import random
import smtplib

import time

import parse


def mail_merge(stri, human):
    """Replaces fName lName and Email with the actual values
    human:
    [0] - fName
    [1] - lName
    [2] - email address
    """
    new_str = stri
    new_str = new_str.replace('{{First Name}}', human[0])
    new_str = new_str.replace('{{Last Name}}', human[1])
    new_str = new_str.replace('{{Email Address}}', human[2])
    return new_str


def start_mailing(fr, subj, texT, passworD, human):
    """
    Sends an e-mail via smtp server. Destination address is being taken from human[2].
    :texT: - Not parsed message text. Can have {{args}} in it. MUST BE MAIL MERGED
    :subj: - Must be mailmerged too
    :passworD: - is not encoded
    Human:
    [0] - First Name
    [1] - Second Name
    [2] - Destination address
    """
    from_address = fr[0].decode("utf-8")
    to_address = human[2]
    subj = subj[0].decode("utf-8")
    TO = to_address
    FROM = from_address
    SUBJECT = subj
    SUBJECT = mail_merge(SUBJECT, human)
    text = texT[0].decode("utf-8")
    text = mail_merge(text, human)
    BODY = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        text
    ))
    username = from_address
    password = passworD[0].decode("utf-8")
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    print("Sending your message from {} to {}".format(from_address, to_address))
    server.sendmail(from_address, [to_address], BODY)
    server.quit()


if __name__ == '__main__':
    raise NotImplementedError


def start(fr, subj, text, password, spreadsheet):
    """Gets human data from a spreadsheet and mails every human on the list"""
    parsed = parse.parse_sheet(spreadsheet)
    for human in parsed:
        start_mailing(fr, subj, text, password, human)
        n = random.randint(10, 15)
        print("Sleeping for {} seconds".format(n))
        time.sleep(n)

    print("All messages have been successfully sent!")

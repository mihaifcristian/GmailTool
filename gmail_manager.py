from imap_tools import MailBox, AND
import datetime as dt
import pprint
import re

# initial_folder = '[Gmail]/Sent Mail'  # 'INBOX' , '[Gmail]/Sent Mail', '[Gmail]/All Mail'
username = '<email_username>'
password = '<email_password>'
imap = 'imap.gmail.com'
mailbox = MailBox(imap)
default_folder = 'INBOX'
mailbox.login(username, password, initial_folder=default_folder)
moved_to_trash = []


# FIND EMAILS IN A FOLDER BY SPECIFIC SUBJECT GIVE IT
def find_emails_on_email_body(folder, subject):
    # mailbox.login(username, password, initial_folder=folder)
    folder if folder is not None else default_folder
    msg_text = [msg.text for msg in mailbox.fetch(AND(subject=subject))]
    for msg in msg_text:
        e_mail = re.findall(r'[\w\.-]+@[\w\.-]+', msg)
        pprint.pprint(e_mail)


# LIST ALL FOLDER AND SUBFOLDER FROM A SPECIFIC LOCATION AND RETURN A LIST WITH EVERY FOLDER THAT CAN BE ITERATED
def list_folders(folder):
    folder if folder is not None else default_folder
    mailbox.folder.set(folder)
    folder_list = []
    for folder_info in mailbox.folder.list(folder):
        folder_list.append(folder_info['name'])  # Take the dictionary with folders and keep just 'name' key value
    return folder_list  # List can be used to find emails on it


# FIND ALL EMAIL BY SPECIFIC SUBJECT
def list_emails_from_subject(folder, subject):
    folder if folder is not None else default_folder
    mailbox.folder.set(folder)
    subjects = [msg.subject for msg in mailbox.fetch(AND(subject=subject))]
    return subjects


def move_to_trash(folders, days_before, subject=None):
    for folder in folders:
        mailbox.folder.set(folder)
        before_date = (dt.date.today() - dt.timedelta(days_before))  # Create date to take all mail before this date
        if subject:
            uid_list = [msg.uid for msg in mailbox.fetch(AND(subject=subject, date_lt=before_date))]
        else:
            uid_list = [msg.uid for msg in mailbox.fetch(AND(date_lt=before_date))]
        mailbox.move(uid_list, '[Gmail]/Trash')
        moved_to_trash.append(uid_list)
    return moved_to_trash


def empty_trash():
    mailbox.folder.set('[Gmail]/Trash')
    mailbox.delete([msg.uid for msg in mailbox.fetch()])


# RUN THE METHODS BESIDE
# pprint.pprint(find_emails_on_email_body('INBOX', 'Undelivered Mail Returned to Sender'))
# pprint.pprint(list_emails_from_subject('INBOX', 'Undelivered Mail Returned to Sender'))
# print(list_folders('INBOX'))
# pprint.pprint(len(move_to_trash(list_folders('[Gmail]/All Mail'), 90)))
# find_emails_on_email_body('[Gmail]/Trash', 'alarm GDA 90953')
pprint.pprint(list_emails_from_subject('[Gmail]/Trash', 'alarm'))
# empty_trash()
mailbox.logout()
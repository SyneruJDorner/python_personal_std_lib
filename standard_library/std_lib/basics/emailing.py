import win32com.client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EMAIL():
    '''
    This class is used to send emails with either outlook or gmail
    '''
    class GMAIL():
        '''
        A class to send emails using gmail.

        More info can be be found at:
        Allow 'less secure apps' in order to use with SMTP\n
        https://support.google.com/accounts/answer/6010255?hl=en
        '''
        @classmethod
        def send_email(cls, email_structure):
            '''
            Send an email using gmail.

            Parameters
            ----------
            email_structure: dict
                A dictionary with the following keys:
                'username': str
                    The username of the gmail account.
                'password': str
                    The password of the gmail account.
                'from': str
                    The sender of the email.
                'to': str
                    The email address of the recipient.
                'cc': str
                    The email address of the cc recipient.
                'bcc': str
                    The email address of the bcc recipient.
                'subject': str
                    The subject of the email.
                'body': str
                    The body of the email.
                'attachments': str
                    The path to the attachments.

            email_structure example:
                email_structure = {
                "username": "your_username@gmail.com",
                "password": "yourpasswordforgmail",
                "from": "your_username@gmail.com",
                "to": "recipient@gmail.com",
                "cc": "recipient_cc@gmail.com",
                "bcc": "recipient_bcc@gmail.com",
                "subject": "What is your subject?",
                "body": "Write your email message."
            }
            '''
            message = MIMEMultipart()
            message['From'] = email_structure["from"]
            message['To'] = email_structure["to"]
            message['Subject'] = email_structure["subject"]
            message.attach(MIMEText(email_structure['body'], 'plain'))

            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(email_structure["username"], email_structure["password"])
            text = message.as_string()
            session.sendmail(email_structure["from"], email_structure["to"], text)
            session.quit()


    class OUTLOOK():
        '''
        A class to send emails using outlook.

        More info can be found at:
        Set 'Programmatic Access Security' to 'Never warn me about suspicious activity'\n
        https://docs.microsoft.com/en-us/outlook/troubleshoot/security/a-program-is-trying-to-send-an-email-message-on-your-behalf
        '''

        @classmethod
        def send_email(cls, email_structure):
            '''
            Send an email using outlook.

            Parameters
            ----------
            email_structure: dict
                A dictionary with the following keys:
                'from': str
                    The sender of the email.
                'to': str
                    The email address of the recipient.
                'cc': str
                    The email address of the cc recipient.
                'bcc': str
                    The email address of the bcc recipient.
                'subject': str
                    The subject of the email.
                'body': str
                    The body of the email.
                'attachments': array
                    The path to the attachments.

            email_structure example:
                email_structure = {
                "from": "your_username@gmail.com",
                "to": "recipient@gmail.com",
                "cc": "recipient_cc@gmail.com",
                "bcc": "recipient_bcc@gmail.com",
                "subject": "What is your subject?",
                "body": "Write your email message."
                "attachments": ["", "", "", "", ""]
            }
            '''
            outlook = win32com.client.Dispatch("Outlook.Application")
            mapi = outlook.GetNamespace("MAPI")
            mail = outlook.createItem(0)
            mail.SendUsingAccount = email_structure["from"]
            mail.SentOnBehalfOfName = email_structure["from"]
            mail.To = email_structure["to"]
            mail.CC = email_structure["cc"]
            mail.BCC = email_structure["bcc"]
            mail.Subject = email_structure["subject"]
            mail.Body = email_structure["body"]

            for attachment in email_structure["attachments"]:
                mail.Attachments.Add(attachment)

            for outlook_emails in outlook.Session.Accounts:
                print(outlook_emails)
                if email_structure["from"].lower() in str(outlook_emails).lower():
                    From = outlook_emails
                    break

            if From != None:
                # This line basically calls the "mail.SendUsingAccount = xyz@email.com" outlook VBA command
                mail._oleobj_.Invoke(*(64209, 0, 8, 0, From))
                mail.Send()

        @classmethod    
        def get_base_email_structure(cls):
            '''
            A function that returns a base email structure.

            Returns a dictionary with the following keys:
            'from': str
                The sender of the email.
            'to': str
                The email address of the recipient.
            'cc': str
                The email address of the cc recipient.
            'bcc': str
                The email address of the bcc recipient.
            'subject': str
                The subject of the email.
            'body': str
                The body of the email.
            'attachments': array
                The path to the attachments.
            '''
            email_structure = {
                "from": "",
                "to": "",
                "cc": "",
                "bcc": "",
                "subject": "",
                "body": "",
                "attachments": []
            }
            return email_structure
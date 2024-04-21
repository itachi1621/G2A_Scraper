from mailersend import emails;

def send_email(from_email,recipients:list,subject,text,html,api_key:str=None):
    try:
        mailer = emails.NewEmail(api_key)
        mail_body = {}
        mail_from ={
            "email": from_email
        }
        recipients = [{"email": recipient} for recipient in recipients]
        mailer.set_mail_from(mail_from,mail_body)
        mailer.set_mail_to(recipients,mail_body)
        mailer.set_subject(subject,mail_body)
        mailer.set_plaintext_content(text,mail_body)
        mailer.set_html_content(html,mail_body)
        response = mailer.send(mail_body)
        print(response)
    except Exception as e:
        print(e)
        return False



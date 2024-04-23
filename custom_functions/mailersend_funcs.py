from mailersend import emails;

def send_email(from_email,from_name,recipients:list,subject,text,html,api_key:str=None):
    try:
        mailer = emails.NewEmail(api_key)
        mail_body = {}
        mail_from ={
            "name": from_name,
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
        print('Email sent successfully')
    except Exception as e:
        print(e)
        print('Email failed to send')
        return False



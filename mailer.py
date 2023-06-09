import smtplib
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(send_from, password, send_to, subject, message):
    """
    sends mail without any attachment
    """

    for receiver in send_to:
        multipart = MIMEMultipart()
        multipart["From"] = send_from
        multipart["To"] = receiver
        multipart["Subject"] = subject

        multipart.attach(MIMEText(message, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(send_from, password)
        server.sendmail(send_from, receiver, multipart.as_string())
        server.quit()


def send_email_with_df(dataframes, file_names, send_from, password, send_to, subject):
    """
    accepts List of dataframes with list of file names
    """
    message = f"""\
    <p><strong>Data for the day today&nbsp;</strong></>
    <p><br></p>
    <p><strong>Regards&nbsp;</strong><br><strong>Aditya MS&nbsp;    </strong></p>
    """

    for receiver in send_to:
        multipart = MIMEMultipart()
        multipart["From"] = send_from
        multipart["To"] = receiver
        multipart["Subject"] = subject

        for df, file_name in zip(dataframes, file_names):
            attachment = MIMEApplication(df.to_csv())
            attachment["Content-Disposition"] = 'attachment; filename="{}"'.format(
                f"{file_name}.csv"
            )
            multipart.attach(attachment)

        multipart.attach(MIMEText(message, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(send_from, password)
        server.sendmail(send_from, receiver, multipart.as_string())
        server.quit()

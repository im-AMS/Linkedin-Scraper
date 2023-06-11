import logging as log
from datetime import date
from email import message
from logging import error
from time import strftime

import pandas as pd
import yaml

from linkedin import linkedin
from mailer import send_email, send_email_with_df
from naukri import naukri

log.basicConfig(
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    level=log.INFO,
)

with open("config.yaml", "r") as file:
    tmp = yaml.safe_load(file)

send_from = tmp["from"]["mail"]
send_password = tmp["from"]["password"]
send_subject = tmp["from"]["subject"]
send_subject = f"{date.today().strftime('%B %d, %Y')} {send_subject}"

send_to = tmp["to"]["mail"]

dev_mail = tmp["dev"]["mail"]

print(send_subject)

dataframes = []
file_names = []
error_message = ""

try:
    log.info(f"Trying to scrape linkedin")
    linked_df = linkedin()
    dataframes.append(linked_df)
    file_names.append("linkedin")

except Exception as e:
    log.info(f"Linkedin failed!!!, {e}")
    error_message = f"{error_message}Linkedin Failed!!!\n{e}\n"

try:
    log.info(f"Trying to scrape naukri")
    naukri_df = naukri()
    dataframes.append(naukri_df)
    file_names.append("naukri")
except Exception as e:
    log.info(f"Naukri failed!!!, {e}")
    error_message = f"{error_message}Naukri Failed!!!\n{e}\n"

if len(error_message) == 0:
    log.info(f"Sending scraped data")
    send_email_with_df(
        dataframes,
        file_names,
        send_from,
        send_password,
        send_to,
        send_subject,
    )
    log.info(f"Sent data. Good Bye for now!")

else:
    log.info(f"Sending Error message to dev, {dev_mail}")
    send_email(
        send_from,
        send_password,
        dev_mail,
        f"{date.today().strftime('%B %d, %Y')} Scrape Failed",
        error_message,
    )
    log.info(f"Sent mail to dev, killing myself to be fixed soon!")

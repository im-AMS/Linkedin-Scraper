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
    linked_df = linkedin()
    dataframes.append(linked_df)
    file_names.append("linkedin")

except Exception as e:
    error_message = f"{error_message}Linkedin Failed!!!\n{e}\n"

try:
    naukri_df = naukri()
    dataframes.append(naukri_df)
    file_names.append("naukri")
except Exception as e:
    error_message = f"{error_message}Naukri Failed!!!\n{e}\n"

if len(error_message) == 0:
    send_email_with_df(
        dataframes,
        file_names,
        send_from,
        send_password,
        send_to,
        send_subject,
    )
else:
    send_email(
        send_from,
        send_password,
        dev_mail,
        f"{date.today().strftime('%B %d, %Y')} Scrape Failed",
        error_message,
    )

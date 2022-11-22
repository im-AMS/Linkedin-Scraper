import os
import pandas as pd
import numpy as np
import requests
import random
import time
from datetime import datetime
from bs4 import BeautifulSoup
import bs4
import re
from joblib import Parallel, delayed
import traceback
import itertools
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


scrape_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")


# For mailer
def send_email(send_to, subject, df, file_name):
    send_from = "ams.mailer.1@gmail.com"
    password = "zaudiemkclttfmbo"
    message = f"""\
    <p><strong>Data for the day {scrape_time}&nbsp;</strong></>
    <p><br></p>
    <p><strong>Regards&nbsp;</strong><br><strong>Aditya MS&nbsp;    </strong></p>
    """
    for receiver in send_to:
        multipart = MIMEMultipart()
        multipart["From"] = send_from
        multipart["To"] = receiver
        multipart["Subject"] = subject  
        attachment = MIMEApplication(df.to_csv())
        attachment["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{file_name}.csv")
        multipart.attach(attachment)
        multipart.attach(MIMEText(message, "html"))
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(multipart["From"], password)
        server.sendmail(multipart["From"], multipart["To"], multipart.as_string())
        server.quit()









with open("user-agents.txt", "r") as text_file:
     user_agents = text_file.readlines()



class to_df:
    
    list_cls__ = "jobs-search__results-list"
    title_cls__ = "base-search-card__title"
    company_cls__ = "base-search-card__subtitle"
    loc_cls__ = "job-search-card__location"
    time_cls__ = "job-search-card__listdate--new"
    time_cls2__ = "job-search-card__listdate"
#     link_cls__ = "base-search-card__info"
    link_cls__ = "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"
    base_card_cls__ = "base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card"
    
    
    
    def __init__(self,html):
        self.soup  = BeautifulSoup(html, 'lxml')
        
    def get_search_col(self):
        return self.soup.find_all(class_ = to_df.list_cls__)
    
    def get_cards(self):
        return self.soup.find_all(class_ = to_df.base_card_cls__)
    
    def get_roles(self,x):
#         expects HTML of list_cls__
#         return [i.text.strip() for i in self.soup.find_all(class_ = to_df.title_cls__)]
        return self.handle_empty(x.find(class_ = to_df.title_cls__)).text.strip()

    def get_companies(self,x):
#         return [i.text.strip() for i in self.soup.find_all(class_ = to_df.company_cls__)]
        return self.handle_empty(x.find(class_ = to_df.company_cls__)).text.strip()
    
    def get_locs(self,x):
#         return [i.text.strip() for i in self.soup.find_all(class_ = to_df.loc_cls__)]
        return self.handle_empty(x.find(class_ = to_df.loc_cls__)).text.strip()
    
    def get_time(self,x):
#         return [i.text.strip() for i in self.soup.find_all(class_ = [to_df.time_cls__, to_df.time_cls2__])]
        return self.handle_empty(x.find(class_ = [to_df.time_cls__, to_df.time_cls2__])).text.strip()
            
    def get_links(self,x):
#         return [i['href'] for i in self.soup.find_all(class_ = to_df.link_cls__, href=True)]
#         return [ i['href'] for i in conv.get_search_col()[0].find_all(class_ = to_df.base_card_cls__ , href = True) ]
#         return [ i['href'] for i in conv.get_search_col()[0].find_all(class_ = to_df.link_cls__ , href = True) ]
#         return self.handle_empty(x.find(class_ = to_df.link_cls__ , href = True)).text.strip()
#         return self.handle_empty(x.find(class_ = to_df.link_cls__ , href = True))
        tmp = x.find('a')
    
        if tmp is None:
#             return "NA"
            return np.nan
        
        else:
            
            return self.handle_empty(str(tmp['href']))
#         return self.handle_empty(x.find('a', href = True))
            
    def handle_empty(self, x):
        if x is None:
            return np.nan
#             return "NA"
        if x == "":
            return np.nan
#             return "NA"
        
        return x
#         return x if x != "" or x is not None else "NA"
    
    def process_cards(self):
        lis = []
        for i in self.get_cards():
#             print(i)
#             print("--------------"*5)
            lis.append([
                self.get_roles(i),
                self.get_companies(i),
                self.get_locs(i),
                self.get_time(i),
                self.get_links(i)
            ])
    
        return lis
        
    def get_df(self):
#         return pd.DataFrame({
#             'role': self.get_roles(),
#             'company': self.get_companies(),
#             'location': self.get_locs(),
#             'time': self.get_time(),
#             'link': self.get_links()
#         })
        return pd.DataFrame(self.process_cards(), columns = ['role', 'company', 'location', 'time', 'link'])


class scrape_exp:
#     regex__ = "(?:\d(?:^|\W){0,1}(?:to|-)(?:$|\W){0,1}\d[ ]{0,1}(?:years|Years|year|year|yrs|Yrs|yr|Yr){0,1}|(?:(?:\d\+|\d \+)|\d) (?:years|Years|year|year|yrs|Yrs|yr|Yr)|\d\+)"
#     regex__ = r"(?:(?:^|\W){0,1}(?:\bexperience\b)(?:$|\W)(?:\w+\s[:,\- ]*){0,5}((?:\d(?:^|\W){0,1}(?:to|-)(?:$|\W){0,1}\d[ ]{0,1}(?:years|Years|year|year|yrs|Yrs|yr|Yr){0,1}|(?:(?:\d\+|\d \+)|\d) (?:years|Years|year|year|yrs|Yrs|yr|Yr)|\d\+))|((?:\d(?:^|\W){0,1}(?:to|-)(?:$|\W){0,1}\d[ ]{0,1}(?:years|Years|year|year|yrs|Yrs|yr|Yr){0,1}|(?:(?:\d\+|\d \+)|\d) (?:years|Years|year|year|yrs|Yrs|yr|Yr)|\d\+))(?:\w+\s){0,5}(?:^|\W){0,1}(?:\bexperience\b)(?:$|\W))"
    regex__ =  r"(?:(?:^|\W){0,1}(?:\bexperience\b)(?:$|\W)(?:[\s]*)(?:\w+\s[:,\- ]*){0,5}(?:\d(?:^|\W){0,1}(?:to|-)(?:$|\W){0,1}\d[ ]{0,1}(?:years|Years|year|year|yrs|Yrs|yr|Yr){0,1}|(?:(?:\d\+|\d \+)|\d) (?:years|Years|year|year|yrs|Yrs|yr|Yr)|\d\+)|(?:\d(?:^|\W){0,1}(?:to|-)(?:$|\W){0,1}\d[ ]{0,1}(?:years|Years|year|year|yrs|Yrs|yr|Yr){0,1}|(?:(?:\d\+|\d \+)|\d) (?:years|Years|year|year|yrs|Yrs|yr|Yr)|\d\+)(?:\w+\s){0,5}(?:^|\W){0,1}(?:\bexperience\b)(?:$|\W))"
    re_spl_char__ = r"[,:;'\"/\?!\’]"
    text_class1__= "description__text description__text--rich"
    text_class2__ = "show-more-less-html__markup"
    base_delay__ = 4

    
    def __init__(self,df):
        self.df = df
        
    def pattern(self):
        return re.compile(scrape_exp.regex__, flags=re.IGNORECASE)
        
    def get_exp(self, URL):
        
#         headers = {
#             'Accept': '*/*',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Host': 'httpbin.org',
# #             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
#             'X-Amzn-Trace-Id': 'Root=1-63189379-0bc2656a09a19a4f29813a97',
#             "User-Agent":random.choice(user_agents).strip()
#             }
        headers = {
        "User-Agent":random.choice(user_agents).strip(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
        }
        
        r = requests.get(URL,
                         allow_redirects=True,
                         headers=headers
                        )
        
#         with open('file.html', 'w') as file:
#             file.write(r.text)

        soup = BeautifulSoup(r.content, 'lxml')
        text = self.text_with_newlines(soup.find(class_ = scrape_exp.text_class2__))
        
        text = re.sub(scrape_exp.re_spl_char__, "", text)
        
#         with open('file.text', 'w') as file:
#             file.write(text)

#         self.exp = self.handle_empty_list(list(set(re.findall(scrape_exp.regex__, string=text))))
#         print(self.exp)
        

        pattern = self.pattern()
        res = pattern.findall(text)
        
        # print(res)
        return ", ".join(res).strip()
        
        
#         res = list(set(itertools.chain(*res)))
#         try:
#             res.remove('')
#         except ValueError:
#             pass
        
#         self.exp = self.handle_empty_list(res)
        
#         self.exp = self.handle_list(self.exp)
        
#         return self.exp
    
        
    def text_with_newlines(self, elem):
        text = ''
        try:
            for e in elem.descendants:
                if isinstance(e, str):
                    text += e.strip()
                elif e.name == 'br' or e.name == 'p' or e.name == 'li' or e.name == 'ul':
                    text += '\n'
            return text
        except Exception as E:
            return text
        
        
    def handle_empty_list(self, lis):
        
        if len(lis) == 0:
            return ["NA"]
        else:
            return lis
        
    def handle_list(self, lis):
        return " ".join(lis).strip()
    
    def tmp(self, idx,row):
        time.sleep(scrape_exp.base_delay__+random.random())
        return [idx, self.get_exp(row["link"])]
#         return [kvp[0] , self.get_exp(kvp[1]["link"])]
    
    def apply(self):
        
        exp_lis = Parallel(n_jobs=-1)(delayed(self.tmp)(idx,row) for idx,row in self.df.iterrows())
        
#         return exp_lis
        
#         exp_lis = []
#         for idx, row in self.df.iterrows():
            
#             exp_lis.append([idx, self.get_exp(row["link"])])
#             time.sleep(scrape_exp.base_delay__+random.random())
#         return exp_lis
        
        exp_df = pd.DataFrame(exp_lis, columns=["idx","Experience"])
        
        return exp_df.set_index("idx")
        
       
URLs = {
        "DA":"https://www.linkedin.com/jobs/search/?f_E=1%2C2%2C3&f_TPR=r86400&geoId=102713980&keywords=data%20analyst&location=India",
        "DS":"https://www.linkedin.com/jobs/search/?f_E=1%2C2%2C3&f_TPR=r86400&geoId=102713980&keywords=data%20science&location=India",
        "BA":"https://www.linkedin.com/jobs/search/?f_E=1%2C2%2C3&f_TPR=r86400&geoId=102713980&keywords=business%20analyst&location=India",
        "FSD":"https://www.linkedin.com/jobs/search/?f_E=1%2C2%2C3&f_TPR=r86400&geoId=102713980&keywords=web%20developer&location=India",
        "PM":"https://www.linkedin.com/jobs/search/?f_E=1%2C2%2C3&f_TPR=r86400&geoId=102713980&keywords=product%20manager&location=India",
        "SD":"https://www.linkedin.com/jobs/search/?f_E=1%2C2%2C3&f_TPR=r86400&geoId=102713980&keywords=software%20developer&location=India",
    "HR Recruitment": "https://www.linkedin.com/jobs/search/?distance=25&f_E=3%2C4%2C6&f_JT=F&geoId=105214831&keywords=hr%20recruitment&location=Bengaluru%2C%20Karnataka%2C%20India"
        }
pages = 15
base_delay = 4







headers = {
        "User-Agent":random.choice(user_agents).strip(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
        }

def df_from_url(headers, domain, URL):


    r = requests.get(URL,
                     allow_redirects=True,
                     headers = headers
                    )
    
    conv = to_df(r.content)
    with open('file.html', 'w') as file:
        file.write(r.text)

    
    try:
        df = conv.get_df()
        df = df.assign(Domain = domain)
        
    except Exception as E:
        print(f"Something happned for {domain} {URL}")
        print(traceback.format_exc())
        return 
        
    return df
    



def data_for_domain(domain, Base_URL, pages, base_delay = base_delay):
    headers = {
        "User-Agent":random.choice(user_agents).strip(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
        }
    
    df = pd.DataFrame()
    for idx in range(pages):
        URL = Base_URL + f"&start={25*idx}"
        
        tmp_df = df_from_url(headers, domain, URL)
        
        if len(tmp_df) == 0:
            print(f"Done at page {idx+1}")
            break
        
        df = pd.concat([df,tmp_df], axis =0 , ignore_index=True)
        time.sleep(base_delay+random.random())
    
    
    df = df.drop_duplicates(subset=["role","company","location"]).reset_index(drop=True)

    return df.dropna()
            


print("Starting to scrape jobs...")

lis = Parallel(n_jobs = -1)(delayed(data_for_domain)(domain, URL, pages) for domain, URL in URLs.items())

print("Done Scraping jobs...")

df = pd.concat(lis, axis=0, ignore_index=True).reset_index(drop=True)
df = df.assign(scraped = scrape_time)


# print("Saving this data to csv file...")
# df.to_csv(f"linkedin_jobs_{scrape_time}_AllDomains.csv", index=False)
# print("Done.\n\n")


print("Scraping experience...")
scrape = scrape_exp(df)

df_scrape = scrape.apply()
print("Done..")


# print("Saving to csv file...")
# df.join(df_scrape).to_csv(f"linkedin_jobs_{scrape_time}_EXPERIENCE_AllDomains.csv", index=False)
# print("Done.")


print("Sending over mail")
send_email(['ams.mailer.1@gmail.com'],f'LinkedIn Scrape: {scrape_time}',df.join(df_scrape), f"linkedin_jobs_{scrape_time}_EXPERIENCE_AllDomains.csv")

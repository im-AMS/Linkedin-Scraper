import json
import logging as log
import random
from dataclasses import dataclass, field
from datetime import datetime
from pprint import pprint
from typing import List

import pandas as pd
import requests
from jsonpath_ng import parse


class Scrape_jobIds:
    """
    Created a seperate class which scrapes only the JobId.
    The intention behind it was to use a different API end point which contains
    even more information about each of the drive and can be accessed by passing jobId
    """

    def __init__(self, user_agent_file="./user-agents.txt"):
        log.basicConfig(
            format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
            level=log.INFO,
        )

        # Use random user agents on each request
        with open(user_agent_file, "r") as text_file:
            self.user_agents = text_file.readlines()

        self.headers = {
            "User-Agent": random.choice(self.user_agents).strip(),
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "appid": "109",
            "systemid": "109",
            "clientid": "d3skt0p",
            "gid": "LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        self.params = [
            ("noOfResults", "50"),
            ("urlType", "search_by_keyword"),
            ("searchType", "adv"),
            ("keyword", "data analyst"),
            ("sort", "f"),
            ("pageNo", "1"),
            ("experience", "0"),
            ("jobAge", "3"),
            ("k", "data analyst"),
            ("experience", "0"),
            ("jobAge", "3"),
            ("seoKey", "data-analyst-jobs"),
            ("src", "sortby"),
            ("latLong", ""),
        ]

    def _scrape(self):
        response = requests.get(
            "https://www.naukri.com/jobapi/v3/search",
            params=self.params,
            # cookies=cookies,
            headers=self.headers,
        )
        return (response, response.text)

    def get_jobId(self):
        # log.info("Scraping jobIds")
        resp_code, resp = self._scrape()
        # with open("api_data.json", "w") as f:
        #     f.write(resp)

        resp_dict = json.loads(resp)
        # resp_dot = dotdict(resp)
        print(resp_code)
        jobId_parser = parse("$.jobDetails[*].jobId")
        # num_jobs_parser = parse("$.noOfJobs")
        log.info(f"Returned code {resp_code}, returned { resp_dict['noOfJobs'] } jobs")
        return [match.value for match in jobId_parser.find(resp_dict)]
        # return [tmp["jobId"] for tmp in resp_dot.jobDetails]


@dataclass
class ParseJobDetails:
    """
    Created this for ease of use.
    Manually parsing each of these json data is extremely cumbersome and errorprone.
    Hence defined a data class which is modular and easy to debug and scalable.
    Also added the feature of automatically parsing json data which is passed as string. ParseJobDetails.from_json_string(json_string)
    It checks if path exists then it assignes the value else assiges None.
    """

    job_id: int = field(metadata={"jsonpath": "$.jobDetails.jobId"})
    company: str = field(metadata={"jsonpath": "$.jobDetails.companyDetail.name"})
    title: str = field(metadata={"jsonpath": "$.jobDetails.title"})
    url: str = field(metadata={"jsonpath": "$.jobDetails.staticUrl"})
    vacancy: int = field(default="", metadata={"jsonpath": "$.jobDetails.vacancy"})
    posted_on: datetime = field(
        default="", metadata={"jsonpath": "$.jobDetails.createdDate"}
    )
    total_applications: int = field(
        default="", metadata={"jsonpath": "$.jobDetails.applyCount"}
    )
    is_walkin: bool = field(default="", metadata={"jsonpath": "$.jobDetails.walkIn"})
    job_type: str = field(default="", metadata={"jsonpath": "$.jobDetails.jobType"})
    wfh_label: str = field(default="", metadata={"jsonpath": "$.jobDetails.wfhType"})
    locations: List[str] = field(
        default="", metadata={"jsonpath": "$.jobDetails.locations[*].label"}
    )
    preffered_skills: List[str] = field(
        default="", metadata={"jsonpath": "$.jobDetails.keySkills.preferred[*].label"}
    )
    other_skills: List[str] = field(
        default="", metadata={"jsonpath": "$.jobDetails.keySkills.other[*].label"}
    )
    min_salary: int = field(
        default="", metadata={"jsonpath": "$.jobDetails.salaryDetail.minimumSalary"}
    )
    max_salary: int = field(
        default="", metadata={"jsonpath": "$.jobDetails.salaryDetail.maximumSalary"}
    )
    ug_degree: List[str] = field(
        default="", metadata={"jsonpath": "$.jobDetails.education.ug"}
    )
    pg_degree: List[str] = field(
        default="", metadata={"jsonpath": "$.jobDetails.education.pg"}
    )
    ppg_degree: List[str] = field(
        default="", metadata={"jsonpath": "$.jobDetails.education.ppg"}
    )

    # enables use of json path filtering for each variable
    @classmethod
    def from_json_string(cls, json_data):
        json_dict = json.loads(json_data)
        variables = {}

        for field_name, field_meta in cls.__dataclass_fields__.items():
            field_path = field_meta.metadata.get("jsonpath")
            if field_path:
                jsonpath_expr = parse(field_path)
                matches = [match.value for match in jsonpath_expr.find(json_dict)]
                if len(matches) == 1:
                    variables[field_name] = matches[0]
                else:
                    variables[field_name] = matches or None

        return cls(**variables)

    def to_dict(self):
        return vars(self)


class Scrape_details:
    """
    A seperate class which gets all the data after passing jobId.
    We can either pass a single jobId or a list of jobId it returns the data appropreately.
    """

    def __init__(self, user_agent_file="./user-agents.txt") -> None:
        log.basicConfig(
            format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
            level=log.INFO,
        )

        self.parse_job_details = ParseJobDetails

        with open(user_agent_file, "r") as text_file:
            self.user_agents = text_file.readlines()

        self.headers = {
            "User-Agent": random.choice(self.user_agents).strip(),
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "AppId": "121",
            "SystemId": "Naukri",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "gid": "LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        self.params = {
            "src": "jobsearchDesk",
            "xp": "1",
            "px": "1",
            "microsite": "y",
        }

    def __scrape(self, jobId):
        response = requests.get(
            f"https://www.naukri.com/jobapi/v4/job/{jobId}",
            params=self.params,
            # cookies=cookies,
            headers=self.headers,
        )
        return (response, response.text)

    def __get_detail_from_single_jobId(self, jobId):
        log.info(f"Scraping details for {jobId}")
        resp_code, resp = self.__scrape(jobId)
        resp_dict = json.loads(resp)
        try:
            # resp_dot = dotdict(resp)
            # company_name_parser = parse("$.jobDetails.companyDetail.name")
            # print(resp_dict)
            log.info(
                f"Returned code {resp_code}, Title: {resp_dict['jobDetails']['title']} Company: {resp_dict['jobDetails']['companyDetail']['name']}\n"
            )
            return self.parse_job_details.from_json_string(resp).to_dict()
        except Exception as e:
            log.warning(e)
            # print(e)
            with open("log.json", "w") as f:
                f.write(resp)
            return

    def __get_detail_from_list_jobId(self, jobId_list):
        details = []
        [details.append(self.__get_detail_from_single_jobId(id)) for id in jobId_list]
        return details

    def get_details(self, jobId):
        if isinstance(jobId, str):
            log.info(f"running __get_detail_from_single_jobId")
            return self.__get_detail_from_single_jobId(jobId)
        elif isinstance(jobId, list):
            log.info(f"running __get_detail_from_list_jobId")
            return self.__get_detail_from_list_jobId(jobId)


# Set logging
log.basicConfig(
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    level=log.INFO,
)

# Create class instance and scrape get the list of jobIds
jobid_scraper = Scrape_jobIds()
jobids = jobid_scraper.get_jobId()
log.info(f"list of jobIds: {jobids}.\nGot {len(jobids)} jobids")

# Create class instance and scrape the job details for each jobIds
details_scraper = Scrape_details()
details_list = details_scraper.get_details(jobids)

# remove none values form list, some JobIds dont display on naukri portal,
# it gets redirected, hence the output will be None
details_list = list(filter(lambda value: value is not None, details_list))

# create a DataFrame with the details
df = pd.DataFrame(details_list)
log.debug(f"{df}")

# export data
df.to_csv("naukri.csv", index=False)
log.info(f"Done")

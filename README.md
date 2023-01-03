# LinkedIn Jobs Scraper with Experience

Scrapes job data and parses experience (if mentioned in description) from linkedIn from the provided URLs.

# How to use?

1. Install requirements
```
pip install -r requirements.txt
```
2. Create a file named `config.yaml`, refer to the `example_config.yaml`. Feel free to copy the same file and use it, make sure to **update your credentials**.
3. To create password credentials, go to [`https://myaccount.google.com/apppasswords`](https://myaccount.google.com/apppasswords) to **generate app password**. Make sure to use this password in the `config.yaml` file.
4. Run the file with
```
python jobs_with_exp_parallel.py
```

# Example Output

|role                |company                       |location                        |time        |link                                                                                                                                                                                                                                    |Domain|scraped            |Experience                                          |
|--------------------|------------------------------|--------------------------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|-------------------|----------------------------------------------------|
|Associate - Projects|Cognizant                     |Bengaluru, Karnataka, India     |15 hours ago|https://in.linkedin.com/jobs/view/associate-projects-at-cognizant-3271094252?refId=N7I0SU%2Bi7Qb2BsvD4tqSlg%3D%3D&trackingId=uKBPSqvEJ2eeaiM2e5ZY1g%3D%3D&position=1&pageNum=0&trk=public_jobs_jserp-result_search-card                 |DA    |12-12-2022_10:31:28|                                                    |
|Python Developer    |Monsoon CreditTech            |Greater Delhi Area              |16 hours ago|https://in.linkedin.com/jobs/view/python-developer-at-monsoon-credittech-3391986098?refId=N7I0SU%2Bi7Qb2BsvD4tqSlg%3D%3D&trackingId=pN9KZts%2Bi%2BLC1rhpo1M2hQ%3D%3D&position=2&pageNum=0&trk=public_jobs_jserp-result_search-card      |DA    |12-12-2022_10:31:28|                                                    |
|IT Cloud Engineer   |Clariant                      |Mumbai Metropolitan Region      |8 hours ago |https://in.linkedin.com/jobs/view/it-cloud-engineer-at-clariant-3396747776?refId=N7I0SU%2Bi7Qb2BsvD4tqSlg%3D%3D&trackingId=41LOO0o0sMPQTxUF8JHkug%3D%3D&position=3&pageNum=0&trk=public_jobs_jserp-result_search-card                   |DA    |12-12-2022_10:31:28|                                                    |
|Data Modeler        |Thermo Fisher Scientific India|Bengaluru East, Karnataka, India|19 hours ago|https://in.linkedin.com/jobs/view/data-modeler-at-thermo-fisher-scientific-india-3396498540?refId=N7I0SU%2Bi7Qb2BsvD4tqSlg%3D%3D&trackingId=eSkktgn0zIlt%2FHc8g4jAqg%3D%3D&position=4&pageNum=0&trk=public_jobs_jserp-result_search-card|DA    |12-12-2022_10:31:28|6+ years working experience , 2+ years of Experience|


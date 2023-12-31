# Job Search via LinkedIn with Web Scraping!
Effortlessly harness the capabilities of this Selenium web scraping application to efficiently sift through a large volume of LinkedIn job listings, tailored to your specific job criteria.

***Benefits***

- Even with LinkedIn's robust filters, job searching can be a time-consuming process, spanning hours or even days to uncover a substantial number of opportunities. However, with this application, you can achieve the same results in a matter of minutes.

- This web scraping tool eliminates the need for redundancy in your job search results. Moreover, it is worth noting that LinkedIn's salary filter is capped at $200,000. Therefore, if you are seeking positions with higher compensation, you can leverage this scraper to ensure that you exclusively receive job listings that meet your minimum acceptable salary criteria.

- Leveraging the ChatGPT OpenAI API and employing artificial intelligence/machine learning capabilities, specifically the GPT-3 language model, to ascertain the duration of required experience specified in the job description.

- This application has been enhanced with a novel feature feature designed to streamline job filtering, allowing users to identify job postings that offer the ability to communicate with the hiring team. ***Please be advised that the utilization of this feature (message hiring team) necessitates a premium LinkedIn Subscription to career or business.***

All job listings will be saved to  "*.json" files 


## Tech Used
- Python
    - dotenv
- Selenium
- webdriver-manager
    - chromedriver
- ChatGPT (OpenAI API)
    - AI/ML (GPT-3) LLM
- JSON
<!-- - lxml
- requests
- BeautifulSoup -->



## Setup, Install & 

1. `pip3 install -r requirements.txt`
2. `mv env.example .env`
3. Setup .env
    - This software has been developed with the purpose of facilitating access to your LinkedIn account. I encountered a challenge in attempting to access salary range information without the necessity of logging in. It's worth noting that job listings can be viewed without the need for authentication. However, to effectively utilize this software, logging in is a requisite step.
    ```
    LinkedIn_USER_NAME=username
    LinkedIn_PASSWORD=password  
    ```
    - Set your minimum acceptiable pay e.g. ($250,000.00 >>> 250) 
    `MINIMUM_ACCEPTABLE_PAY=250K`
    - find & copy the path where you saved chromedriver
    `CHROME_DRIVER_PATH=/some/path/to/chromedriver`
    - To initiate your job search on LinkedIn, please follow the standard procedure of accessing the platform through your web browser. Once you have commenced your job search and applied the appropriate filters, kindly copy and paste the dynamic URL generated by LinkedIn, which encapsulates your specific job search criteria. ***Please take note that LinkedIn employs dynamic URLs to store all your filter criteria. Therefore, you can simply copy and paste this URL into the .env file.***
    `URL="<Please copy and paste the dynamic URL from LinkedIn that includes your pertinent job search filters>"`
    - ***Please note that the URL must be enclosed in double quotes.***
    - Set up ChatGPT API key; [Find your key here](https://platform.openai.com/api-keys)
    `CHATGPT_API_KEY=<Please copy and paste your ChatGPT API key here>`


## Run

1. You will have to manually make the "jobs.txt" as it is ignored by git.
2. `python3 app.py`
3. You might encounter a CAPTCHA prompt, in which case, kindly complete it. The code includes a 20-second timer to provide you with ample time to fulfill this requirement.
4. All outcomes will be appended to the "jobs.txt" file in JSON format.


## NOTES

- If you introduce new requirements, please regenerate the "requirements.txt" file.
    - `pip3 freeze > requirements.txt` 
    - If you are not utilizing a virtual environment, it will include all items, including those from other projects. ***Make sure to only add what is needed.*** 

- #### `*.json` & `*.txt` files are ignored by git.


## IMG

***Site + Res***

![Image of the terminal just before entering the command to run the scraper](https://raw.githubusercontent.com/LWRGitHub/job-search-scraping-linkedin/main/job-search-scraping-img.png)

"""
This script scrapes the University of Pisa's website to extract information about the courses offered by the university.

Author: Amir Sarrafzadeh Arasi
Date: 2024/11/04

The script is divided into the following functions:
1. fetch_data: Fetches the HTML content of a given URL.
2. parse_data: Parses the HTML content using BeautifulSoup.
3. process_department: Processes the department page to extract department data.
4. process_course: Processes the course page to extract course data.
5. main: The main function that orchestrates the scraping process.

The script first fetches the main page of the university's website to extract the department IDs and names.
It then iterates over each department to fetch the courses offered by the department.
For each course, it extracts the course data such as code, language, CFU, period, and academic year.

The extracted data is stored in a Pandas DataFrame and saved to a CSV file.

The script uses logging to log information and errors during the scraping process.
"""

# Import necessary libraries
import re
import json
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Set up logging with more informative formatting
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s -  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Define the function to fetch data from a given URL
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        logging.info(f"Successfully fetched data from {url}")
        return response.content
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error while fetching data from {url}: {str(e)}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception occurred while fetching data from {url}: {str(e)}")
    return None


# Define the function to parse the HTML content using BeautifulSoup
def parse_data(html_content):
    if html_content:
        try:
            return BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            logging.error(f"Error parsing HTML content: {str(e)}")
    return None


# Define the function to process the department page
def process_department(url, parameters):
    department_data = {}
    logging.info(f"Processing department: {url}")
    html_content = fetch_data(url)
    soup = parse_data(html_content)
    if soup:
        select_element = soup.find("select", id=f"{parameters["course"]}")
        if select_element:
            temp_list = []
            for option_element in select_element.find_all("option"):
                value = option_element.get("value")
                name = option_element.text.strip()
                if name:
                    temp_list.append((value, name))
            department_data = temp_list
            logging.info(f"Department processed successfully: {url}")
    return department_data


# Define the function to process the course page
def process_course(url):
    course_data = []
    logging.info(f"Processing course: {url}")
    html_content = fetch_data(url)
    soup = parse_data(html_content)
    if soup:
        links = soup.find_all('a', href=re.compile(r'programma.php'))
        for link in links:
            query_string = link.get('href')
            temp_url = f'https://esami.unipi.it/{query_string}'
            second_html_content = fetch_data(temp_url)
            second_soup = parse_data(second_html_content)
            if second_soup:
                codice_value = second_soup.find_all('span', class_='value-programma')[2].text.strip()
                lingua_value = second_soup.find_all('span', class_='value-programma')[5].text.strip()
                cfu_value = second_soup.find_all('span', class_='value-programma')[3].text.strip()
                periodo_value = second_soup.find_all('span', class_='value-programma')[4].text.strip()
                anno_value = second_soup.find_all('span', class_='value-programma')[0].text.strip()
                course_data.append([codice_value, lingua_value, cfu_value, periodo_value, anno_value])
        logging.info(f"Course processed successfully: {url}")
    return course_data


# Define the main function to orchestrate the scraping process
def main():
    try:
        # Load parameters from JSON file
        with open('parameters.json', 'r') as f:
            parameters = json.load(f)
        logging.info("Parameters loaded successfully")
    except Exception as e:
        logging.error(f"Error loading parameters from JSON file: {str(e)}")
        return
    try:
        # Fetch the main page and parse the HTML content
        html_content = fetch_data(parameters["main_page_url"])
        soup = parse_data(html_content)
        logging.info("Main page processed successfully")
        department_dict = {}
        if soup:
            select_element = soup.find("select", id=f"{parameters["department"]}")
            if select_element:
                for option_element in select_element.find_all("option"):
                    value = option_element.get("value")
                    name = option_element.text.strip()
                    if name:
                        department_dict[value] = name

        courses_names = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            for key, value in department_dict.items():
                second_url = f'{parameters["main_page_url"]}did={key}'
                courses_names[value] = executor.submit(process_department, second_url, parameters)

        final_output = {}
        counter = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            for key1, value1 in department_dict.items():
                courses = courses_names[value1].result()
                for key2, value2 in courses:
                    third_url = f'{parameters["main_page_url"]}did={key1}&cid={key2}'
                    course_data = executor.submit(process_course, third_url).result()
                    for data in course_data:
                        counter += 1
                        final_output[f"course_{counter}"] = [value1, value2] + data
        logging.info("All courses processed successfully")
        df = pd.DataFrame(final_output)
        df = df.transpose()
        df.columns = parameters["columns"]
        df.to_csv(parameters["csv_file"], index=False)
        logging.info(f"Data saved to CSV file: {parameters['csv_file']}")
    except Exception as e:
        logging.error(f"An error occurred during the scraping process: {str(e)}")


if __name__ == "__main__":
    main()

# University of Pisa Course Scraper

This Python script is designed to scrape the University of Pisa's website and extract information about the courses offered by the university. The extracted data includes details such as course code, language, CFU (Crediti Formativi Universitari), period, and academic year.

## Table of Contents
1. [Introduction](#introduction)
2. [Author](#author)
3. [Functions](#functions)
4. [Usage](#usage)
5. [Dependencies](#dependencies)
6. [License](#license)

## Introduction <a name="introduction"></a>

The University of Pisa Course Scraper is a tool that automates the process of gathering information about the courses available at the University of Pisa. It accesses the university's website, navigates through its pages, and extracts relevant data from the HTML content. The extracted data is then processed and stored in a CSV file for further analysis or use.

## Author <a name="author"></a>

This script was authored by Amir Sarrafzadeh Arasi. The author's email address is not provided.

## Functions <a name="functions"></a>

The script is divided into several functions, each responsible for a specific task:

1. **fetch_data**: Fetches the HTML content of a given URL using the `requests` library.
2. **parse_data**: Parses the HTML content using BeautifulSoup to extract relevant information.
3. **process_department**: Processes the department page to extract department data.
4. **process_course**: Processes the course page to extract course data.
5. **main**: The main function that orchestrates the scraping process by calling other functions.

## Usage <a name="usage"></a>

To use the University of Pisa Course Scraper, follow these steps:

1. Make sure you have Python installed on your system.
2. Install the required dependencies listed in the [Dependencies](#dependencies) section.
3. Modify the `parameters.json` file to customize the scraping parameters if necessary.
4. Run the script by executing the command `python scraper.py` in your terminal.

## Dependencies <a name="dependencies"></a>

The script requires the following dependencies:

- `requests`
- `beautifulsoup4`
- `pandas`

You can install these dependencies using pip:
```
pip install requests beautifulsoup4 pandas
```

## License <a name="license"></a>

The University of Pisa Course Scraper is provided under the [MIT License](LICENSE). You are free to modify and distribute the script as long as you include the original license and attribution to the author.




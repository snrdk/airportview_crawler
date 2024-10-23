# Airport Review website Crawler w/ Docker  
This repository contains a web scraping tool to collect articles from the _**International Airport Review**_ website using Python and BeautifulSoup, packaged in a Docker container for easy deployment. This is simple crawler code. 

## Contents
- `Dockerfile`: Contains the setup for building the Docker image.
- `airportview.py`: The main Python script for crawling articles from the website.
- `airportview.sh`: A shell script to build the Docker image and run the container for multiple URLs.
- `requirements.txt`: Python dependencies required for the project.


## Prerequisites  
Before running the project, make sure you have [Docker](https://www.docker.com/) installed on your system.

## Build the Docker image
```bash
docker build -t airport_crawler .
```

This command will create a Docker image named `airport_crawler` based on the `Dockerfile` provided.  

## Run the Docker container  
To start the crawler and save the data into a CSV file, use the provided shell script `airportview.sh`. This script will run the crawler for multiple URLs:  
```bash
./airportview.sh
```
The shell script will loop through a list of topics (e.g., "airside-operations", "passenger-experience", etc.) and run the crawler for each of these topics. The results will be saved as CSV files in the `data` directory.

## Data collection process
he script crawls articles related to specific topics from the International Airport Review website. The topics can be modified by changing the argument provided when running the Docker container or modifying the `airportview.sh file`. The script collects all articles published in the past year and saves the data into a CSV file.

## Files:
* Dockerfile: Defines the Docker environment setup.
* airportview.py: Python script that performs the crawling.
* airportview.sh: Shell script to run the crawler for multiple topics.
* requirements.txt: Lists Python dependencies such as beautifulsoup4, requests, and python-dateutil.

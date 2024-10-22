import time
import csv
import argparse
import os
import sys
from datetime import datetime, timedelta
import re
from dateutil import parser
sys.path.append('/lge')
from utils import *

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--save_format", type=str, choices=["csv", "mysql"], default="csv")
    parser.add_argument("-u", "--url", type=str, required=True)
    args = parser.parse_args()
    
    return args

def main(args):
    ''' 0. Webpage URL for crawling '''
    base_url = 'https://www.internationalairportreview.com/core_topic/'
    page='/?fwp_paged=1'
    url = f"{base_url}{args.url}{page}"

    
    
    ''' 1. Parsing to bs4 object after HTTP GET request using func in utils.py '''
    soup = Load_soup(url)
    
    
    ''' 2. Get the date 1 year ago using func in utils.py '''
    year_ago_date = Get_Date_from_a_Year_ago()
    
    ## Formatting according to the Upload date format for each site !!!
    #ex) Aug 16, 2022
    date_format = "%d %B %Y"
    year_ago_date = year_ago_date.strftime(date_format)
    year_ago_datetime = datetime.strptime(year_ago_date, date_format)
    
    
    ''' 3. Collect 1 year worth of article urls '''
    article_urls = []
    
    
    next_page=1
    while True:
        ''' Site-Specific article url collection code ... '''
        ## 3-0. Get article url in the current main page
         
        for i in range(2, 17):
            selector = f'#fullLeft > main > div.facetwp-template > article:nth-child({i}) > div.articleExcerpt > h3 > a'
            element = soup.select_one(selector)
            if element:
                href_value = element['href']
                article_urls.append(href_value)
            else:
                print("href_value {i} not found")
            
            
        ## 3-1. Find the crawled_date, the upload date of the last crawled article
            try:
#                print(i)
#                crawled_date_with_director = soup.select_one(f'#fullLeft > main > div.facetwp-template > article:nth-child({i}) > div.articleExcerpt > p.meta').get_text()
               cleaned_text = soup.select_one(f'#fullLeft > main > div.facetwp-template > article:nth-child({i}) > div.articleExcerpt > p.meta').get_text()
            except:
#                cleaned_text = soup.select_one(f'#fullLeft > main > div.facetwp-template > article:nth-child({i}) > div.articleExcerpt > p:nth-child(3) > span').get_text()
                
                cleaned_text = soup.select_one(f'#fullLeft > main > div.facetwp-template > article:nth-child({i}) > div.articleExcerpt > p:nth-child(3) > span').get_text()
                
#            index = crawled_date_with_director.find('|')
#            if index != -1:
#                cleaned_text = crawled_date_with_director[:index-1]
            cleaned_text = re.search(r'(\d{1,2} \w+ \d{4})', cleaned_text)
            if cleaned_text:
                cleaned_text = cleaned_text.group(1)
            print(cleaned_text)
            crawled_datetime = datetime.strptime(cleaned_text, date_format)

            
        time.sleep(2)
        ## 3-2. Compare last crawled_date with year_ago_date
        if crawled_datetime <= year_ago_datetime: break
        else:
           ## Get next page
           last_number = int(url.split('=')[-1])
           incremented_number = last_number + 1
           url = url.rsplit('=', 1)[0] + '=' + str(incremented_number)
           print(url)
           soup = Load_soup(url)
    

    ''' 4. Crawl the content of each article '''
    for article in article_urls:
        time.sleep(2)
        soup = Load_soup(article)
        
        vertical = 'Transport'
        sub_vertical = args.url
        format = 'News/Article/Podcast' # News/Expertise/Video
        
        title = soup.select_one(f'#fullLeft > main > article > h1').get_text()
        print(title)
        container = soup.select_one('#fullLeft > main > article')
        if container:
            content_p = [p.get_text() for p in container.find_all(['p','ul','h'])]
            combined_text = ' '.join(content_p)
            
            
        content = combined_text
        print(content)
        print()
        
        try:
            element = soup.select_one(f'#metaInfo > div.dateTime > div > p')
            if element:
                upload_date = element.get_text()
            else:
                raise ValueError("Element not found")
        except:
            element = soup.select_one(f'#inpage > div.date > p')
            if element:
                upload_date = element.get_text()
            else:
                element = soup.select_one(f'#metaInfo > div.dateTime > div')
                if element:
                    upload_date = element.get_text()
                else:
                    upload_date = "Date not found"

        # upload_date = parser.parse(upload_date).strftime('%d %B %Y')
        print(upload_date)
        
        ''' 5. Save Data '''
        if args.save_format == "csv":
            writer.writerow([vertical, sub_vertical, format, title, content, upload_date, article, ''])
            
        elif args.save_format == "mysql":
            Save_to_MySQL(vertical, sub_vertical, format, title, content, upload_date, article, '')
    
    print(f"\n Data saved successfully in {args.save_format}")


if __name__ == '__main__':
    args = parse_arg()
    
    # If you want to save the data to csv file ,
    if args.save_format == "csv":
        csv_path = "./data/"
        os.makedirs(csv_path, exist_ok=True)
        csv_save_path = f'{csv_path}/{args.url}.csv'
        f = open(csv_save_path, "w", encoding="utf-8", newline="")
        writer = csv.writer(f)
        writer.writerow(["Vertical", "Sub_Vertical", "Format", "Title", "Content", "Upload_Date", "URL", "Video"])
        
    main(args)
    
    if args.save_format == "csv": f.close()
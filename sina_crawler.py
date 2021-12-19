#coding=utf-8
from functions import *
from email_infor import *
import requests
import time
import random
import os.path


# add header for the crawler
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

# Add in your search list!
search_list = ["所罗门群岛"]

# Create url encoded search list based on the word list you have gaven
urlencoded_search_list = url_encoding(search_list)
urls = create_url_list(urlencoded_search_list)

# loop for none stop run
day_count = 0
while 1:
    # you can personalize your own report email here
    # send an email to you when everyday's mission start
    start_title = "Program start!"
    start_report = str(datetime.now())

    # define folder path
    yesterday_folder = "../WBTestdata/" + yesterday()
    today_folder = "C:/Users/daumi/PycharmProjects/keyword_based_Sina_weibo_crawler/WBTestdata/" + today()

    print(os.path.dirname(os.path.realpath(__file__)))
    # Testify if today's folder exist, if not, create
    if not os.path.exists(today_folder):
        print( "Today's first run! Create new folder.")
        os.mkdir(today_folder)

    # start mission, set 0, print out mission information: start time, date of today, how many days this program has run
    word_count = 0
    total_page_count = 0
    today_start_time = datetime.now()

    # loop for every word in the list
    for country in range(len(search_list)):
        word_count += 1
        this_baseurl = urls[country]  # create base url: without page number
        print(this_baseurl)
        initial_page_number = 1  # define start page
        str_initial_page_number = str(initial_page_number)
        exception_count = 0  # exception count
        end_date = days_ago(365)  # Determine the date of when to end, format [03-30]

        # loop for adding page number and requesting them in succession
        # The date below all follow format [04-02], check function.py for more information
        for i in range(initial_page_number, initial_page_number + 3000):  # Let's say, no more than 3000 pages per word
            this_page_number = str(i)

            # Last line 3D key search phrase change that to one of your search phrases
            this_url = "https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D英雄联"  # generate current url with current page number
            print('HELLO')
            # Get and write down JSON data into txt file with structured file name
            try:
                req = requests.get(this_url, headers=headers, timeout=4)
                content = req.content
                # This situation happens when today's mission did not finished on time before 24:00
                # So there is not folder exist for today's file path: this_file_path
                # Need to create the folder first
                # f = open(today_folder, "w")
                # f.write(content)
                print(content)
                print( "total page count: ", total_page_count)
                total_page_count += 1

                # Get this page's end time to determine to continue to next page or to next word
                try:
                    this_end_time = get_this_endtime_text(content)

                # This situation happens when the server changed the JSON structure,
                # if happens, please check the JSON data and change the retrieve structure accordingly
                except Exception as e:
                    print(e)
                    break

                if end_date > this_end_time:
                    print( "current endtime: ", this_end_time)
                    print( "We reached 2 days ago's data! Now sleep a while and call for next country!")
                    break
                else:
                    print( "current page's endtime: ", this_end_time)
                    print( "Not enough! Sleep a while and continue requesting for next page!")
                    time.sleep(random.randint(2, 8))
            finally:
                print('tse')
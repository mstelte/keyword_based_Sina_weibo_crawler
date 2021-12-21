import datetime
from weibo_crawler import crawl_weibo

start_date = datetime.datetime(2021, 9, 1, 0, 0, 0, 0, datetime.timezone(datetime.timedelta()))
end_date = datetime.datetime(2021, 12, 18, 23, 59, 59, 59, datetime.timezone(datetime.timedelta()))

searches = []
searches.append(["#英雄联盟##EDG#", "edg_lol_worlds"])
searches.append(["#斯德哥尔摩major#", "stockholm_csgo_major"])
searches.append(["#dota2国际邀请赛#", "dota2_international"])
searches.append(["#2020欧洲杯#", "euro2020"])
searches.append(["#环法自行车赛#", "tour_de_france_2021"])
searches.append(["#NBA总决赛#", "nba_final"])

for search in searches:
    crawl_weibo(search[0], start_date, end_date, search[1])
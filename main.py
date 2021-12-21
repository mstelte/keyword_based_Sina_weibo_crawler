import datetime
from weibo_crawler import crawl_weibo

start_date = datetime.datetime(2021, 9, 1, 0, 0, 0, 0, datetime.timezone(datetime.timedelta()))
end_date = datetime.datetime(2021, 12, 18, 23, 59, 59, 59, datetime.timezone(datetime.timedelta()))

searches = []
searches.append(["#PGC2021#", "PGC2021"])
searches.append(["#斯德哥尔摩major#", "PGLMAJOR"])
searches.append(["#2021英雄联盟全球总决赛#", "Worlds2021"])
searches.append(["#短池世锦赛#", "FINAAbuDhabi2021"])
searches.append(["#2021MLB世界大赛#", "WorldSeries"])
searches.append(["#F1阿布扎比大奖赛#", "AbuDhabiGP"])

for search in searches:
    crawl_weibo(search[0], start_date, end_date, search[1])
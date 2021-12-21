from genericpath import exists
import requests
import os
import datetime
import json

def crawl_weibo(keyword: str, start_date: datetime, end_data: datetime, file_name: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    url = "https://m.weibo.cn/api/container/getIndex?"
    
    cur_page = 0
    data_retrieved = True

    while data_retrieved:
        cur_page += 1

        #https://m.weibo.cn/api/container/getIndex?containerid=

        data = {
            'containerid': f'100103type%3D1%26q%3D{format_keyword_for_url(keyword)}',
            'page_type':' searchall',
            'page': cur_page,
        }
        html = requests.get(url, headers=headers, params=data)

        if html.content:
            response = html.json()
            cards = response["data"]["cards"]
            if str(cards) != "[]":
                try:
                    for card in unpack_nested_cards(cards, data["containerid"], cur_page):
                        creation_time = parse_creation_time_of_card(card["mblog"]["created_at"])
                        if creation_time >= start_date and creation_time <= end_data:
                            with open(f"{os.path.dirname(os.path.realpath(__file__))}/data/{file_name}.txt", "a", encoding="utf-8") as file:
                                file.write(str(card))
                except Exception as e:
                    print(e)
            else:
                data_retrieved = False

def format_keyword_for_url(keyword: str) -> str:
    return keyword.replace("#", "%23")

def unpack_nested_cards(retrieved_cards: any, container_id: str, cur_page: int) -> set[any]:
    types = [3, 6, 7, 9, 10, 11, 17, 24, 25, 30, 42, 59, 89, 143, 145, 156]

    cards = []
    card_ids = set()

    for retrieved_card in retrieved_cards:

        #https://github.com/ArchiveLife/weibo/blob/e893f270d3ce/api/list.go#L69

        json_card = json.loads(json.dumps(retrieved_card))

        if json_card.get("mblog"):
            card_id = retrieved_card["mblog"]["id"]
            if card_id not in card_ids:
                cards.append(retrieved_card)
                card_ids.add(card_id)

        if json_card.get("card_group"):
            for card in unpack_nested_cards(retrieved_card["card_group"], container_id, cur_page):
                card_id = card["mblog"]["id"]
                if card_id not in card_ids:
                    cards.append(card)
                    card_ids.add(card_id)

        if json_card.get("left_element"):
            card_id = retrieved_card["left_element"]["mblog"]["id"]
            if card_id not in card_ids:
                cards.append(retrieved_card["left_element"])
                card_ids.add(card_id)

        if json_card.get("right_element"):
            card_id = retrieved_card["right_element"]["mblog"]["id"]
            if card_id not in card_ids:
                cards.append(retrieved_card["right_element"])
                card_ids.add(card_id)
                
        if retrieved_card["card_type"] not in types:
            print(f"Unknown card_type {retrieved_card['card_type']} found in container {container_id} on page {cur_page}")

    return cards

def parse_creation_time_of_card(creation_time: str) -> datetime:
    (weekday, month, day, time, timezone, year) = creation_time.split(" ")
    (hour, minute, second) = time.split(":")
    if timezone[0:1] == "+":
        actual_timezone = datetime.timezone(datetime.timedelta(hours = int(timezone[1:]) / 100))
    elif timezone[0:1] == "-":
        actual_timezone = datetime.timezone(datetime.timedelta(hours = int(timezone[1:]) / -100))
    actual_creation_time = datetime.datetime(int(year), parse_month_to_int(month), int(day), int(hour), int(minute), int(second), 0, actual_timezone)

    return actual_creation_time

def parse_month_to_int(month: str) -> int:
    if month == 'Jan':
        return 1
    if month == 'Feb':
        return 2
    if month == 'Mar':
        return 3
    if month == 'Apr':
        return 4
    if month == 'May':
        return 5
    if month == 'Jun':
        return 6
    if month == 'Jul':
        return 7
    if month == 'Aug':
        return 8
    if month == 'Sep':
        return 9
    if month == 'Oct':
        return 10
    if month == 'Nov':
        return 11
    if month == 'Dec':
        return 12
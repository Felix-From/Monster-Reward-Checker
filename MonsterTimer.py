import requests
from bs4 import BeautifulSoup as bs
from time import sleep

discord_webhook_url = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
discord_userID_mention = "xxxxxxxxxxxxxxxxxxxx"

telegram_token = "xxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
telegram_chat_id = "xxxxxxxxxxxxx"

url = "https://www.monsterenergyclawclub.de/public-rewards-1/"

# Yes, prob. would a sql db or a json file be better to edit the checklist on the go
# but it works and thats what i needed.
list_of_Items_to_look = ["cargo-kuhler",
                         "hjc-rpha-full-face-all-black-helm-grosse-l",
                         "hjc-rpha-full-face-all-black-helm-grosse-m",
                         "gaming-rucksacke",
                         "monster-turnbeutel",
                         "monster-energy-dx-racer-v3-gaming-stuhl",
                         "monster-energy-logo-handtuch",
                         "2024-skateboard-drip-2",
                         "skateboard-2024",
                         "kaffeetasse-1"
                         ]

repeats_till_stop_alert = [3 for i in range(len(list_of_Items_to_look))]

#Start Msg to check if it has started :D
telegram_msg_first = "MonsterBot wurde gestartet."
telegram_url_first = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={telegram_msg_first}"
requests.get(telegram_url_first)


while True:
    # Request URL and get HTML content.
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    # Parse HTML content.
    # Select first "a" box with the href "/reward/cargo-kuhler"
    for index, item in enumerate(list_of_Items_to_look):    
        reward = soup.find('a', href="/reward/"+item)
        # Check if reward is available
        if reward != None:
            #print(f"{item} found... "+str(repeats_till_stop_alert[index]))

            # Check if "img" box is available with the class "out-of-stock"
            img = reward.find('img', class_="out-of-stock")
            if img == None:
                
                # Discord
                data = {
                    "content" : list_of_Items_to_look[index]+" ist da <@"+discord_userID_mention+">",
                    "username" : "Monster Bot",
                    "avatar_url" : "https://www.monsterenergy.com/img/home/monster-logo.png"
                }
                result = requests.post(discord_webhook_url,json=data)

                # Telegram
                telegram_msg = list_of_Items_to_look[index]+" ist da!"
                telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={telegram_msg}"
                requests.get(telegram_url)

                # Count down and Remove if 3 messages was send
                repeats_till_stop_alert[index] -= 1
                if repeats_till_stop_alert[index] == 0:
                    list_of_Items_to_look.pop(index)
                    repeats_till_stop_alert.pop(index)
    # Timeout 5 min... 
    sleep(300)
    pass
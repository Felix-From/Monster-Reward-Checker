import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import mysql.connector
import json
import time

## CONST
# MYSQL
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PSSWRD = ''
DB_NAME = 'MonsterChecker'

## Functions

def DiscordAliveMsg():
    global discord_webhook_url,discord_userID_mentions,currentTime,time_to_sleep,time_for_is_alive,list_of_Items_to_look,already_found_items
    # time_of_bot  = Current Timestamp , time_of_next_msg = (TIME_FOR_IS_ALIVE - currentTime)*TIME_TO_SLEEP, calced_time_next_msg = Current Timestamp + time_of_next_msg
    time_of_bot = time.strftime('%d.%m.%Y - %H:%M:%S', time.localtime(time.time()))
    calced_time_next_msg = time.time() + ((time_for_is_alive - currentTime)*time_to_sleep)
    calced_time_next_msg = time.strftime('%d.%m.%Y - %H:%M:%S', time.localtime(calced_time_next_msg))
    mentions =str(["<@"+discord_userID_mention+">" for discord_userID_mention in discord_userID_mentions])
    mentions = mentions.replace("[","").replace("]","").replace("'","")
    #print(mentions)
    #print(discord_userID_mentions)
    return json.dumps({
                "username": "MonsterChecker Infos",
                "avatar_url": "https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcR80LfVzZDx3VO1R6oK05rZuZyBVP2N692ufGoWgLnz6vs043BspMdn-y40xSEowA1d",
                "embeds": [
                    {
                    "title": "MonsterChecker | Alive ",
                    "fields": [
                        {
                        "name": "Uhrzeit vom Bot:",
                        "value": f"```\n{time_of_bot}\n```",
                        "inline": True
                        },
                        {
                        "name": "Zeitpunkt nächster AktivCheck",
                        "value": f"```\n{calced_time_next_msg}\n```",
                        "inline": True
                        },
                        {
                        "name": "Looking for Items:",
                        "value": f"```\n{list_of_Items_to_look}\n```"
                        },
                        {
                        "name": "Already Found:",
                        "value": f"```\n{already_found_items}\n```"
                        },
                        {
                        "name": "Mentions",
                        "value": mentions
                        }
                    ],
                    "image": {
                        "url": "https://i.pinimg.com/736x/4d/e9/fc/4de9fc6b5a6ce2138c70c6b11888b79c.jpg"
                    },
                    "color": "2749696",
                    "footer": {
                        "text": "MonsterChecker"
                    }
                    }
                ]
            })

def getCurrentSettings():
    global discord_webhook_url,discord_userID_mentions,telegram_token,telegram_chats_id,telegram_owner_id,list_of_Items_to_look,already_found_items,repeats_till_stop_alert,time_for_is_alive,time_to_sleep
    connection = mysql.connector.connect(
                host=DB_HOST,       # e.g., "localhost"
                user=DB_USER,   # e.g., "root"
                password=DB_PSSWRD,
                database=DB_NAME # e.g., "test_db"
            )

    cursor = connection.cursor()

    query = "SELECT * FROM Settings"  # Replace with your table name

    cursor.execute(query)

    results = cursor.fetchall()

    for row in results:
        discord_webhook_url = row[1]
        discord_userID_mentions = row[2].split(",")
        telegram_token = row[3]
        telegram_chats_id = row[4].split(",")
        telegram_owner_id = row[5]
        new_list_of_Items_to_look = row[6].split(",")
        time_for_is_alive = row[7]
        time_to_sleep = row[8]
        #print(discord_webhook_url,discord_userID_mention,telegram_token,telegram_chats_id,telegram_owner_id,list_of_Items_to_look)
    
    #Check if any of the array items match item from already_found_items, if so then remove it from new_list_of_Items
    for index, item in enumerate(new_list_of_Items_to_look):
        if item in already_found_items:
            new_list_of_Items_to_look.pop(index)

    if (len(new_list_of_Items_to_look)>len(repeats_till_stop_alert)):
        for i in range(len(new_list_of_Items_to_look)-len(repeats_till_stop_alert)):
            repeats_till_stop_alert.append(3)
    list_of_Items_to_look = new_list_of_Items_to_look
    
    cursor.close()
    connection.close()

def main():
    global discord_webhook_url,discord_userID_mentions,telegram_token,telegram_chats_id,telegram_owner_id,list_of_Items_to_look,already_found_items,repeats_till_stop_alert,time_for_is_alive,time_to_sleep,currentTime
    # Request URL and get HTML content.
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    # Select all "a" box with the href "/reward/cargo-kuhler"
    for index, item in enumerate(list_of_Items_to_look):    
        reward = soup.find('a', href="/reward/"+item)
        # Check if reward is available
        if reward != None:
            #print(f"{item} found... "+str(repeats_till_stop_alert[index]))
            # Check if "img" box is available with the class "out-of-stock"
            img = reward.find('img', class_="out-of-stock")
            if img == None:
                # MSG

                # Discord
                mentions =str(["<@"+discord_userID_mention+">" for discord_userID_mention in discord_userID_mentions])
                mentions = mentions.replace("[","").replace("]","").replace("'","")
                data = {
                    "content" : list_of_Items_to_look[index]+" ist da "+mentions,
                    "username" : "Monster Bot",
                    "avatar_url" : "https://www.monsterenergy.com/img/home/monster-logo.png"
                }
                result = requests.post(discord_webhook_url,json=data)
                #print("Discord MSG",data)

                # Telegram
                for chatid in telegram_chats_id:
                    telegram_msg = list_of_Items_to_look[index]+" ist da!"
                    telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={telegram_msg}"
                    requests.get(telegram_url)
                    #print("telegram Msg",telegram_msg)

                # Count down and Remove if 3 messages was send
                repeats_till_stop_alert[index] -= 1
                if repeats_till_stop_alert[index] == 0:
                    #print("Repeat Pop! ", list_of_Items_to_look[index])
                    already_found_items.append(list_of_Items_to_look[index])
                    list_of_Items_to_look.pop(index)
                    repeats_till_stop_alert.pop(index)


    currentTime += 1
    if currentTime >= time_for_is_alive:
        #Setting Sync
        getCurrentSettings()
            
        #Close IF

        currentTime = 0
        # Discord
        header = {
            'Content-Type': 'application/json'
        }
        result = requests.post(discord_webhook_url,headers=header,data=DiscordAliveMsg())
        print("Discord ALIVE")
        #print(result)

        # Telegram
        for chatid in telegram_chats_id:
            telegram_msg3 = "Alive Check!"
            telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={telegram_msg3}"
            requests.get(telegram_url)
        print("Telegram ALIVE")

    # Timeout time_for_is_alive Sec.
    sleep(time_to_sleep)


#Define Vars

#                   Time if time_to_sleep is set to 300 = 5 min
#                   time for alive check
#                   #5 = 25min        (5 * 12)= 1h    
time_for_is_alive = (5 * 12)*4

time_to_sleep = 300 #Sekunden

currentTime = time_for_is_alive # cirremtTime = time_for_is_alive = Live Check on Start, if set to 0, first check is after first period (time_for_is_alive)

discord_webhook_url = ""

discord_userID_mentions = []

telegram_token = ""

telegram_chats_id = []

telegram_owner_id = ""

url = "https://www.monsterenergyclawclub.de/public-rewards-1/"

list_of_Items_to_look = []

repeats_till_stop_alert = []

already_found_items = []

#
# Load Config from Database.
#

getCurrentSettings()

# Message to 'Owner' that the Bot Started.
telegram_msg_first = "MonsterBot wurde gestartet."
telegram_url_first = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_owner_id}&text={telegram_msg_first}"
requests.get(telegram_url_first)

print("Started")
while True:
    if len(list_of_Items_to_look) != 0:
        main()
    else:
        break
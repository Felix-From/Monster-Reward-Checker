import requests
from bs4 import BeautifulSoup as bs
from time import sleep

webhook_url = "xxxxxxxxxxxxxxxxxx"
url = "https://www.monsterenergyclawclub.de/public-rewards-1/"


while True:
    # Request URL and get HTML content.
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    # Parse HTML content.
    # Select first "a" box with the href "/reward/cargo-kuhler"
    reward = soup.find('a', href="/reward/lanyard")
    # Check if reward is available
    if reward != None:
        print("Kuhler found...")
        # Check if "img" box is available with the class "out-of-stock"
        img = reward.find('img', class_="out-of-stock")
        if img == None:
            data = {
                "content" : "Monster Kühler IST da <@xxxxxxxxxxxxxxxxx>",
                "username" : "Monster Bot",
                "avatar_url" : "https://www.monsterenergy.com/img/home/monster-logo.png"
            }
            result = requests.post(webhook_url,json=data)
            print("DER KÜHLER IST DAA!!")
        else:
            print("Out of Stock!")
    sleep(300)
    pass
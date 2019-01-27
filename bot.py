#!/usr/bin/python
import os
import schedule
import time
import unittest
import smtplib
import nexmo
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sms_msg = "YOUR MESSAGE TO BE SENT IN SMS"
search_text = "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous."
key_value = 'YOUR_KEY_VALUE'
secret_value = 'YOUR_SECRET_VALUE'
#targeted URL
scrapped_url = "http://www.val-doise.gouv.fr/booking/create/13860"

def scrap_page( url ):
    driver = webdriver.Chrome()
    driver.get( url )
    elmt = driver.find_element_by_id( "condition" )
    get_button = driver.find_element_by_name( "nextButton" )
    elmt.click()
    get_button.click()
    time.sleep(2)
    html_source = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return html_source.get_text()

# Check availability
# Return true or false
def check_availability():
    html_source = scrap_page( scrapped_url )
    return search_text in html_source

# SMS notification
def notify_sms( msg ):
    client = nexmo.Client( key= key_value, secret= secret_value )
    client.send_message({
                        'from': 'PrefBot',
                        'to': 'ENTER YOUR PHONE NUMBER',
                        'text': msg,
                        })

# Email notification
# If you want in couple with the sms notification
def notify_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("YOUR_EMAIL_ADRESS", "YOUR_PASSWORD")
    server.sendmail("SENDER_EMAIL", "RECEIVER_EMAIL", "Availabity yes")
    server.quit()

def send_availability():
    availability = check_availability()
    if availability == 0:
        notify_sms( sms_msg )
        notify_email()

# Run this script every 10 min
schedule.every(10).minutes.do(send_availability)

while True:
    schedule.run_pending()
    time.sleep(1)


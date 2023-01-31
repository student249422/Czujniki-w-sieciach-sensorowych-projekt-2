#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import hashlib
import csv
import datetime
import requests
import subprocess

flag = 0
user_name = "admin"
admin_password_hashed = "5f4dcc3b5aa765d61d8327deb882cf99"
tries = 0
while flag != 1:
    login = raw_input("Wprowadz login: ")
    if login == user_name:
        password = raw_input("Wprowadz haslo: ")
        md5_pass = hashlib.md5(password).hexdigest()
        if md5_pass == admin_password_hashed:
            print("Zalogowano")
            flag = 1
    if flag==0:
        print("Zle dane logowania")
        tries+=1
    if tries>=3:
        print("Dostep zabroniony, zbyt duzo prob")
        break
        
a = 1000
if flag==1:
    for i in range(a):        
        try:
            GPIO.setmode(GPIO.BOARD)

            PIN_TRIGGER = 7
            PIN_ECHO = 11

            GPIO.setup(PIN_TRIGGER, GPIO.OUT)
            GPIO.setup(PIN_ECHO, GPIO.IN)

            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            print("Calculating distance")

            GPIO.output(PIN_TRIGGER, GPIO.HIGH)

            time.sleep(0.00001)

            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO)==0:
                  pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO)==1:
                  pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            today = str(datetime.datetime.now()) #dzisiejsza data zmapowana na typ string
            #api_url = "https://api.thingspeak.com/update?api_key=7186JUHA2IWE2M8U&field1="+str(distance) #tutaj utworzony link z dopisanym wynikiem pomiaru
            #response = requests.get(api_url) #wyslanie linku z naszym pomiarem do thingspeak za pomoca metody GET z HTTP (rest API, w response zapisze sie odpowiedz API)
            result = [today, distance] #tutaj jest stworzona tablica z data pomiaru i jego wartoscia
            with open('data_200cm.txt', mode='a') as f: #otworzenie pliku .csv
                writer = csv.writer(f) #tworzy sie obiekt zapisujacy dane do pliku
                # write the header
                writer.writerow(result) #zapisanie danych spod zmiennej result do pliku

            print("Distance:",distance,"cm")
            
            if (distance<15.0):
                subprocess.Popen(["aplay","/home/pi/lenarcik-kaminski/alert2.wav"])
                time.sleep(0.3)
            if (distance<25.0 and distance>=15.0):
                subprocess.Popen(["aplay","/home/pi/lenarcik-kaminski/alert2.wav"])
                time.sleep(0.6)
            if (distance<50.0 and distance>=25.0):
                subprocess.Popen(["aplay","/home/pi/lenarcik-kaminski/alert2.wav"])
                time.sleep(1)

        finally:
              GPIO.cleanup()
        #if (i<a-1):
            #time.sleep(16)


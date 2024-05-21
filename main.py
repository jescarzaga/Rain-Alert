import os
import requests
import smtplib
from dotenv import find_dotenv, load_dotenv

api_key = "b00b01c13ffbc0b29a62d72840dc7692"
MY_LAT = 32.735687
MY_LON = -97.108063

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

email = os.getenv("email")
password = os.getenv("password")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "cnt": 4,
    "appid": api_key,
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()


condition_code = [int(hour_data["weather"][0]["id"]) for hour_data in weather_data["list"]]

will_rain = False
for code in condition_code:
    if code < 700:
        will_rain = True

if will_rain:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg="Subject:Rain Alert\n\nIt's gonna rain today so make sure to wear a hoodie!"
        )

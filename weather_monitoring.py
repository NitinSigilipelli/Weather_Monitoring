import requests
import time
import schedule
import smtplib
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
from pymongo import MongoClient
# Configurations
API_KEY = '70919af569b86efccf8694f3570161d5'
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
INTERVAL = 1 # minutes
THRESHOLD_TEMP = 35  # Celsius
#ALERT_EMAIL = 'nitinchakravarthy369@google.com'
MONGO_URI = 'mongodb://localhost:27017/' 

weather_data = defaultdict(list)
daily_summaries = defaultdict(list)  

# Setup MongoDB connection
client = MongoClient(MONGO_URI)
db = client['weather_db']
daily_summaries_collection = db['daily_summaries'] 


def send_email_alert(city, temp):
    """ Sends email alert when temperature exceeds threshold """
    subject = f"Weather Alert for {city}"
    message = f"Temperature Alert: {temp}°C in {city}. Stay safe!"
    print(f"Alert: {message}")
    # You can uncomment below to enable actual email sending
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login('sigilipellinitin@gmail.com', 'geql fnpb zrdg grym')
    # body = f"Subject: {subject}\n\n{message}"
    # server.sendmail('sigilipellinitin@gmail.com', ALERT_EMAIL, body)
    # server.quit()


def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

def fetch_weather_data():
    """ Fetches weather data for the cities and process rollups """
    global weather_data
    
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get("main"):
            temp = kelvin_to_celsius(data["main"]["temp"])
            feels_like = kelvin_to_celsius(data["main"]["feels_like"])
            weather_condition = data["weather"][0]["main"]
            timestamp = data["dt"]

            weather_data[city].append({
                "temp": temp,
                "feels_like": feels_like,
                "weather_condition": weather_condition,
                "timestamp": timestamp
            })

            print(f"Fetched weather data for {city}: {temp}°C, {weather_condition} feels like {feels_like}")

            # Check threshold for alert
            if temp > THRESHOLD_TEMP:
                send_email_alert(city, temp)

def aggregate_daily_data():
    """ Generates daily rollups for average, max, min temperature and dominant weather """
    global weather_data, daily_summaries
    
    for city, data in weather_data.items():
        if data:
            avg_temp = round(sum(d['temp'] for d in data) / len(data), 2)
            max_temp = max(d['temp'] for d in data)
            min_temp = min(d['temp'] for d in data)

            weather_conditions = [d['weather_condition'] for d in data]
            dominant_weather = max(set(weather_conditions), key=weather_conditions.count)

            daily_summary = {
                "city": city,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "avg_temp": avg_temp,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "dominant_weather": dominant_weather
            }

            daily_summaries[city].append(daily_summary)

            # Store daily summary in MongoDB
            daily_summaries_collection.insert_one(daily_summary)
            print(f"Daily Summary for {city}:")
            print(f"Average Temp: {avg_temp}°C, Max Temp: {max_temp}°C, Min Temp: {min_temp}°C, Dominant Weather: {dominant_weather}")
            visualize_weather_data(city)
        # Clear the day's data after processing
        weather_data[city] = []

def visualize_weather_data(city):
    """ Visualize daily summaries for a given city """
    if city not in daily_summaries or not daily_summaries[city]:
        print(f"No data available for {city} to visualize.")
        return

    # Prepare data for plotting
    dates = [d['date'] for d in daily_summaries[city]]
    avg_temps = [d['avg_temp'] for d in daily_summaries[city]]
    max_temps = [d['max_temp'] for d in daily_summaries[city]]
    min_temps = [d['min_temp'] for d in daily_summaries[city]]

    # Plotting the temperature trends
    plt.figure(figsize=(10, 5))
    plt.plot(dates, avg_temps, label='Avg Temp (°C)', marker='o')
    plt.plot(dates, max_temps, label='Max Temp (°C)', marker='x')
    plt.plot(dates, min_temps, label='Min Temp (°C)', marker='^')

    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f"Weather Trends for {city}")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def setup_scheduling():
    """ Sets up periodic data fetching and daily aggregation """
    # Fetch weather data every INTERVAL minutes
    schedule.every(INTERVAL).minutes.do(fetch_weather_data)

    # Aggregate daily data at midnight
    schedule.every().day.at("00:00").do(aggregate_daily_data)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("Server Started Wait for ",INTERVAL," Mintues to get the results")
    try:
        setup_scheduling()
    finally:
        client.close() 

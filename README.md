# Weather Monitoring System

## Description
This project is a Python-based weather monitoring system that fetches real-time weather data for multiple cities, alerts users via email when temperatures exceed a specified threshold, and aggregates daily weather data for visualization. It uses the OpenWeatherMap API to gather weather data and stores daily summaries in a MongoDB database.

## Features
- Fetches real-time weather data for multiple cities.
- Sends email alerts when temperatures exceed a defined threshold.
- Aggregates daily weather data for average, max, and min temperatures.
- Visualizes weather trends using Matplotlib.
- Stores daily summaries in MongoDB.

## Technologies Used
- Python
- OpenWeatherMap API
- MongoDB
- Matplotlib
- schedule for periodic tasks

## Prerequisites
- Python 3.x
- MongoDB
- An OpenWeatherMap API key

## Installation

### 1. Clone the Repository
git clone https://github.com/NitinSigilipelli/Weather_Monitoring.git

### 2. Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### 3. Install Required Packages
pip install requests matplotlib schedule pymongo

### 4. Configure the Project
Open the main script and update the following configurations:
- API_KEY: Your OpenWeatherMap API key.
- ALERT_EMAIL: The email address to receive alerts.
- MONGO_URI: MongoDB connection string.

## Usage
To start the weather monitoring system, run the main script:
python main.py

The script will fetch weather data at regular intervals and aggregate daily summaries at midnight.

## Visualizations
Visualizations of daily weather trends for each city will be generated and displayed using Matplotlib.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or enhancements.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Author
Nitin Sigilipelli

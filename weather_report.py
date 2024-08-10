import pandas as pd
import requests
import numpy as np
import boto3
from io import StringIO
import os

api_key = 'Replace with your API key'
base_url = 'http://api.openweathermap.org/data/2.5/weather'

df = pd.read_csv('worldcities.csv')

country_counts = df['country'].value_counts() >= 100
c = country_counts[country_counts == True].index

df = df[df['country'].isin(c)]
df = df.groupby('country').head(6)

def fetch_weather(city, lat, lng):
    params = {
        'lat': lat,
        'lon': lng,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'weather' in data or 'sys' in data:
            return {
                'city': city,
                'temperature': data['main']['temp'],
                'weather': data['weather'][0]['description'],
                'lat' : data['coord']['lat'],
                'lng' : data['coord']['lon'],
                'temp_min' : data['main']['temp_min'],
                'temp_max' : data['main']['temp_max'],
                'sea_level' : data['main']['sea_level'],
                'humidity' : data['main']['humidity'],
                'current_time' : data['dt'],
                'sunrise' : data['sys']['sunrise'],
                'sunset' : data['sys']['sunset'],
                'timezone' : data['timezone']
            }
        else:
            print(f"Missing 'main' or 'weather' in response for city: {city}")
            return {'city': city, 'temperature': None, 'weather': None}
    else:
        print(f"Failed to fetch weather data for city: {city}, status code: {response.status_code}")
        return {'city': city, 'temperature': None, 'weather': None}

# Fetch weather data for each city
weather_data = []
for index, row in df.iterrows():
    weather = fetch_weather(row['city'], row['lat'], row['lng'])
    weather_data.append(weather)

weather_df = pd.DataFrame(weather_data)

cities_df = df[['city_ascii', 'lat', 'lng', 'admin_name','capital', 'population','country']]
new = pd.merge(cities_df, weather_df, on = ['lat', 'lng'], how = 'inner')

# transforming data 

new.rename(columns = {'city_ascii' : 'city'}, inplace= True)
new['admin_name'].fillna('Unknown', inplace = True)
new['capital'].fillna('Unknown', inplace = True)

new['current_time'] = pd.to_datetime(new['current_time'], unit = 's')
new['sunrise'] = pd.to_datetime(new['sunrise'], unit = 's')
new['sunset'] = pd.to_datetime(new['sunset'], unit = 's')
new['day_length'] = np.ceil((new['sunset'] - new['sunrise']).dt.total_seconds() /3600)
new['Hot-cities'] = np.where(new['temperature'] > 30 , 'Y', 'N')

country_stats = new.groupby('country').agg({
    'temperature': 'mean',
    'population': 'sum',
    'humidity': 'mean'
}).reset_index()
country_stats['Country_AVG_popul_temp_humi'] = (country_stats['population'].astype(int).astype(str)) + ',' +round(country_stats['temperature'],2).astype(str) +','+ round(country_stats['humidity'],2).astype(str)

country_stats = country_stats[['country','Country_AVG_popul_temp_humi']]
final = pd.merge(new,country_stats, on='country', how = 'inner')


# loading data to S3 bucket

os.environ['AWS_ACCESS_KEY_ID'] = 'Your AWS_ACCESS_KEY_ID'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'Your AWS_SECRET_ACCESS_KEY'
csv_buffer = StringIO()
final.to_csv(csv_buffer, index= False)
s3 = boto3.client('s3', region_name= 'us-east-1')
bucket_name = 'bucket-for-etl'
file_name = 'weather_report.csv'
s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())


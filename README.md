# Weather Report Script

## Cities dataset is from: https://simplemaps.com/data/world-cities

## Overview

This Python script, `weather_report.py`, is part of an ETL (Extract, Transform, Load) project designed to extract weather data from an API and combine it with a world cities dataset. The goal is to get the latest weather information for a selection of cities. Due to the limitations of the free trial version of the OpenWeather API, the dataset has been reduced to approximately 600 rows. The final data is stored in a CSV format in an AWS S3 bucket.

## Features

- **Data Extraction**: Fetches current weather data from the OpenWeather API for a selection of cities.
- **Data Transformation**: Merges weather data with a world cities dataset to provide comprehensive weather information.
- **Data Loading**: Stores the final transformed data into an AWS S3 bucket in CSV format.
- **API Rate Limiting**: Handles API rate limiting by reducing the dataset size to ~600 cities due to the number of hits allowed per day in the free OpenWeather API plan.

## Prerequisites

Before running the script, ensure you have the following:

- **Python 3.x**: The script is written in Python, so you'll need to have Python installed on your machine.
- **OpenWeather API Key**: Obtain an API key from [OpenWeather](https://openweathermap.org/api) and replace the placeholder in the script.
- **AWS Credentials**: Ensure you have access to an AWS S3 bucket and proper credentials set up to store the final CSV file.
- **Required Libraries**: The script may require certain Python libraries (e.g., `requests`, `boto3`, `pandas`). Install them using `pip`:
  ```bash
  pip install requests boto3 pandas
  ```

## Usage

1. **Clone the Repository**: If this script is part of a GitHub repository, clone it to your local machine.
   ```bash
   git clone https://github.com/yourusername/repositoryname.git
   ```
2. **Navigate to the Directory**: Move into the directory where the script is located.
   ```bash
   cd repositoryname
   ```
3. **Edit the Script**: Open the script and update it with your API key, AWS credentials, and any other configurations if required.
   ```python
   API_KEY = 'your_openweather_api_key_here'
   AWS_ACCESS_KEY = 'your_aws_access_key_here'
   AWS_SECRET_KEY = 'your_aws_secret_key_here'
   S3_BUCKET_NAME = 'your_s3_bucket_name_here'
   ```
4. **Run the Script**: Execute the script using Python.
   ```bash
   python weather_report.py
   ```
5. **View the Output**: The script will fetch the weather data, merge it with the world cities dataset, and store the result in an S3 bucket as a CSV file.

## Example

Here’s an example of how to use the script:

```bash
python weather_report.py
```

Expected output:
- Weather data will be merged with city information.
- The final data will be uploaded to the specified S3 bucket as `weather_data.csv`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

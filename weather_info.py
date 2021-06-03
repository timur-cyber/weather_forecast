import datetime
import requests
from bs4 import BeautifulSoup


class WeatherMaker:
    def __init__(self, time_from, time_to):
        self.start = datetime.datetime.strptime(time_from, '%d-%m-%Y')
        self.end = datetime.datetime.strptime(time_to, '%d-%m-%Y')
        self.weather_forecast = []
        self.date_list = []

    def get_forecast(self):
        while self.end > self.start:
            self.start = datetime.datetime(self.start.year, self.start.month, self.start.day) + datetime.timedelta(
                days=1)
            self.date_list.append(self.start)

        for date in self.date_list:
            source = f'https://darksky.net/details/57.908,59.9711/{date.year}-{date.month}-{date.day}/ca12/en'
            response = requests.get(source)
            html_doc = BeautifulSoup(response.text, features='html.parser')
            weather_value = html_doc.find('p', {'id': 'summary'})
            list_of_values = html_doc.find_all('span', {'class': 'temp'})
            temperature = list_of_values[0].text
            value = weather_value.text if weather_value.text != '' else 'Unknown'
            if u'\xa0' in value:
                value = value.replace(u'\xa0', u' ')
            self.weather_forecast.append(
                {'date': date, 'temperature': temperature, 'weather': value}
            )

        return self.weather_forecast

    def write(self, stat):
        for line in stat:
            date_date = datetime.datetime.strftime(line['date'], '%d-%m-%Y')
            date = date_date
            temperature = line['temperature']
            weather = line['weather']
            print(f'Date: {date}. Temperature: {temperature}. Weather: {weather}')

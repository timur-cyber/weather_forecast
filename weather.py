import argparse
import datetime
from weather_info import WeatherMaker
from image_maker import ImageMaker
from db_maker import DatabaseUpdater


class Manager:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def make_images(self):
        image = ImageMaker(self.forecast_stat)
        image.get_image()

    def update_base(self):
        db = DatabaseUpdater()
        db.update_base(self.forecast_stat)

    def get_info_from_base(self):
        db_getter = DatabaseUpdater()
        stat = db_getter.get_stat_from_db(self.start, self.end)
        for info in stat:
            date = datetime.datetime.strftime(info["date"], '%d-%m-%Y')
            print(f'Date: {date}. Temperature: {info["temperature"]}. Weather: {info["weather"]}')

    def run(self):
        try:
            weather = WeatherMaker(self.start, self.end)
            self.forecast_stat = weather.get_forecast()
            self.make_images()
            self.update_base()
            self.get_info_from_base()
        except ValueError:
            print('Неверный формат. Пожалуйста введите корректный формат. (ДД-ММ-ГГ)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Инструмент манипуляций с прогнозом погоды.')
    parser.add_argument('date_from', type=str, help='Начальная дата')
    parser.add_argument('date_to', type=str, help='Конечная дата')
    args = parser.parse_args()

    manager = Manager(args.date_from, args.date_to)
    manager.run()

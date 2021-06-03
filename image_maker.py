import datetime
import os
from collections import defaultdict
import cv2


class ImageMaker:
    def __init__(self, stat_dict):
        self.YELLOW_COLOR = (17, 221, 240)
        self.BLUE_COLOR = (54, 3, 0)
        self.LIGHT_BLUE_COLOR = (189, 170, 2)
        self.GREY_COLOR = (20, 20, 20)
        self.WHITE_COLOR = (255, 255, 255)
        self.color = None
        self.stat_dict = stat_dict
        self.weather_image = None

    def analyze(self, elem):
        weather_total = defaultdict(int)
        weather_total[elem['weather']] += 1
        total_list = list(weather_total.items())
        total_list.sort(key=lambda x: x[1], reverse=True)
        element = total_list[0]
        if 'snow' in element[0].lower():
            self.color = self.LIGHT_BLUE_COLOR
            self.weather_image = 'python_snippets\\external_data\\weather_img\\snow.jpg'
        elif 'cloud' in element[0].lower() or 'overcast' in element[0].lower() or 'foggy' in element[0].lower():
            self.color = self.GREY_COLOR
            self.weather_image = 'python_snippets\\external_data\\weather_img\\cloud.jpg'
        elif 'clear' in element[0].lower():
            self.color = self.YELLOW_COLOR
            self.weather_image = 'python_snippets\\external_data\\weather_img\\sun.jpg'
        elif 'rain' in element[0].lower():
            self.color = self.BLUE_COLOR
            self.weather_image = 'python_snippets\\external_data\\weather_img\\rain.jpg'
        elif 'unknown' == element[0].lower():
            self.color = self.WHITE_COLOR
            self.weather_image = None
        else:
            self.color = self.GREY_COLOR
            self.weather_image = 'python_snippets\\external_data\\weather_img\\sun.jpg'

    def make_gradient(self, image):
        b = self.color[0]
        g = self.color[1]
        r = self.color[2]
        for i in range(1, 300):
            b += 1
            g += 1
            r += 1
            if r > 255:  # Или можно использовать тернарный оператор. В одну строку =)
                r = 255
            if b > 255:
                b = 255
            if g > 255:
                g = 255
            image[i - 1:i, :] = (b, g, r)

    def write_text(self, image, elem):
        date = datetime.datetime.strftime(elem['date'], '%d-%m-%Y')
        weather = elem['weather']
        temp = elem['temperature'][:-1]
        cv2.putText(image, date, (10, 25), 3, 1, (0, 0, 0))
        cv2.putText(image, weather, (50, 130), 1, 1.5, (0, 0, 0))
        cv2.putText(image, f'Temperature: {temp}', (60, 180), 5, 1.5, (0, 0, 0))

        if self.weather_image:
            weather_img = cv2.imread(self.weather_image)
            image[:100, 412:512] = weather_img[:100, :]

    def get_image(self):
        path = os.path.normpath('python_snippets/external_data/probe.jpg')
        for elem in self.stat_dict:
            image = cv2.imread(path)
            self.analyze(elem)
            self.make_gradient(image)
            self.write_text(image, elem)
            self.save_image(elem['date'], image)

    def save_image(self, date, image):
        os.makedirs('images', exist_ok=True)
        date_str = f'{date.day}-{date.month}-{date.year}'
        path = os.path.normpath(f'images/{date_str}.jpg')
        cv2.imwrite(path, image)

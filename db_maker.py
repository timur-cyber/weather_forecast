import peewee
import datetime


class BaseTable(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase('weather_data.db')


class Updater(BaseTable):
    date = peewee.DateTimeField()
    temperature = peewee.CharField()
    weather = peewee.CharField()


class DatabaseUpdater:
    def __init__(self):
        self.connection = peewee.SqliteDatabase('weather_data.db')
        self.connection.create_tables([Updater])

    def update_base(self, stat):
        for elem in stat:
            date = elem['date']
            temperature = elem['temperature']
            weather = elem['weather']
            try:
                Updater.get(Updater.date == date)
            except Exception:
                Updater.create(
                    date=date,
                    temperature=temperature,
                    weather=weather,
                )

    def get_stat_from_db(self, time_from, time_to):
        start = datetime.datetime.strptime(time_from, '%d-%m-%Y')
        end = datetime.datetime.strptime(time_to, '%d-%m-%Y')
        db_stat = []

        result = Updater.select().where(Updater.date.between(start, end))

        for line in result:
            dict_to_list = {'date': line.date, 'temperature': line.temperature, 'weather': line.weather}
            db_stat.append(dict_to_list)

        return db_stat

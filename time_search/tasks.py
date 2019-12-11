import datetime
import itertools
from time import sleep

from background_task import background
from django.utils.timezone import make_aware

from .models import Guide
from .scraping import *
from .views import BUS_STOPS


#@background(schedule=60)
def get_scraping_data():
    now = datetime.datetime.now()

    for stops in itertools.product(BUS_STOPS, BUS_STOPS):
        if stops[0] == stops[1]:
            continue
        url = get_url(now.hour, now.minute, stops[0],stops[1])
        df = get_data(url)
        d = df.T.to_dict()

        for _d in d.values():
            collect_time = datetime.datetime.strptime(_d['collect_time'], '%Y-%m-%d %H:%M:%S')
            collect_time = make_aware(collect_time)

            departure_time = collect_time.strftime('%Y-%m-%d {0}:{1}:00'.format(*_d['発時刻'].split(':')))
            departure_time = datetime.datetime.strptime(departure_time, '%Y-%m-%d %H:%M:%S')
            departure_time = make_aware(departure_time)

            print('collect_time: ', collect_time, collect_time.tzinfo)
            print('departure_time: ', departure_time, departure_time.tzinfo)

            g = Guide(collect_time=collect_time,
                      departure_place=_d['departure_place'],
                      departure_time=departure_time,
                      arrival_place=_d['arrival_place'],
                      line_id=_d['行先番号'],
                      destination=_d['行き先'],
                      delay_time=_d['delay_time'])

            g.save()


if __name__ == '__main__':

    while True:
        get_scraping_data()
        sleep(60)

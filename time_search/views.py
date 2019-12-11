import datetime
import pytz

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils.timezone import make_aware

from .models import Guide
from .scraping import *


BUS_STOPS = ['名鉄岐阜（神田町通り）',
             'ＪＲ岐阜',
             'メディアコスモス・鶯谷高校口',
             '岐阜大学',
             '岐阜大学病院']


"""
METHOD
"""
def get_delayed_time(dep_t, delay_t):
    dep_t = dep_t.strftime('%Y-%m-%d %H:%M:00')
    dep_t = datetime.datetime.strptime(dep_t, '%Y-%m-%d %H:%M:%S')
    dep_t = dep_t + datetime.timedelta(hours=9)
    delay_t = dep_t + datetime.timedelta(minutes=delay_t)

    return dep_t.strftime('%H:%M'), delay_t.strftime('%H:%M')


"""
class
"""

class IndexView(generic.TemplateView):
    template_name = 'time_search/index.html'

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)

        context['bus_stops'] = BUS_STOPS

        return context

class GuideLineView(generic.TemplateView):
    template_name = 'time_search/guideline.html'

class AnalysisView(generic.TemplateView):
    template_name = 'time_search/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['xlabels'] = [i for i in range(5, 25)]
        context['label'] = '毎時間ごとの遅延時間の平均'
        context['data'] = [i for i in range(20)]

        return context

class SearchResultView(generic.ListView):
    model = Guide
    paginate_by = 10
    #context_object_name = 'guides'
    template_name = 'time_search/search_result.html'

    def get_context_data(self, **kwargs):

        is_debug = False

        context = super().get_context_data(**kwargs)
        data = []
        now = datetime.datetime.now()

        dep_stop_name = self.request.GET['dep_stop_name']
        arr_stop_name = self.request.GET['arr_stop_name']

        if not is_debug:

            url = get_url(now.hour, now.minute, dep_stop_name, arr_stop_name)
            print(url)
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

            guides = Guide.objects.filter(departure_time__date=datetime.date(now.year, now.month, now.day),
                                          departure_time__time__range=(datetime.time(now.hour, now.minute), datetime.time(23, 59)),
                                          departure_place=dep_stop_name, arrival_place=arr_stop_name,
                                          collect_time=collect_time
                                          ).distinct()
        else:
            guides = Guide.objects.filter(departure_place=dep_stop_name, arrival_place=arr_stop_name)

        for g in guides:
            dep_t, dep_delay_t = get_delayed_time(g.departure_time, g.delay_time)
            dic = {'dep_t': dep_t, 'dep_delay_t': dep_delay_t,
                   'delay_t': g.delay_time,
                   'line_id': g.line_id,
                   'destination': g.destination}
            data.append(dic)

        data = sorted(data, key=lambda d: d['dep_delay_t'])

        keys = []
        _data = []
        for d in data:
            s = d['dep_t'] + d['line_id']
            keys.append(s)
            l = len(keys)
            keys = list(set(keys))
            if len(keys) == l:
                _data.append(d)


        context['guides'] = _data

        context['now'] = now.strftime('%Y/%m/%d %H:%M:%S')

        context['dep_stop_name'] = dep_stop_name
        context['arr_stop_name'] = arr_stop_name

        try:
            context['collect_time'] = guides[0].collect_time
        except:
            context['collect_time'] = collect_time

        return context

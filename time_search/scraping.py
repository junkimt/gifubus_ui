"""
scraping.py
"""

import os.path as osp
import re
from time import sleep
import datetime
import pytz
import pandas as pd

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

"""
METHOD
"""

def get_collect_time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def convert_ja_url(url):
    p = urlparse(url)
    query = urllib.parse.quote_plus(p.query, safe='=&')
    url = '{}://{}{}{}{}{}{}{}{}'.format(
        p.scheme, p.netloc, p.path,
        ';' if p.params else '', p.params,
        '?' if p.query else '', query,
        '#' if p.fragment else '', p.fragment)
    return url

def get_delay_time(s):
    try:
        r = re.search('[0-9]+分', s)
        s = s[r.span()[0]:r.span()[1]]
        s = s.replace('分', '')
        return int(s)
    except:
        return 0

def get_guide_data(soup):
    data = []

    idx = 1
    id_str = 'ctl00_ContentPlaceHolder1_Usc_RouteG{}_UpdtPnl_Route'

    while True:
        dic = {}
        _id_str = id_str.format(idx)

        _soup = soup.find_all('div', id=_id_str)
        if len(_soup) == 0:
            break

        _soup = _soup[0]
        selector_head_str = 'ctl00_ContentPlaceHolder1_Usc_RouteG{}_Usc_RouteDetailInfoFal_Lbl_'
        for sel in ['OnStationname', 'DepartureTime', 'RosenName', 'KeitouNumber', 'Ikisaki', 'RequireTime', 'Fare', 'ArrivalTime', 'OffStationName', 'OffStationPole']:
            dic[sel] = _soup.find(id=selector_head_str.format(idx) + sel).text

        data.append(dic)
        idx += 1

    return data

def str2datetime(s):
    return datetime.datetime.now().strftime('%Y-%m-%d {0}:{1}:00'.format(*s.split(':')))


def get_data(url):
    soup = get_soup(url)
    soup = soup.find(id='ctl00_ContentPlaceHolder1_Usc_RouteG1_Usc_RouteDetailInfoFal_LnkBtn_ApproachInformation')

    js_str = str(soup).split('onclick="')[1].split('"')[0]
    js_str = js_str.replace('amp;', '')

    options = Options()
    options.add_argument('--headless')
    driver_path = '/app/.chromedriver/bin/chromedriver'
    chrome = webdriver.Chrome(options=options, executable_path=driver_path)

    chrome.get(url)
    chrome.execute_script(js_str)

    for w in chrome.window_handles:
        chrome.switch_to.window(w)
        if '岐阜バス接近情報' in chrome.title:
            break


    soup = BeautifulSoup(chrome.page_source, 'html.parser')

    table = soup.find_all('table', id='gwApploach')[0]

    ths, tds = [], []

    for tr in table.find_all('tr'):
        for th in tr.find_all('th'):
            ths.append(th.text)

    for tr in table.find_all('tr'):
        dic = {}
        for td, th in zip(tr.find_all('td'), ths):
            dic[th] = td.text
        if len(dic) == 0:
            continue
        tds.append(dic)

    df = pd.DataFrame(tds)

    delay_ts = [get_delay_time(s) for s in df['接近情報'].tolist()]
    df['delay_time'] = delay_ts

    span = soup.find_all('span', id='lblApproach')[0]
    collect_time = span.text
    collect_time = datetime.datetime.strptime(collect_time, '%Y年%m月%d日 %H:%M現在').strftime('%Y-%m-%d %H:%M:00')
    df['collect_time'] = [collect_time for _ in range(len(df))]

    dep_place = soup.find_all('span', id='lblHbusStopName')[0].text
    arr_place = soup.find_all('span', id='lblCbusStopName')[0].text

    df['departure_place'] = [dep_place for _ in range(len(df))]
    df['arrival_place'] = [arr_place for _ in range(len(df))]

    chrome.quit()

    #return pd.concat(dfs)
    return df


def get_url(hour, minute, dep_place, arr_place):
    now = datetime.datetime.now()
    url_format = 'http://navi.gifubus.co.jp/Frm_0160.aspx?ge=tx_1l9_359_4ot_5gl_68d_7rx&id=1s4dxi&ia=1s4dur&d=1&t={0}{1}&a=1&tt=1&cm=1&ds={2}&as={3}&inpym={4}%2f{5}&inpymd={4}%2f{5}%2f{6}&inpt={0}{1}&inpa=1'

    hour = str(hour).zfill(2)
    minute = str(minute - minute % 5).zfill(2)
    month = now.strftime('%m').zfill(2)
    day = now.strftime('%d').zfill(2)

    return url_format.format(hour, minute, dep_place, arr_place, now.strftime('%Y'), month, day)

"""
MAIN
"""
if __name__ == '__main__':

    dep_place = 'メディアコスモス・鶯谷高校口'
    arr_place = 'ＪＲ岐阜'
    now = datetime.datetime.now()
    url = get_url(now.hour, now.minute, dep_place, arr_place)
    print(url)

    df = get_data(url)

    csv_path = 'guide.csv'
    if osp.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False)
    else:
        df.to_csv(csv_path)

    df = pd.read_csv(csv_path, index_col=0)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df.to_csv(csv_path)

















#

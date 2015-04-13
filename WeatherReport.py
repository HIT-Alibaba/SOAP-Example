# -*- coding:utf-8 -*-

import sys

from flask import Flask, render_template
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import


reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.webxml.com.cn/WebServices/WeatherWebService.asmx?wsdl'

imp = Import('http://www.w3.org/2001/XMLSchema',
             location='http://localhost:8000/XMLSchema.xsd')
imp.filter.add('http://WebXml.com.cn/')
client = Client(url, doctor=ImportDoctor(imp))

app = Flask(__name__)

cities_cache = {}
province_cache = None


@app.route('/')
def index():
    global province_cache
    province_list = client.service.getSupportProvince()
    if province_cache is not None:
        province = province_cache
    else:
        province = province_list[0]

    return render_template('index.html', province=province)


@app.route('/getCity/<string:province>')
def get_city(province):
    global cities_cache
    cities_list = client.service.getSupportCity(province)
    cities = []
    if province in cities_cache:
        cities = cities_cache[province]
    else:
        for raw_city in cities_list[0]:
            r = raw_city.split(' ')
            _id = r[-1]
            name = ' '.join(r[0:-1])
            _id = int(_id.lstrip('(').rstrip(')'))
            t = {'name': name, 'id': _id}
            cities.append(t)
        cities_cache[province] = cities
    return render_template('city.html', cities=cities, province=province)


@app.route('/getWeather/<int:city_id>')
def get_weather(city_id):
    r = client.service.getWeatherbyCityName(city_id)
    t = r[0]
    city_name = t[1]
    today = ' '.join([t[6], t[5], t[7]])
    tomorrow = ' '.join([t[13], t[12], t[14]])
    the_day_after_tomorrow = ' '.join([t[18], t[17], t[19]])
    city_info = t[22]
    return render_template("weatherResult.html", city_name=city_name, today=today, tomorrow=tomorrow,
                           the_day_after_tomorrow=the_day_after_tomorrow, city_info=city_info)


if __name__ == '__main__':
    app.run(debug=True)

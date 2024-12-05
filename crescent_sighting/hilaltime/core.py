# _jengkolrebus
# November 2024
# Yogyakarta

import numpy as np
from skyfield import almanac
from skyfield.api import load, Topos
from skyfield.units import Angle
from skyfield.framelib import ecliptic_frame
from skyfield.trigonometry import position_angle_of
from pytz import timezone

ts = load.timescale()
eph = load('de421.bsp')
moon = eph['moon']
sun = eph['sun']
jkt = timezone("Asia/Jakarta")

class var:
    config = {
        'latitude': 0,
        'longitude': 0,
        'date_start': 0,
        'date_end': 0,
    }
    data = {
        "conjunction": [],
        "sunset": [],
        "moonset": [],
        "moon_altitude": [],
        "moon_azimuth": [],
        "sun_altitude": [],
        "sun_azimuth": [],
        "elongation": [],
        "moon_age": [],
        "moon_app_diameter": [],
        "sun_app_diameter": [],
        "sun_astrometric": [],
        "moon_astrometric": [],
        "illumination": [],
        "lag_time": [],
        "crescent_angle": [],
    }
    MOON_DIAMETER = 3474.2 #1737.1 # km
    SUN_DIAMETER = 1392700 #696340 # km

class hilal():
    def __init__(self, latitude, longitude, date_start, date_end):
        self.latitude = latitude
        self.longitude = longitude
        self.date_start = date_start
        self.date_end = date_end
        self.loc = Topos(self.latitude, self.longitude)
        self.topo = eph['earth'] + self.loc

    def conjunction(self):
        date_start = ts.utc(self.date_start[0], self.date_start[1], self.date_start[2])
        date_end = ts.utc(self.date_end[0], self.date_end[1], self.date_end[2])
        f = almanac.oppositions_conjunctions(eph, eph['moon'])
        t, y = almanac.find_discrete(date_start, date_end, f)
        for ti, yi in zip(t, y):
            if(yi == 1):
                var.data['conjunction'].append(ti)
            else:
                pass

    def newmoon(self):
        conjunction = []
        date_start = ts.utc(self.date_start[0], self.date_start[1], self.date_start[2])
        date_end = ts.utc(self.date_end[0], self.date_end[1], self.date_end[2])
        f = almanac.moon_phases(eph)
        t, y = almanac.find_discrete(date_start, date_end, f)
        for ti, yi in zip(t, y):
            if(yi == 0):
                conjunction.append(ti)
            else:
                pass
        return conjunction

    def moonset(self, t):
        t = t.utc
        t0 = ts.utc(t[0], t[1], t[2], t[3], t[4], t[5])
        t1 = ts.utc(t[0], t[1], t[2]+1, t[3], t[4], t[5])
        f = almanac.risings_and_settings(eph, eph['moon'], self.loc, horizon_degrees=-0.833333)
        t, y = almanac.find_discrete(t0, t1, f)
        for ti, yi in zip(t, y):
            if(yi == 0):
                return ti
            else:
                pass
    
    def isMoonset(self, t):
        stat = self.moonset(t)
        if (stat == None):
            return True
        else:
            return False

    def sunset(self, t, case):
        t = t.utc
        t0 = ts.utc(t[0], t[1], t[2], t[3], t[4], t[5])
        t1 = ts.utc(t[0], t[1], t[2] + case, t[3], t[4], t[5])
        # print(t0, t1)
        f = almanac.sunrise_sunset(eph, self.loc)
        t, y = almanac.find_discrete(t0, t1, f)
        for ti, yi in zip(t, y):
            if(yi == False):
                # return ti
                if self.isMoonset(ti) == True:
                    self.sunset(ti, 2)
                else:
                    return ti
            else:
                pass
    def objPos(self, t, obj):
        astrometric = self.topo.at(t).observe(eph[obj])
        alt, az, d = astrometric.apparent().altaz()
        if (obj == 'moon'):
            appDiam = (2*np.arcsin(var.MOON_DIAMETER/(2*d.km)))*(180/np.pi)
        else:
            appDiam = (2*np.arcsin(var.SUN_DIAMETER/(2*d.km)))*(180/np.pi)
        return alt, az, appDiam, astrometric

    def elongation(self, moon, sun):
        elong = moon.separation_from(sun)
        return elong.degrees
    
    def crescentAngle(self, moon_astrometric, sun_astrometric):
        return position_angle_of(moon_astrometric.apparent().altaz(), sun_astrometric.apparent().altaz()).degrees
    
    def illumination(self, t):
        t = t.utc
        t = ts.utc(t[0], t[1], t[2], t[3], t[4], t[5])
        earth = eph['earth']

        e = earth.at(t)
        s = e.observe(sun).apparent()
        m = e.observe(moon).apparent()

        _, slon, _ = s.frame_latlon(ecliptic_frame)
        _, mlon, _ = m.frame_latlon(ecliptic_frame)

        illum = 100.00 * m.fraction_illuminated(sun)
        # print('Illumination: {0:.2f}%'.format(illum))
        return round(illum, 2)

    def altitude_map(latitude, longitude, t):
        loc = Topos(latitude, longitude)
        topo = eph['earth'] + loc
        
        t0 = ts.utc(t.year, t.month, t.day, t.hour, t.minute, t.second)
        t1 = ts.utc(t.year, t.month, t.day + 1, t.hour, t.minute, t.second)
        # print(t0, t1)
        f = almanac.sunrise_sunset(eph, loc)
        t, y = almanac.find_discrete(t0, t1, f)
        for ti, yi in zip(t, y):
            if(yi == False):
                sunset = ti
            else:
                pass
        
        # ketinggian hilal
        t = sunset
        astrometric = topo.at(t).observe(eph['moon'])
        alt, az, d = astrometric.apparent().altaz()
        return alt
    
    def tt_timezone(self, t, timezone):
        return t.astimezone(timezone)
    
    def find(self):
        # self.newmoon()
        print(var.data['conjunction'])
        var.data['conjunction'] = [i for i in self.newmoon()]

        sunset = [self.sunset(t, 1) for t in var.data["conjunction"]]
        # for index, i in enumerate(sunset):
        #     if self.isMoonset(i) == False:
        #         i = self.sunset(i, 2)
        #         sunset[index] = i
        #     else:
        #         pass
        
        moonset = [self.moonset(t) for t in sunset]
        var.data["sunset"] = sunset
        var.data["moonset"] = moonset
        var.data['illumination'] = [self.illumination(t) for t in sunset]

        var.data['moon_altitude'],
        var.data['moon_azimuth'],
        var.data['moon_app_diameter'],
        m = [self.objPos(t, "moon") for t in var.data["sunset"]]

        var.data['sun_altitude'],
        var.data['sun_azimuth'],
        var.data['sun_app_diameter'],
        s = [self.objPos(t, "sun") for t in var.data["sunset"]]
        self.elongation(m, s)

        var.data['elongation'] = [self.elongation(moon, sun) for (moon, sun) in zip(var.data["moon_astrometric"], var.data["sun_astrometric"])]

        [var.data["crescent_angle"].append((self.crescentAngle(x, y)).degrees) for (x, y) in zip(var.data['moon_astrometric'], var.data['sun_astrometric'])]

        # ubah format data di dictionary
        data_conj = [
            t.astimezone(jkt).replace(tzinfo=None) for t in var.data["conjunction"]
        ]
        var.data["conjunction"] = data_conj
        data_sunset = [
            t.astimezone(jkt).replace(tzinfo=None) for t in var.data["sunset"]
        ]
        var.data["sunset"] = data_sunset
        moon_age = [
            t1 - t0 for (t0, t1) in zip(var.data["conjunction"], var.data["sunset"])
        ]
        var.data["moon_age"] = moon_age
        data_moonset = [
            t.astimezone(jkt).replace(tzinfo=None) for t in var.data["moonset"]
        ]
        var.data["moonset"] = data_moonset

        var.data["lag_time"] = [x-y for (x, y) in zip(var.data["moonset"], var.data["sunset"])]

        for i in var.data:
            print(i, ':', var.data[i])


    def compute(self):
        data = var.data

        # conjunction
        conjunction = data['conjunction'] = self.newmoon()

        # sunset time
        sunset = data['sunset'] = [self.sunset(c, 1) for c in conjunction]

        # moonset time
        moonset = data['moonset'] = [self.moonset(s) for s in sunset]

        # sun position properties
        sun = [self.objPos(s, 'sun') for s in sunset]
        sun_altitude = data['sun_altitude'] = [i[0].degrees for i in sun]
        sun_azimuth = data['sun_azimuth'] = [i[1].degrees for i in sun]
        sun_app_diameter = data['sun_app_diameter'] = [i[2] for i in sun]
        sun_astrometric = data['sun_astrometric'] = [i[3] for i in sun]

        # moon position properties
        moon = [self.objPos(s, 'moon') for s in sunset]
        moon_altitude = data['moon_altitude'] = [i[0].degrees for i in moon]
        moon_azimuth = data['moon_azimuth'] = [i[1].degrees for i in moon]
        moon_app_diameter = data['moon_app_diameter'] = [i[2] for i in moon]
        moon_astrometric = data['moon_astrometric'] = [i[3] for i in moon]

        # elongation
        elongation = data['elongation'] = [self.elongation(moon, sun) for (moon, sun) in zip(moon_astrometric, sun_astrometric)]

        # illumination
        illumination = data['illumination'] = [self.illumination(t) for t in sunset]

        # crescent angle
        crescent_angle = data['crescent_angle'] = [self.crescentAngle(m, s) for (m, s) in zip(moon_astrometric, sun_astrometric)]

        # change time format to timezone
        data['conjunction'] = [self.tt_timezone(c, jkt) for c in data['conjunction']]
        data['sunset'] = [self.tt_timezone(s, jkt) for s in data['sunset']]
        data['moonset'] = [self.tt_timezone(m, jkt) for m in data['moonset']]

        # lag time
        lag_time = data['lag_time'] = [m-s for (m, s) in zip(data['moonset'], data['sunset'])]

        # moon_age
        moon_age = data['moon_age'] = [m-c for (m, c) in zip(data['moonset'], data['conjunction'])]
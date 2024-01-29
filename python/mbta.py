import requests
import json
import math
import time

from data import *
from util import *


class APIRequest(object):
    @staticmethod
    def make_request(method, parameters=None):
        headers = {'accept': 'application/vnd.api+json'}
        parameters = parameters or {}
        #print("----> make_request")
        #print("----> method = ", end="")
        #print(method)
        #print("----> parameters = ",end="")
        #print(parameters)
        r = requests.get(
            'https://api-v3.mbta.com/' + method + '?',
            params=parameters, headers=headers
        )
        #print("https://api-v3.mbta.com/stops?filter%5Broute%5D=Red")
        print(r.url)
        t = json.loads(r.text)
        #print(t)
        return t

    @staticmethod
    def stops_by_route(route):
        return APIRequest.make_request('stops', {'filter[route]': route})


class Route(object):
    def __init__(self, stations, name, api_name=None, train_filter=None):
        print("Route __init__")
        print("In Route __init__ stations are:")
        for st in Route.get(stations):
            print(st)
        print("In Route __init__ stations end")
        self.name = name
        self.api_name = api_name or name
        self.stations = map(stations.get, ROUTES[name])
        print("----------- After map -------------")
        print("In Route __init__ stations are:")
        for st in Route.get(stations):
            print(st)
        print("In Route __init__ stations end")
        self.stations_dict = {}
        print("--------------- Route __init__ ----------")
        for st in self.stations:
            #print(st)
            self.stations_dict[st.name] = st
        self.train_filter = train_filter
        print("In Route __init__ ABOUT TO RETURN stations are:")
        for st in Route.get(stations):
            print(st)
        print("In Route __init__ ABOUT TO RETURN stations end")
        
    def get(self):
        print("-------------- Route get ----------------");
        print("self = ",end="")
        print(self)
        for st in self.stations:
            print(st)
        print("-------------- Route get end ----------------");
        return self.stations

    def get_trains(self):
        print("--------------- get_trains --------------------")
        trains = []
        req = APIRequest.make_request(
            'vehicles', {'filter[route]': self.api_name})
        #print(req)
        if not req.get('data'):
            return []
        for vehicle in req['data']:
            #print("vehicle = ")
            #print(vehicle)
            trains.append(Train(
                #FIXME trip_name and trip_id
                "None",
                "1",
                (
                    float(vehicle['attributes']['latitude']),
                    float(vehicle['attributes']['longitude'])
                ),
                int(vehicle['attributes']['direction_id']),
                #FIXME
                #int(vehicle['attributes']['updated_at'])
                0
                )
            )
        #if self.train_filter:
            #trains = filter(self.train_filter, trains)
        for t in trains:
            print(t)
        return trains

    def locate_train(self, train):
        print("------------- locate_train  Stations -----------------")
        print("self = ",end="")
        print(self)
        for st in self.stations:
            print(st)
        print("------------- locate_train  Stations  END-----------------")
        for p in pairwise(self.stations):
            print(p)
            print(p[0].location);
            print(p[1].location);
            print(point_line_segment_distance(
                p[0].location,
                p[1].location,
                train.location))

        between = min(
            pairwise(
                self.stations),
            key=lambda a_b: point_line_segment_distance(
                a_b[0].location,
                a_b[1].location,
                train.location))
        progress = point_distance(
            train.location,
            between[0].location
        ) / point_distance(
            between[0].location,
            between[1].location
        )
        if train.direction == 1:
            between = tuple(reversed(between))
            progress = 1 - progress
        print("------------- locate_train end -----------------")
        return (between[0], between[1], progress)


class Routes(object):
    def __init__(self, stations):
        #print("Routes __init__")
        self.routes = {}
        for k in API_ROUTE_NAMES:
            #print("A----> ",end="")
            #print(k)
            #print("In Routes __init__ stations are:")
            #for st in Route.get(stations):
            #    print(st)
            #print("In Routes __init__ stations end")
            self.routes[k] = Route(stations, k, API_ROUTE_NAMES[k])
            print("Routes self = ",end="")
            print(self)
            #print("====")
            #print(self.routes)
        for k in API_ROUTE_FILTERS:
            self.routes[k].train_filter = API_ROUTE_FILTERS[k]

    def all(self):
        for k in self.routes:
            yield self.routes[k]

    def get(self, name):
        return self.routes[name]


class Train(object):
    def __init__(self, name, id, location, direction, timestamp):
        self.name = name
        self.id = id
        self.location = location
        self.direction = direction
        self.measurements = 1
        self.last_velocity = 0
        self.average_velocity = 0
        self.timestamp = timestamp


class Station(object):
    def __init__(self, name, location):
        self.lines = set()
        self.name = name
        self.location = location
        #print("Station object: name = ",end="")
        #print(name)

    def __str__(self):
        return self.name

    def transfer_station(self):
        return len(self.lines) > 1


class Stations(object):
    def __init__(self):
        self.stations = {}
        for route in API_ROUTE_NAMES.values():
            res = APIRequest.stops_by_route(route)
            stops = res['data']
            for s in stops:
                #print("--->")
                #print(s)
                name = s['attributes']['name']
                #print("StationS object: name= ",end="")
                #print(name)
                #for q in self.stations:
                #    print(q)
                station = Station(
                    name, (float(s['attributes']['latitude']), float(s['attributes']['longitude'])))
                if not self.stations.get(name):
                    #print("--- Setting station name to ",end="")
                    #print(name)
                    self.stations[name] = station
                else:
                    5/0
                self.stations[name].lines.add(route.split('-')[0])
                #print("stations.get('JFK/UMass') returns ",end="")
                #print(self.stations.get('JFK/UMass'))

    def get(self, name):
        #print("Stations.get(",end="")
        #print(name,end="")
        #print(") returns:")
        #print(self.stations.get(name))
        return self.stations.get(name)

    def get_location(self, name):
        station = self.stations.get(name)
        if not station:
            return False
        else:
            return station.location

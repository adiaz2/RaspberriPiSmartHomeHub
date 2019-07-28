from qhue import Bridge
from HuePhillipsRoom import HuePhillipsRoom
from HuePhillipsZone import HuePhillipsZone
from HuePhillipsLight import HuePhillipsLight

class HuePhillipsBridge:
    def __init__(self, ip, username):
        self.ipAddress = ip
        self.username = username
        self.bridge = Bridge(self.ipAddress, self.username)
        self.lights, self.groups, self.zones, self.rooms = {}, {}, {}, {}
        self.createLights()
        self.createGroups()

    def createLights(self):
        for light in self.bridge.lights:
            self.lights[light()['name']] = HuePhillipsLight(light)

    def createGroups(self):
        for g in self.bridge.groups:
            groupLights =
            for light in g()['lights']:
                groupLights.append()
            if g()['type'] is 'Zone':
                group = HuePhillipsZone()
            elif g()['type'] is 'Room':
                group = HuePhillipsRoom()

    @property
    def isOn(self):
        return self.lightDict['state']['on']

    @property
    def brightness(self):
        return self.lightDict['state']['bri']

    @brightness.setter
    def brightness(self, b):
        self.light.state(bri=b)

    def getGroupLights(self, group):
        group['lights']


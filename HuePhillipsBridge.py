from qhue import Bridge
from HuePhillipsRoom import HuePhillipsRoom
from HuePhillipsZone import HuePhillipsZone
from HuePhillipsLight import HuePhillipsLight



class HuePhillipsBridge:
    def __init__(self, ip, username):
        self.ipAddress = ip
        self.username = username
        self.bridge = Bridge(self.ipAddress, self.username)
        # Key is the qhue object, value is the HuePhillipsType object
        self.lights, self.groups, self.zones, self.rooms = {}, {}, {}, {}
        self.createLights()
        self.createGroups()

    def createLights(self):
        for light in self.bridge.lights().keys():
            print(light)
            self.lights[light] = HuePhillipsLight(self.bridge.lights[light])

    def createGroups(self):
        for group in self.bridge.groups().keys():
            realGroup = self.bridge.groups[group]
            if realGroup()['type'] == 'Zone':
                self.groups[group] = HuePhillipsZone(realGroup, self.getLightsFromGroup(realGroup))
                self.zones[group] = self.groups[group]
            elif realGroup()['type'] == 'Room':
                self.groups[group] = HuePhillipsRoom(realGroup, self.getLightsFromGroup(realGroup))
                self.rooms[group] = self.groups[group]

    def getAllLights(self):
        return list(self.lights.values())

    def getLightsFromGroup(self, group):
        groupLights = []
        for light in group()['lights']:
            groupLights.append(self.lights[light])
        return groupLights

    def getRooms(self):
        return self.rooms.values()

    def getZones(self):
        return self.zones.values()

    def getGroups(self):
        return self.groups.values()

    # @property
    # def isOn(self):
    #     return self.lightDict['state']['on']
    #
    # @property
    # def brightness(self):
    #     pass
    #
    # @brightness.setter
    # def brightness(self, b):
    #     self.light.state(bri=b)

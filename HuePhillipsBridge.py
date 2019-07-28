from qhue import Bridge

class HuePhillipsBridge:
    def __init__(self, ip, username):
        self.ipAddress = ip
        self.username = username
        self.bridge = Bridge(self.ipAddress, self.username)

    @property
    def groups(self):
        return self.bridge()['groups'].keys()

    @property
    def isOn(self):
        return self.lightDict['state']['on']

    @property
    def brightness(self):
        return self.lightDict['state']['bri']

    @brightness.setter
    def brightness(self, b):
        self.light.state(bri=b)

    def getGroupLights(self):

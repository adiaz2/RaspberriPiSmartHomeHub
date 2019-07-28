class HuePhillipsGroup:
    def __init__(self, group):
        self.group = group

    @property
    def groupDict(self):
        return self.group()

    @property
    def areAllOn(self):
        return self.groupDict['state']['all_on']

    @property
    def isOn(self):
        return self.groupDict['state']['any_on']

    @isOn.setter
    def isOn(self, setting):
        self.group.action(on=setting)

    @property
    def brightness(self):
        return self.groupDict['action']['bri']

    @brightness.setter
    def brightness(self, b):
        self.group.action(bri=b)

    @property
    def hue(self):
        return self.groupDict['action']['hue']

    @hue.setter
    def hue(self, h):
        self.group.action(hue=h)

    @property
    def saturation(self):
        return self.groupDict['action']['sat']

    @saturation.setter
    def saturation(self, s):
        self.group.action(sat=s)

    @property
    def name(self):
        return self.groupDict['name']

    def toggle(self):
        self.isOn = (not self.isOn)

    def startColorLoop(self):
        self.group.action(effect='colorloop')

    def stopColorLoop(self):
        self.group.action(effect='none')

    def setMaxBrightness(self):
        self.brightness = 254

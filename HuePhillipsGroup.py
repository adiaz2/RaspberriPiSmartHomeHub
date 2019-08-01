class HuePhillipsGroup:
    def __init__(self, group, lights):
        self.group = group
        self.lights = lights
        self.inactiveBrightness = self.brightness
        self.inactiveHue = self.hue
        self.inactiveSaturation = self.saturation

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
        if setting:
            self.brightness = self.inactiveBrightness
            self.hue = self.inactiveHue
            self.saturation = self.inactiveSaturation

    @property
    def brightness(self):
        return self.groupDict['action']['bri']

    @brightness.setter
    def brightness(self, b):
        self.inactiveBrightness = b
        self.group.action(bri=b)

    @property
    def hue(self):
        return self.groupDict['action']['hue']

    @hue.setter
    def hue(self, h):
        self.inactiveHue = h
        self.group.action(hue=h)

    @property
    def saturation(self):
        return self.groupDict['action']['sat']

    @saturation.setter
    def saturation(self, s):
        self.inactiveSaturation = s
        self.group.action(sat=s)

    @property
    def name(self):
        return self.groupDict['name']

    def getLightNames(self):
        return self.group().lights

    def getLights(self):
        return self.lights

    def setLights(self, lights):
        self.lights = lights

    def toggle(self):
        self.isOn = (not self.isOn)

    def startColorLoop(self):
        self.isOn = True
        self.group.action(effect='colorloop')

    def stopColorLoop(self):
        self.group.action(effect='none')

    def setMaxBrightness(self):
        self.brightness = 254

    def newColor(self, h, s, b):
        if h < 0:
            h = 0
        self.inactiveHue, self.inactiveSaturation, self.inactiveBrightness = h, s, b
        for light in self.lights:
            light.newColor(h, s, b)

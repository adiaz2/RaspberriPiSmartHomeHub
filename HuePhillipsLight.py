import time

class HuePhillipsLight:

    def __init__(self, light):
        self.light = light
        self.inactiveBrightness = self.brightness
        self.inactiveHue = self.hue
        self.inactiveSaturation = self.saturation

    @property
    def lightDict(self):
        return self.light()

    @property
    def isOn(self):
        return self.lightDict['state']['on']

    @isOn.setter
    def isOn(self, setting):
        self.light.state(on=setting)
        if setting:
            self.brightness = self.inactiveBrightness
            self.hue = self.inactiveHue
            self.saturation = self.inactiveSaturation

    @property
    def brightness(self):
        return self.lightDict['state']['bri']

    @brightness.setter
    def brightness(self, b):
        self.inactiveBrightness = b
        if self.isOn:
            self.light.state(bri=b)

    @property
    def hue(self):
        return self.lightDict['state']['hue']

    @hue.setter
    def hue(self, h):
        self.inactiveHue = h
        if self.isOn:
            self.light.state(hue=h)

    @property
    def saturation(self):
        return self.lightDict['state']['sat']

    @saturation.setter
    def saturation(self, s):
        self.inactiveSaturation = s
        if self.isOn:
            self.light.state(sat=s)

    @property
    def name(self):
        return self.lightDict['name']

    @property
    def productname(self):
        return self.lightDict['productname']

    def toggle(self):
        self.isOn = (not self.isOn)

    def turnOn(self):
        self.isOn = True

    def turnOff(self):
        self.isOn = False

    def blinkLight(self):
        self.turnOff()
        time.sleep(.4)
        self.turnOn()

    def startColorLoop(self):
        self.isOn = True
        self.light.state(effect='colorloop')

    def stopColorLoop(self):
        self.light.state(effect='none')

    def setMaxBrightness(self):
        self.brightness = 254

    def newColor(self, h, s, b):
        if h < 0:
            h = 0
        self.inactiveHue, self.inactiveSaturation, self.inactiveBrightness = h, s, b
        try:
            self.light.state(hue=h, sat=s, bri=b)
        except:
            pass
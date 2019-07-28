class HuePhillipsLight:

    def __init__(self, light):
        self.light = light

    @property
    def lightDict(self):
        return self.light()

    @property
    def isOn(self):
        return self.lightDict['state']['on']

    @isOn.setter
    def isOn(self, setting):
        self.light.state(on=setting)

    @property
    def brightness(self):
        return self.lightDict['state']['bri']

    @brightness.setter
    def brightness(self, b):
        self.light.state(bri=b)

    @property
    def hue(self):
        return self.lightDict['state']['hue']

    @hue.setter
    def hue(self, h):
        self.light.state(hue=h)

    @property
    def saturation(self):
        return self.lightDict['state']['sat']

    @saturation.setter
    def saturation(self, s):
        self.light.state(sat=s)

    @property
    def name(self):
        return self.lightDict['name']

    @property
    def productname(self):
        return self.lightDict['productname']

    def toggle(self):
        self.isOn = (not self.isOn)

    def startColorLoop(self):
        self.light.state(effect='colorloop')

    def stopColorLoop(self):
        self.light.state(effect='none')

    def setMaxBrightness(self):
        self.brightness = 254

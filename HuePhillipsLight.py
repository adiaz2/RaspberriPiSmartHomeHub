class HuePhillipsLight:

    def __init__(self, light):
        self.light = light

    #These are properties. they are recalculated each time to ensure the correct value
    @property
    def lightDict(self):
        return self.light()

    @property
    def isOn(self):
        return self.lightDict['state']['on']
        
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
        return self.lightDict['name']

    def turnOn(self):
        self.light.state(on=True)

    def turnOff(self):
        self.light.state(on=False)

    def toggle(self):
        self.light.state(on=(not self.isOn))

    def startColorLoop(self):
        self.light.state(effect='colorloop')

    def setMaxBrightness(self):
        self.brightness = 255









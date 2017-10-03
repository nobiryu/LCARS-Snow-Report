from datetime import datetime
import pygame, urllib, cStringIO
from pygame.mixer import Sound
from PIL import Image

from ui import colours
from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen
from ui.widgets.sprite import LcarsMoveToMouse

class ScreenMain(LcarsScreen):
    def setup(self, all_sprites):
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1b.png"),
                        layer=0)
	# Image reference
	WINTERPARKSNOW = cStringIO.StringIO(urllib.urlopen("http://cams.winterparkresort.com/winter-park-basecam.jpg").read())
	WINTERPARKSNOW2 = Image.open(WINTERPARKSNOW)
	WINTERPARK2 = WINTERPARKSNOW2.resize((380,232), Image.ANTIALIAS)
	WINTERPARK2.save("WINTERPARKSNOW.jpg")
	KEYSTONESNOW = cStringIO.StringIO(urllib.urlopen("http://common.snow.com/mtncams/riverrun.jpg").read())
        KEYSTONESNOW2 = Image.open(KEYSTONESNOW)
        KEYSTONE2 = KEYSTONESNOW2.resize((380,232), Image.ANTIALIAS)
        KEYSTONE2.save("KEYSTONESNOW.jpg")      
	BRECKENRIDGESNOW = cStringIO.StringIO(urllib.urlopen("http://common.snow.com/Mtncams/brecksnowcam.jpg").read())
        BRECKENRIDGESNOW2 = Image.open(BRECKENRIDGESNOW)
        BRECKENRIDGE2 = BRECKENRIDGESNOW2.resize((380,232), Image.ANTIALIAS)
        BRECKENRIDGE2.save("BRECKENRIDGESNOW.jpg")


        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (15, 44), "COLORADO"),
                        layer=1)
        all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "SNOW REPORT", 2),
                        layer=1)
        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "WEATHER"),
                        layer=1)
        all_sprites.add(LcarsBlockSmall(colours.ORANGE, (211, 16), "CAMERAS"),
                        layer=1)
        all_sprites.add(LcarsBlockLarge(colours.BEIGE, (249, 16), "ENERGY"),
                        layer=1)
        all_sprites.add(LcarsText(colours.BLACK, (444, 612), "172 18 0 99"),
                        layer=1)

        # info text
        all_sprites.add(LcarsText(colours.WHITE, (192, 174), "RESORT OPENING DAY:", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (244, 174), "WINTER PARK: NOVEMBER 15, 2017", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (286, 174), "ARAPAHOE BASEN: MID OCTOBER", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (330, 174), "KEYSTONE: NOVEMBER 10, 2017", 1.5),
                        layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (370, 174), "BRECKENRIDGE:  NOVEMBER 10, 2017", 1.5),
                        layer=3)
        self.info_text = all_sprites.get_sprites_from_layer(3)

        # date display
        self.stardate = LcarsText(colours.BLUE, (12, 380), "STAR DATE 2711.05 17:54:32", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # buttons        
        all_sprites.add(LcarsButton(colours.RED_BROWN, (6, 662), "LOGOUT", self.logoutHandler),
                        layer=4)
        #all_sprites.add(LcarsButton(colours.BEIGE, (107, 127), "DASHBOARD", self.sensorsHandler),
        #                layer=4)
        all_sprites.add(LcarsButton(colours.PURPLE, (107, 262), "BRECKENRIDGE", self.sensorsHandler),
                        layer=4)
        all_sprites.add(LcarsButton(colours.BEIGE, (107, 127), "KEYSTONE", self.gaugesHandler),
                        layer=4)
        #all_sprites.add(LcarsButton(colours.PEACH, (107, 398), "WINTER PARK", self.weatherHandler),
        #                layer=4)
        all_sprites.add(LcarsButton(colours.PEACH, (107, 398), "WINTER PARK", self.weatherHandler),
                        layer=4)

        # gadgets        
        all_sprites.add(LcarsGifImage("assets/gadgets/fwscan.gif", (277, 556), 100), layer=1)
        
        self.sensor_gadget = LcarsImage ("BRECKENRIDGESNOW.jpg", (200, 130)) 
        self.sensor_gadget.visible = False
        all_sprites.add(self.sensor_gadget, layer=2)

        self.dashboard = LcarsImage("KEYSTONESNOW.jpg", (200, 130))
        self.dashboard.visible = False
        all_sprites.add(self.dashboard, layer=2) 

        self.weather = LcarsImage("WINTERPARKSNOW.jpg", (200, 130))
	self.weather.visible = False
        all_sprites.add(self.weather, layer=2) 

        self.gauges = LcarsImage("KEYSTONESNOW.jpg", (200, 130))
        self.gauges.visible = False
        all_sprites.add(self.weather, layer=2)

        #all_sprites.add(LcarsMoveToMouse(colours.WHITE), layer=1)
        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/panel/220.wav").play()

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)
        
    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.beep1.play()

        if event.type == pygame.MOUSEBUTTONUP:
            return False

    def hideInfoText(self):
        if self.info_text[0].visible:
            for sprite in self.info_text:
                sprite.visible = False

    def gaugesHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = True
        self.weather.visible = False

    def sensorsHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = True
        self.dashboard.visible = False
        self.weather.visible = False
    
    def weatherHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = False
        self.weather.visible = True
    
    def logoutHandler(self, item, event, clock):
        from screens.authorize import ScreenAuthorize
        self.loadScreen(ScreenAuthorize())
    
    

from kivy.uix.image import Image
from kivy.clock import Clock

class PixelImage(Image):

    def __init__(self, **kwargs):
        super(PixelImage, self).__init__(**kwargs)
        Clock.schedule_once(self.set_texture_filters)

    def set_texture_filters(self, dt):
        if self.texture is None:
            return
        self.texture.mag_filter = 'nearest'
        self.texture.min_filter = 'nearest'
        self.canvas.ask_update()

    def on_source(self, instance, value):
        Clock.schedule_once(self.set_texture_filters)
from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm


class MapTile(sw.Tile):
    def __init__(self):

        self.map = sm.SepalMap()

        super().__init__("map_tile", "Map", inputs=[self.map])

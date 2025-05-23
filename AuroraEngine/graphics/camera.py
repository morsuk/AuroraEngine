import OpenGL.GL as opengl
from ..essentials import Vector2

class Camera:

    MainCamera: "Camera"

    def __init__(self, screen_size: tuple[int, int]):
        self.position = Vector2(0, 0)
        self.zoom = 1.0
        self.screen_size = screen_size
        
    def applyProjection(self):
        width, height = self.screen_size
        aspect = width / height

        opengl.glMatrixMode(opengl.GL_PROJECTION)
        opengl.glLoadIdentity()

        left, right = -aspect * self.zoom, aspect * self.zoom
        bottom, top = -1 * self.zoom, 1 * self.zoom

        opengl.glOrtho(left + self.position.x, right + self.position.x,
                bottom + self.position.y, top + self.position.y,
                -1, 1)

        opengl.glMatrixMode(opengl.GL_MODELVIEW)
        opengl.glLoadIdentity()

    def update_screen_size(self, width, height):
        self.screen_size = (width, height)

    def screenToWorld(self, x, y) -> Vector2:
        width, height = self.screen_size
        aspect = width / height


        ndc_x = (x / width) * 2 - 1
        ndc_y = 1 - (y / height) * 2 

        world_x = ndc_x * aspect * self.zoom + self.position.x
        world_y = ndc_y * self.zoom + self.position.y
        return Vector2(world_x, world_y)

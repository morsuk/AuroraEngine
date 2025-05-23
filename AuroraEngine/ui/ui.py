from ..essentials import Vector2
from OpenGL.GL import *

class UIElement:
    def __init__(self, position: Vector2, size: Vector2):
        self.position = position
        self.size = size
        self.visible = True

    def draw(self):
        pass

    def on_click(self):
        pass

    def contains_point(self, point: Vector2) -> bool:
        x, y = point.x, point.y
        left = self.position.x
        right = self.position.x + self.size.x
        bottom = self.position.y
        top = self.position.y + self.size.y
        return left <= x <= right and bottom <= y <= top

class UIManager:
    def __init__(self):
        self.elements = []

    def add(self, element: UIElement):
        self.elements.append(element)

    def draw(self):
        for element in self.elements:
            element.draw()

    def handle_click(self, mouse_pos: Vector2):
        for element in self.elements:
            if element.visible and element.contains_point(mouse_pos):
                element.on_click()


class Button(UIElement):
    def __init__(self, position: Vector2, size: Vector2, text: str, callback):
        super().__init__(position, size)
        self.text = text
        self.callback = callback

    def draw(self):
        if not self.visible:
            return

        glColor3f(0.2, 0.2, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(self.position.x, self.position.y)
        glVertex2f(self.position.x + self.size.x, self.position.y)
        glVertex2f(self.position.x + self.size.x, self.position.y + self.size.y)
        glVertex2f(self.position.x, self.position.y + self.size.y)
        glEnd()


    def on_click(self):
        if self.callback:
            self.callback()

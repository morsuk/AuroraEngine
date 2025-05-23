from ..scenes import SceneManager
from ..essentials import Vector2

class Physics:
    class Collisions:
        @staticmethod
        def boxColission(pos1: Vector2, scale1: Vector2, pos2: Vector2, scale2: Vector2):
            return (
                abs(pos1.x - pos2.x) * 2 < (scale1.x + scale2.x) and
                abs(pos1.y - pos2.y) * 2 < (scale1.y + scale2.y)
            )
    class Raycast:
        pass 
from AuroraEngine import *
from AuroraEngine.essentials import GameObject

class PlayerMovement(Component):
    def __init__(self, gameObject: GameObject, speed: float, rotationSpeed: float):
        super().__init__(gameObject)
        self.rotationSpeed: float = rotationSpeed
        self.speed: float = speed
        
    def update(self):
        self.gameObject.transform.rotate(self.rotationSpeed * System.deltaTime)
        mousePos: Vector2 = Camera.MainCamera.screenToWorld(*Input.getMousePos())
        self.gameObject.transform.position = Vector2.lerp(self.gameObject.transform.position, mousePos, self.speed * System.deltaTime)
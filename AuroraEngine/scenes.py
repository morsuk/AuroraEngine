from .essentials import GameObject
from typing import Optional

class Scene:
    def __init__(self, name: str):
        self.gameObjects: list[GameObject] = []
        self.name = name

    def updateScene(self) -> None:
        for gameObject in self.gameObjects:
            gameObject.updateComponents()

    def instantiate(self, gameObject: GameObject) -> None:
        self.gameObjects.append(gameObject)


class SceneManager:
    _currentScene: Optional[Scene] = None

    @staticmethod
    def loadScene(sceneObject: Scene) -> None:
        SceneManager._currentScene = sceneObject

    @staticmethod
    def getScene() -> Optional[Scene]:
        return SceneManager._currentScene
    



    

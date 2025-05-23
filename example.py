from AuroraEngine import *
from AuroraEngine.components.SpriteRenderer import SpriteRenderer
from components.PlayerMovement import PlayerMovement

screen = Window((800, 600), title="AuroraEngine Preview")
screen.setAspectRatio((16,9))
screen.disableVSync()
screen.limitFPS(0)


main_scene = Scene('Main Scene')
screen.camera.zoom = 1

player = GameObject('Player1', transform=Transform(Vector2.zero(), 0, Vector2.one()))
player.addComponent(SpriteRenderer, sprite="rectangle")
player.addComponent(PlayerMovement, speed=5, rotationSpeed=720)
player.transform.scale = Vector2(.2, .2)
main_scene.instantiate(player)

while screen.mainloop():
    
    screen.refresh()
    main_scene.updateScene()
    screen.renderScreen()

 
System.exit()
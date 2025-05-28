import OpenGL.GL as opengl
from ..essentials import Component, GameObject, Console, Color32

class SpriteRenderer(Component):

    def __init__(self, gameObject: GameObject, sprite: str = "None", color:Color32 = Color32(255, 255, 255, 1)):
        super().__init__(gameObject)
        self.sprite = sprite
        self.color:Color32 = color


    def start(self):
        pass


    def update(self):

        opengl.glPushMatrix()
        opengl.glTranslatef(self.gameObject.transform.position.x, self.gameObject.transform.position.y, 0)
        opengl.glRotatef(self.gameObject.transform.rotation, 0, 0, 1)
        opengl.glScalef(self.gameObject.transform.scale.x, self.gameObject.transform.scale.y, 1)

        match self.sprite:
            case "rectangle":
                opengl.glBegin(opengl.GL_QUADS)
                opengl.glColor3f(*self.color.getColor())
                opengl.glVertex2f(-0.5, -0.5)
                opengl.glVertex2f( 0.5, -0.5)
                opengl.glVertex2f( 0.5,  0.5)
                opengl.glVertex2f(-0.5,  0.5)
                opengl.glEnd()


            case "triangle":
                opengl.glBegin(opengl.GL_TRIANGLES)
                opengl.glColor3f(*self.color.getColor())
                opengl.glVertex2f(-0.5, -0.5)
                opengl.glVertex2f( 0.5, -0.5)
                opengl.glVertex2f( 0.0,  0.5)
                opengl.glEnd()

            case _:
                Console.warn(f"No sprite with name {self.sprite} found. - [{self.gameObject.name}]")

        opengl.glPopMatrix() 
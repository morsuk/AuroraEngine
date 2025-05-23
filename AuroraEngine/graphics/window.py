import glfw
import OpenGL.GL as opengl
from ..input import Input
from ..essentials import Vector2, System, EngineSettings, Console
from .camera import Camera

class Window:
    def __init__(self, dimensions: tuple, title: str = "AuroraEngine Window", _GLFW_Monitor = None, _GLFW_Share = None):
        if not glfw.init():
            raise Exception("GLFW cannot be initialized")
        
        self.dimensions = dimensions
        self.window = glfw.create_window(self.dimensions[0], self.dimensions[1], title, _GLFW_Monitor, _GLFW_Share)
        self.camera = Camera(glfw.get_framebuffer_size(window=self.window))
        Camera.MainCamera = self.camera

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window cannot be created")
        
        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, self.framebufferSizeCallback)
        Input.setWindow(self.window)

    
    @staticmethod
    def limitFPS(fps: int) -> None:
        EngineSettings.fps_limit = fps

    @staticmethod
    def clear() -> None:
        glfw.poll_events()
        opengl.glClear(opengl.GL_COLOR_BUFFER_BIT)

    @staticmethod
    def loadIdentity() -> None:
        opengl.glLoadIdentity()

    def mainloop(self) -> bool:
        Input.update()
        return not glfw.window_should_close(self.window)
        

    def framebufferSizeCallback(self, window, width, height) -> None:
        opengl.glViewport(0, 0, width, height)
        self.camera.update_screen_size(width, height)
        self.camera.applyProjection()

        self.dimensions = glfw.get_framebuffer_size(self.window)

    def setAspectRatio(self, ratio: tuple) -> None:
        glfw.set_window_aspect_ratio(self.window, *ratio)

    def disableVSync(self) -> None:
        glfw.swap_interval(0)

    def screenToWorldPos(self,x, y) -> Vector2:
        width, height = self.dimensions
        norm_x: float = (x / width) * 2 - 1
        norm_y: float = 1 - (y / height) * 2
        return Vector2(norm_x * (width / height), norm_y)
    
    def refresh(self) -> None:
        self.camera.applyProjection()
        Window.clear()
        self.loadIdentity()

    

    def renderScreen(self) -> None:
        """Refreshes the screen and performs important post frame calculations. Last function you should call in the mainloop."""
        glfw.swap_buffers(self.window)
        System.deltaTime = System.time() - System.lastFrameTimestamp
        if System.deltaTime > EngineSettings.deltaTimeMaxOverhead:
            if EngineSettings.deltaTimeOverheadWarning:
                Console.warn("Deltatime overhead exceeded set limit, ignore during startup.\n" +
                "Change EngineSettings.deltaTimeOverheadWarning to disable this warning.")
            System.deltaTime = 0
        System.lastFrameTimestamp = System.time()
        if EngineSettings.fps_limit and not EngineSettings.fps_limit == 0:
            System.wait(1 / EngineSettings.fps_limit)

    
    



 
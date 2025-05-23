import glfw
from .essentials import *

class Input:
    _window = None
    _previous_keys = {}
    Keys: dict = {'UNKNOWN': -1, 'SPACE': 32, 'APOSTROPHE': 39, 'COMMA': 44, 'MINUS': 45, 'PERIOD': 46, 'SLASH': 47, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57, 'SEMICOLON': 59, 'EQUAL': 61, 'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90, 'LEFT_BRACKET': 91, 'BACKSLASH': 92, 'RIGHT_BRACKET': 93, 'GRAVE_ACCENT': 96, 'WORLD_1': 161, 'WORLD_2': 162, 'ESCAPE': 256, 'ENTER': 257, 'TAB': 258, 'BACKSPACE': 259, 'INSERT': 260, 'DELETE': 261, 'RIGHT': 262, 'LEFT': 263, 'DOWN': 264, 'UP': 265, 'PAGE_UP': 266, 'PAGE_DOWN': 267, 'HOME': 268, 'END': 269, 'CAPS_LOCK': 280, 'SCROLL_LOCK': 281, 'NUM_LOCK': 282, 'PRINT_SCREEN': 283, 'PAUSE': 284, 'F1': 290, 'F2': 291, 'F3': 292, 'F4': 293, 'F5': 294, 'F6': 295, 'F7': 296, 'F8': 297, 'F9': 298, 'F10': 299, 'F11': 300, 'F12': 301, 'F13': 302, 'F14': 303, 'F15': 304, 'F16': 305, 'F17': 306, 'F18': 307, 'F19': 308, 'F20': 309, 'F21': 310, 'F22': 311, 'F23': 312, 'F24': 313, 'F25': 314, 'KP_0': 320, 'KP_1': 321, 'KP_2': 322, 'KP_3': 323, 'KP_4': 324, 'KP_5': 325, 'KP_6': 326, 'KP_7': 327, 'KP_8': 328, 'KP_9': 329, 'KP_DECIMAL': 330, 'KP_DIVIDE': 331, 'KP_MULTIPLY': 332, 'KP_SUBTRACT': 333, 'KP_ADD': 334, 'KP_ENTER': 335, 'KP_EQUAL': 336, 'LEFT_SHIFT': 340, 'LEFT_CONTROL': 341, 'LEFT_ALT': 342, 'LEFT_SUPER': 343, 'RIGHT_SHIFT': 344, 'RIGHT_CONTROL': 345, 'RIGHT_ALT': 346, 'RIGHT_SUPER': 347, 'MENU': 348}
    @staticmethod
    def setWindow(window):
        Input._window = window

    @staticmethod
    def Key(key: str) -> int:
        return  Input.Keys[key.upper()]

    @staticmethod
    def update():
        for key in range(glfw.KEY_SPACE, glfw.KEY_LAST):
            current = glfw.get_key(Input._window, key)
            Input._previous_keys[key] = current

    @staticmethod
    def getKey(key: int) -> bool:
        return glfw.get_key(Input._window, key) == glfw.PRESS
    
    @staticmethod
    def getKeyDown(key: int) -> bool:
        current = glfw.get_key(Input._window, key)
        previous = Input._previous_keys.get(key, glfw.RELEASE)
        return current == glfw.PRESS and previous == glfw.RELEASE

    @staticmethod
    def getAxis(axis: str) -> int:
        w = glfw.get_key(Input._window, glfw.KEY_W) == glfw.PRESS or glfw.get_key(Input._window, glfw.KEY_UP) == glfw.PRESS
        s = glfw.get_key(Input._window, glfw.KEY_S) == glfw.PRESS or glfw.get_key(Input._window, glfw.KEY_DOWN) == glfw.PRESS
        a = glfw.get_key(Input._window, glfw.KEY_A) == glfw.PRESS or glfw.get_key(Input._window, glfw.KEY_LEFT) == glfw.PRESS
        d = glfw.get_key(Input._window, glfw.KEY_D) == glfw.PRESS or glfw.get_key(Input._window, glfw.KEY_RIGHT) == glfw.PRESS

        if axis.lower() == "vertical":
            return -int(s) + int(w)
        elif axis.lower() == "horizontal":
            return -int(a) + int(d)
        return 0
    
    @staticmethod
    def getMousePos() -> Vector2:
        if Vector2(*glfw.get_cursor_pos(Input._window)):
            return Vector2(*glfw.get_cursor_pos(Input._window))
        else:
            return Vector2.zero()
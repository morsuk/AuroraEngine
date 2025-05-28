"""Code entirely written by AI (Alude Idiocracy) Contact at mc.morsuk@gmail.com"""

import OpenGL.GL as opengl
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt, pow, radians, degrees, exp, log, log10, floor, ceil, fabs, pi, e, copysign
import glfw
import time
from typing import Optional

class Vector2:
    
    zero: "Vector2"
    one: "Vector2"
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def magnitude(self) -> float:
        """Returns the magnitude, or 'length' of the vector."""
        return (self.x**2 + self.y**2)**0.5
    
    def normalized(self) -> "Vector2":
        """Returns direction of the vector, without retaining it's magnitude."""
        mag = self.magnitude()
        if mag == 0:
            return Vector2.zero
        return Vector2(self.x / mag, self.y / mag)
    
    
    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    
    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector2 index out of range (must be 0 or 1)")
    
    def __setitem__(self, index: int, value: float):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Vector2 index out of range (must be 0 or 1)")
        
    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __neg__(self) -> "Vector2":
        return Vector2(-self.x, -self.y)
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __contains__(self, item) -> bool:
        return item == self.x or item == self.y
    
    def getAngleTo(self, other: "Vector2") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return degrees(atan2(dy, dx))
    
    def distanceTo(self, other: "Vector2") -> float:
        """World space distance between two vectors."""
        return Vector2(abs(self.x - other.x), abs(self.y - other.y)).magnitude()
    
    @staticmethod
    def lerp(vec1: "Vector2", vec2: "Vector2", t: float) -> "Vector2":
        """Returns a vector between the two argument vectors dependent to the value of t."""
        return Vector2(vec1.x + (vec2.x - vec1.x) * t, vec1.y + (vec2.y - vec1.y) * t)


Vector2.zero = Vector2(0,0)
Vector2.one = Vector2(1,1)


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self) -> float:
        """Returns the magnitude, or 'length' of the vector."""
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalized(self) -> "Vector3":
        """Returns direction of the vector, without retaining it's magnitude."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3.zero()
        return Vector3(self.x / mag, self.y / mag, self.z / mag)
    
    @staticmethod
    def zero() -> "Vector3":
        return Vector3(0, 0, 0)
    
    @staticmethod
    def one() -> "Vector3":
        return Vector3(1, 1, 1)
    

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    
    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Vector3 index out of range (must be 0-2)")
    
    def __setitem__(self, index: int, value: float):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError("Vector2 index out of range (must be 0-2)")
        
    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> "Vector3":
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __neg__(self) -> "Vector3":
        return Vector3(-self.x, -self.y, -self.z)
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    
    def __contains__(self, item) -> bool:
        return item == self.x or item == self.y or item == self.z
    
    def __abs__(self) -> "Vector3":
        return Vector3(abs(self.x), abs(self.y), abs(self.z))
    
    def cross(self, other: "Vector3") -> "Vector3":
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self, other: "Vector3") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def getAngleTo(self, other: "Vector2") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return degrees(atan2(dy, dx))
    
    def distanceTo(self, other: "Vector3") -> float:
        return Vector3(abs(self.x - other.x), abs(self.y - other.y), abs(self.z - other.z)).magnitude()
    
    @staticmethod
    def lerp(vec1: "Vector3", vec2: "Vector3", t: float) -> "Vector3":
        return Vector3(vec1.x + (vec2.x - vec1.x) * t, vec1.y + (vec2.y - vec1.y) * t, vec1.z + (vec2.z - vec1.z) * t)

class Quaternion:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def normalized(self) -> "Quaternion":
        mag = sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)
        return Quaternion(self.x / mag, self.y / mag, self.z / mag, self.w / mag)

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
        )

    def rotateVector(self, v: Vector3) -> Vector3:
        qvec = Vector3(self.x, self.y, self.z)
        uv = qvec.cross(v)
        uuv = qvec.cross(uv)
        uv = uv * (2.0 * self.w)
        uuv = uuv * 2.0
        return Vector3(v.x + uv.x + uuv.x, v.y + uv.y + uuv.y, v.z + uv.z + uuv.z)

    @staticmethod
    def fromAxisAngle(axis: Vector3, angle_degrees: float) -> "Quaternion":
        angle_rad = radians(angle_degrees)
        half_angle = angle_rad / 2
        s = sin(half_angle)
        axis = axis.normalized()
        return Quaternion(axis.x * s, axis.y * s, axis.z * s, cos(half_angle))

    @staticmethod
    def fromEulerAngles(pitch: float, yaw: float, roll: float) -> "Quaternion":
        pitch, yaw, roll = map(radians, (pitch, yaw, roll))
        cy = cos(yaw * 0.5)
        sy = sin(yaw * 0.5)
        cp = cos(pitch * 0.5)
        sp = sin(pitch * 0.5)
        cr = cos(roll * 0.5)
        sr = sin(roll * 0.5)

        return Quaternion(
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy
        )

    @staticmethod
    def slerp(q1: "Quaternion", q2: "Quaternion", t: float) -> "Quaternion":

        dot = q1.x * q2.x + q1.y * q2.y + q1.z * q2.z + q1.w * q2.w

        if dot < 0.0:
            q2 = Quaternion(-q2.x, -q2.y, -q2.z, -q2.w)
            dot = -dot

        DOT_THRESHOLD = 0.9995
        if dot > DOT_THRESHOLD:
            result = Quaternion(
                q1.x + t * (q2.x - q1.x),
                q1.y + t * (q2.y - q1.y),
                q1.z + t * (q2.z - q1.z),
                q1.w + t * (q2.w - q1.w)
            )
            return result.normalized()

        theta_0 = acos(dot)
        sin_theta_0 = sin(theta_0)
        theta = theta_0 * t
        sin_theta = sin(theta)

        s0 = cos(theta) - dot * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0

        return Quaternion(
            q1.x * s0 + q2.x * s1,
            q1.y * s0 + q2.y * s1,
            q1.z * s0 + q2.z * s1,
            q1.w * s0 + q2.w * s1
        )

    def __str__(self) -> str:
        return f"Quaternion({self.x}, {self.y}, {self.z}, {self.w})"


    


class Transform:
    def __init__(self, position: Vector2 = Vector2.zero, rotation: float = 0, scale: Vector2 = Vector2.zero) -> None:
        self.position: Vector2 = position
        self.rotation: float = rotation
        self.scale: Vector2 = scale

    def distanceTo(self, other: "Transform") -> float:
        return (self.position - other.position).magnitude()
    
    def rotate(self, angle: float) -> None:
        self.rotation += angle

    def __str__(self) -> str:
        return f"Transform({self.position},{self.rotation},{self.scale})"
    
    def __iter__(self):
        return iter((self.position, self.rotation, self.scale))


class GameObject:
    def __init__(self, name: str, transform: Transform = Transform(Vector2.zero, 0, Vector2.one)):
        self.name: str = name
        self.transform = transform
        self.components: list[Component] = []
        

    def addComponent(self, componentClass, *args, **kwargs) -> "Component":
        component: "Component" = componentClass(self, *args, **kwargs)
        self.components.append(component)
        component.start()
        return component

    def getComponent(self, componentClass):
        for c in self.components:
            if isinstance(c, componentClass):
                return c
        return None

    def updateComponents(self):
        for component in self.components:
            component.update()


    def getDirection(self, direction: str = "forward") -> Vector2:
        angle: float = radians(self.transform.rotation)
        match direction:
            case "forward":
                return Vector2(cos(angle), sin(angle))

            case "right":
                return Vector2(cos(angle + 1.570796), sin(angle + 1.570796))
            
            case "left":
                return Vector2(cos(angle - 1.570796), sin(angle - 1.570796))

            case "backward":
                return -Vector2(cos(angle), sin(angle))
            
            case _:
                return Vector2.zero
            

class Component:
    def __init__(self, gameObject: GameObject):
        self.gameObject: GameObject = gameObject

    def start(self):
        pass

    def update(self):
        pass

class System:
    deltaTime: float = 0
    lastFrameTimestamp: float = 0

    @staticmethod
    def exit() -> None:
        glfw.terminate()

    @staticmethod
    def wait(seconds: float) -> None:
        time.sleep(seconds)

    @staticmethod
    def time() -> float:
        return time.time()
    
class Console:
    @staticmethod
    def warn(string: Optional[str]) -> None:
        print(f"\033[33m{string}\033[0m")

    @staticmethod
    def error(string: Optional[str]) -> None:
        print(f"\033[31m{string}\033[0m")

    @staticmethod
    def log(string: Optional[str]) -> None:
        print(string)

class EngineSettings:
    deltaTimeMaxOverhead = 10
    deltaTimeOverheadWarning = True
    fps_limit = 0


class Mathf:
    PI = pi
    TAU = 2 * pi
    E = e
    EPSILON = 1e-6

    @staticmethod
    def sqrt(x: float) -> float:
        return sqrt(x)

    @staticmethod
    def pow(x: float, y: float) -> float:
        return pow(x, y)

    @staticmethod
    def abs(x: float) -> float:
        return fabs(x)
    
    @staticmethod
    def max(*args: float) -> float:
        return max(args)

    @staticmethod
    def min(*args: float) -> float:
        return min(args)

    @staticmethod
    def sign(x: float) -> float:
        return copysign(1.0, x)

    @staticmethod
    def sin(x: float) -> float:
        return sin(x)

    @staticmethod
    def cos(x: float) -> float:
        return cos(x)

    @staticmethod
    def tan(x: float) -> float:
        return tan(x)

    @staticmethod
    def asin(x: float) -> float:
        return asin(x)

    @staticmethod
    def acos(x: float) -> float:
        return acos(x)

    @staticmethod
    def atan(x: float) -> float:
        return atan(x)

    @staticmethod
    def atan2(y: float, x: float) -> float:
        return atan2(y, x)

    @staticmethod
    def exp(x: float) -> float:
        return exp(x)

    @staticmethod
    def log(x: float, base: float = e) -> float:
        return log(x, base)

    @staticmethod
    def log10(x: float) -> float:
        return log10(x)

    @staticmethod
    def floor(x: float) -> float:
        return floor(x)

    @staticmethod
    def ceil(x: float) -> float:
        return ceil(x)

    @staticmethod
    def round(x: float) -> float:
        return round(x)

    @staticmethod
    def clamp(x: float, min_val: float, max_val: float) -> float:
        return max(min(x, max_val), min_val)

    @staticmethod
    def clamp01(x: float) -> float:
        return Mathf.clamp(x, 0.0, 1.0)

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * Mathf.clamp01(t)

    @staticmethod
    def lerpUnclamped(a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    @staticmethod
    def inverseLerp(a: float, b: float, value: float) -> float:
        if abs(b - a) < Mathf.EPSILON:
            return 0.0
        return Mathf.clamp01((value - a) / (b - a))

    @staticmethod
    def deltaAngle(a: float, b: float) -> float:
        diff = (b - a + 180.0) % 360.0 - 180.0
        return diff if diff != -180.0 else 180.0

    @staticmethod
    def moveTowards(current: float, target: float, max_delta: float) -> float:
        if abs(target - current) <= max_delta:
            return target
        return current + Mathf.sign(target - current) * max_delta

    @staticmethod
    def repeat(t: float, length: float) -> float:
        return t % length

    @staticmethod
    def pingPong(t: float, length: float) -> float:
        t = Mathf.repeat(t, length * 2)
        return length - abs(t - length)

    @staticmethod
    def deg2rad(deg: float) -> float:
        return radians(deg)

    @staticmethod
    def rad2deg(rad: float) -> float:
        return degrees(rad)

    @staticmethod
    def approximately(a: float, b: float) -> bool:
        return abs(a - b) < Mathf.EPSILON
    
    @staticmethod
    def mirror(x: float, bounds: float) -> float:
        """Reflects value within bounds like a mirror at the edges."""
        x = abs(x)
        while x > bounds:
            x = bounds - (x - bounds)
        return x
    
    @staticmethod
    def oscillate(x: float, amplitude: float = 1.0, frequency: float = 1.0) -> float:
        """Returns a sine wave oscillation over time."""
        return amplitude * sin(x * frequency)
    
    @staticmethod
    def gamma(value: float, absmax: float, gamma: float) -> float:
        """Applies gamma correction to a value."""
        sign = Mathf.sign(value)
        return sign * pow(abs(value) / absmax, gamma) * absmax if absmax != 0 else 0.0

    @staticmethod
    def barycentric(a: float, b: float, c: float, u: float, v: float) -> float:
        """Returns a barycentric interpolation between three values."""
        return a + (b - a) * u + (c - a) * v
    
class Color32:
    _1o255 = 1.0 / 255.0
    
    red: "Color32"
    green: "Color32"
    blue: "Color32"
    white: "Color32"
    black: "Color32"
    
    def __init__(self, r: (str | float), g: float = 0, b: float = 0, a: float = 1):
        if isinstance(r, str):
            hex_color = r.lstrip("#")
            if len(hex_color) == 6:
                self.r = int(hex_color[0:2], 16) / 255.0
                self.g = int(hex_color[2:4], 16) / 255.0
                self.b = int(hex_color[4:6], 16) / 255.0
                self.a = 1.0
            elif len(hex_color) == 8:
                self.r = int(hex_color[0:2], 16) / 255.0
                self.g = int(hex_color[2:4], 16) / 255.0
                self.b = int(hex_color[4:6], 16) / 255.0
                self.a = int(hex_color[6:8], 16) / 255.0
            else:
                Console.error("Invalid hex color string format. Use #RRGGBB or #RRGGBBAA.")
                self.r, self.g, self.b, self.a = 0.0, 0.0, 0.0, 1.0
        else:
            if r > 1.0 or g > 1.0 or b > 1.0 or a > 1.0:
                self.r = Mathf.clamp01(r * Color32._1o255)
                self.g = Mathf.clamp01(g * Color32._1o255)
                self.b = Mathf.clamp01(b * Color32._1o255)
                self.a = Mathf.clamp01(a)
            else:
                self.r = Mathf.clamp01(r)
                self.g = Mathf.clamp01(g)
                self.b = Mathf.clamp01(b)
                self.a = Mathf.clamp01(a)


    def getColor(self) -> tuple[float, float, float, float]:
        """Returns the color as a tuple (r, g, b) with values between 0.0 and 1.0."""
        return (self.r, self.g, self.b, self.a)
    
    @staticmethod
    def lerp(c1: "Color32", c2: "Color32", t: float) -> "Color32":
        t = Mathf.clamp01(t)
        return Color32(
            c1.r + (c2.r - c1.r) * t,
            c1.g + (c2.g - c1.g) * t,
            c1.b + (c2.b - c1.b) * t,
            c1.a + (c2.a - c1.a) * t
        )
        
Color32.red = Color32(255, 0, 0, 1)
Color32.green = Color32(0,255,0,1)
Color32.blue = Color32(0,0,255,1)
Color32.white = Color32(255,255,255,1)
Color32.black = Color32(0,0,0,1)
import OpenGL.GL as opengl
import numpy as np
from typing import Optional

from AuroraEngine.essentials import GameObject, Component, Console, Vector2, Color32, Mathf, System
from AuroraEngine.graphics.shaders import Shader



class VBO_SpriteRenderer(Component):

    # Class-level VBO/VAO/Shader Program for all VBO_SpriteRenders
    _program_id: int = 0
    _vao_id: int = 0
    _vbo_id: int = 0
    _model_loc: int = -1
    _projection_loc: int = -1
    _color_loc: int = -1

    _initialized_gl_resources = False

    def __init__(self, gameObject: GameObject, sprite: str = "rectangle", color: Color32 = Color32(255, 255, 255), custom_size: Optional[Vector2] = None):
        super().__init__(gameObject)
        self.sprite = sprite
        self.color = color
        self.custom_size = custom_size

        if not VBO_SpriteRenderer._initialized_gl_resources:
            self._setup_gl_resources()
            VBO_SpriteRenderer._initialized_gl_resources = True

    @classmethod
    def _setup_gl_resources(cls):
        Console.log("VBO_SpriteRender: Setting up OpenGL resources (VBOs, VAOs, Shaders)...")

        cls._program_id = Shader.create_program(Shader.VERTEX_SHADER_SOURCE, Shader.FRAGMENT_SHADER_SOURCE)


        cls._model_loc = opengl.glGetUniformLocation(cls._program_id, "model")
        cls._projection_loc = opengl.glGetUniformLocation(cls._program_id, "projection")
        cls._color_loc = opengl.glGetUniformLocation(cls._program_id, "spriteColor")
        if cls._model_loc == -1 or cls._projection_loc == -1 or cls._color_loc == -1:
            Console.error("Failed to get uniform locations for VBO_SpriteRender shader!")
            raise RuntimeError("Shader uniform location error.")

        quad_vertices = np.array([
            -0.5, -0.5,  # Bottom-left
             0.5, -0.5,  # Bottom-right
             0.5,  0.5,  # Top-right
            -0.5,  0.5   # Top-left
        ], dtype=np.float32)

        cls._vao_id = opengl.glGenVertexArrays(1)
        opengl.glBindVertexArray(cls._vao_id)

        cls._vbo_id = opengl.glGenBuffers(1)
        opengl.glBindBuffer(opengl.GL_ARRAY_BUFFER, cls._vbo_id)
        opengl.glBufferData(opengl.GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, opengl.GL_STATIC_DRAW)
        opengl.glVertexAttribPointer(0, 2, opengl.GL_FLOAT, opengl.GL_FALSE, 2 * quad_vertices.itemsize, None)
        opengl.glEnableVertexAttribArray(0)
        opengl.glBindBuffer(opengl.GL_ARRAY_BUFFER, 0)
        opengl.glBindVertexArray(0)
        Console.log("VBO_SpriteRender: OpenGL resources setup complete.")


    def start(self):
        pass

    def update(self):
        self.draw(*self.gameObject.transform, color=self.color) # type: ignore[arg-type]
        pass

    def draw(self, position: Vector2, rotation: float, scale: Vector2, color: Color32):
        opengl.glUseProgram(VBO_SpriteRenderer._program_id)



        model_matrix = np.array([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32).reshape(4,4)

        scale_matrix = np.array([
            scale.x, 0.0, 0.0, 0.0,
            0.0, scale.y, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32).reshape(4,4)
        model_matrix = np.dot(model_matrix, scale_matrix)


        angle_rad = Mathf.deg2rad(rotation)
        cos_theta = Mathf.cos(angle_rad)
        sin_theta = Mathf.sin(angle_rad)
        rotation_matrix = np.array([
            cos_theta, -sin_theta, 0.0, 0.0,
            sin_theta,  cos_theta, 0.0, 0.0,
            0.0,        0.0,       1.0, 0.0,
            0.0,        0.0,       0.0, 1.0
        ], dtype=np.float32).reshape(4,4)
        model_matrix = np.dot(model_matrix, rotation_matrix)


        translation_matrix = np.array([
            1.0, 0.0, 0.0, position.x,
            0.0, 1.0, 0.0, position.y,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32).reshape(4,4)
        model_matrix = np.dot(model_matrix, translation_matrix)



        left, right, bottom, top, near, far = -10.0, 10.0, -10.0, 10.0, -1.0, 1.0
        projection_matrix = np.array([
            2.0/(right-left), 0.0, 0.0, -(right+left)/(right-left),
            0.0, 2.0/(top-bottom), 0.0, -(top+bottom)/(top-bottom),
            0.0, 0.0, -2.0/(far-near), -(far+near)/(far-near),
            0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32).reshape(4,4)


        opengl.glUniformMatrix4fv(VBO_SpriteRenderer._model_loc, 1, opengl.GL_TRUE, model_matrix)
        opengl.glUniformMatrix4fv(VBO_SpriteRenderer._projection_loc, 1, opengl.GL_TRUE, projection_matrix)

        r, g, b, a = color.getColor()
        opengl.glUniform4f(VBO_SpriteRenderer._color_loc, r, g, b, a)

        opengl.glBindVertexArray(VBO_SpriteRenderer._vao_id)
        opengl.glDrawArrays(opengl.GL_QUADS, 0, 4)

        opengl.glBindVertexArray(0)
        opengl.glUseProgram(0)
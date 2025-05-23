import OpenGL.GL as opengl
from ..essentials import Console


class Shader:

    VERTEX_SHADER_SOURCE = """
    #version 330 core
    layout (location = 0) in vec2 aPos; // Vertex position

    uniform mat4 model; // Model matrix (position, rotation, scale)
    uniform mat4 projection; // Projection matrix (orthographic)

    void main()
    {
        gl_Position = projection * model * vec4(aPos, 0.0, 1.0);
    }
    """
    FRAGMENT_SHADER_SOURCE = """
    #version 330 core
    out vec4 FragColor;

    uniform vec4 spriteColor; // Color passed from Python

    void main()
    {
        FragColor = spriteColor;
    }
    """

    @staticmethod
    def compile_shader(source: str, shader_type: int) -> int: 
        shader = opengl.glCreateShader(shader_type)
        opengl.glShaderSource(shader, source)
        opengl.glCompileShader(shader)

        if not opengl.glGetShaderiv(shader, opengl.GL_COMPILE_STATUS):
            info_log = opengl.glGetShaderInfoLog(shader).decode('utf-8')
            shader_type_str = "VERTEX" if shader_type == opengl.GL_VERTEX_SHADER else "FRAGMENT"
            Console.error(f"Error compiling {shader_type_str} shader:\n{info_log}")
            opengl.glDeleteShader(shader)
            raise RuntimeError(f"Shader compilation failed: {info_log}")
        return shader # type: ignore[arg-type]

    @staticmethod
    def create_program(vertex_shader_source: str, fragment_shader_source: str) -> int:
        vertex_shader = Shader.compile_shader(vertex_shader_source, opengl.GL_VERTEX_SHADER)
        fragment_shader = Shader.compile_shader(fragment_shader_source, opengl.GL_FRAGMENT_SHADER)

        program = opengl.glCreateProgram()
        opengl.glAttachShader(program, vertex_shader)
        opengl.glAttachShader(program, fragment_shader)
        opengl.glLinkProgram(program)

        if not opengl.glGetProgramiv(program, opengl.GL_LINK_STATUS):
            info_log = opengl.glGetProgramInfoLog(program).decode('utf-8')
            Console.error(f"Error linking shader program:\n{info_log}")
            opengl.glDeleteProgram(program)
            opengl.glDeleteShader(vertex_shader)
            opengl.glDeleteShader(fragment_shader)
            raise RuntimeError(f"Shader linking failed: {info_log}")

        opengl.glDeleteShader(vertex_shader)
        opengl.glDeleteShader(fragment_shader)
        return program # type: ignore[arg-type]

from ..essentials import Component, GameObject, Vector2, Color32, Mathf, System, Console
from ..components.VBOSpriteRenderer import VBO_SpriteRenderer
import random
import OpenGL.GL as opengl
from typing import Optional

class Particle:
    def __init__(self,
            position: Vector2,
            velocity: Vector2,
            start_lifetime: float,
            start_size: float,
            end_size: float,
            start_color: Color32,
            end_color: Color32,
            start_rotation: float = 0.0,
            angular_velocity: float = 0.0):
        self.position = position
        self.velocity = velocity
        self.total_lifetime = start_lifetime
        self.current_life = 0.0
        self.start_size = start_size
        self.end_size = end_size
        self.start_color = start_color
        self.end_color = end_color
        self.rotation = start_rotation
        self.angular_velocity = angular_velocity
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            return

        self.current_life += System.deltaTime

        if self.current_life >= self.total_lifetime:
            self.is_alive = False
            return

        self.position += self.velocity * System.deltaTime

        self.rotation += self.angular_velocity * System.deltaTime


    def get_current_state(self) -> tuple[Vector2, float, Vector2, Color32]:
        """Returns the current position, rotation, scale, and color for rendering."""
        t = self.current_life / self.total_lifetime

        current_size = Mathf.lerp(self.start_size, self.end_size, t)
        current_scale = Vector2(current_size, current_size)

        current_color = Color32.lerp(self.start_color, self.end_color, t)

        return self.position, self.rotation, current_scale, current_color
    



class ParticleSystem(Component):
    def __init__(self, gameObject: GameObject,
        max_particles: int = 100,
        emission_rate: float = 10.0, # particles per second
        duration: float = 5.0, # seconds
        looping: bool = True,
        start_delay: float = 0.0,
        start_lifetime_min: float = 1.0,
        start_lifetime_max: float = 3.0,
        start_speed_min: float = 1.0,
        start_speed_max: float = 5.0,
        start_size_min: float = 0.1,
        start_size_max: float = 0.3,
        end_size_min: float = 0.01,
        end_size_max: float = 0.05,
        start_color_min: Color32 = Color32(255, 255, 255, 255), # White
        start_color_max: Color32 = Color32(255, 255, 255, 255),
        end_color_min: Color32 = Color32(255, 255, 255, 0), # Transparent White
        end_color_max: Color32 = Color32(255, 255, 255, 0),
        start_rotation_min: float = 0.0,
        start_rotation_max: float = 360.0,
        angular_velocity_min: float = -50.0, # degrees per second
        angular_velocity_max: float = 50.0,
        shape: str = "cone", # "point", "circle", "cone"
        cone_angle: float = 30.0, # degrees
        cone_direction: float = 0.0, # degrees
        sprite_type: str = "rectangle",
        gravity_modifier: float = 0.0
        ):
        super().__init__(gameObject)

        self.max_particles = max_particles
        self.emission_rate = emission_rate
        self.duration = duration
        self.looping = looping
        self.start_delay = start_delay

        self.start_lifetime_min = start_lifetime_min
        self.start_lifetime_max = start_lifetime_max
        self.start_speed_min = start_speed_min
        self.start_speed_max = start_speed_max
        self.start_size_min = start_size_min
        self.start_size_max = start_size_max
        self.end_size_min = end_size_min
        self.end_size_max = end_size_max
        self.start_color_min = start_color_min
        self.start_color_max = start_color_max
        self.end_color_min = end_color_min
        self.end_color_max = end_color_max
        self.start_rotation_min = start_rotation_min
        self.start_rotation_max = start_rotation_max
        self.angular_velocity_min = angular_velocity_min
        self.angular_velocity_max = angular_velocity_max
        self.gravity_modifier = gravity_modifier

        self.shape = shape
        self.cone_angle = cone_angle
        self.cone_direction = cone_direction

        self.sprite_type = sprite_type

        self.particles: list[Particle] = []
        self.time_since_last_emission = 0.0
        self.emission_accumulator = 0.0
        self.current_duration_time = 0.0
        self.has_started = False
        self.delay_timer = 0.0

        self.sprite_renderer: Optional[VBO_SpriteRenderer] = None

    def start(self):
        self.sprite_renderer = self.gameObject.getComponent(VBO_SpriteRenderer) # type: ignore[arg-type]
        if not self.sprite_renderer:
            self.sprite_renderer = self.gameObject.addComponent(VBO_SpriteRenderer, sprite=self.sprite_type) # type: ignore[arg-type]
            Console.warn(f"ParticleSystem on '{self.gameObject.name}' added a default SpriteRenderer as none was found.")
        else:
            self.sprite_renderer.sprite = self.sprite_type


    def update(self):
        if not self.has_started:
            self.delay_timer += System.deltaTime
            if self.delay_timer >= self.start_delay:
                self.has_started = True
            return

        if not self.looping and self.current_duration_time >= self.duration:
            # don't delete, it is to keep particles from despawning
            pass
        else:
            self.current_duration_time += System.deltaTime
            self.emit_particles()

        self.update_particles()
        self.render_particles()

    def emit_particles(self):
        if len(self.particles) >= self.max_particles:
            return

        self.emission_accumulator += self.emission_rate * System.deltaTime
        num_to_emit = Mathf.floor(self.emission_accumulator)
        self.emission_accumulator -= num_to_emit

        for _ in range(int(num_to_emit)):
            if len(self.particles) >= self.max_particles:
                break
            self._create_single_particle()

    def _create_single_particle(self):
        start_pos = self.gameObject.transform.position

        lifetime = random.uniform(self.start_lifetime_min, self.start_lifetime_max)

        speed = random.uniform(self.start_speed_min, self.start_speed_max)

        direction_rad = Mathf.rad2deg(self.gameObject.transform.rotation + self.cone_direction)
        if self.shape == "cone":
            half_angle_rad = Mathf.rad2deg(self.cone_angle / 2.0)
            random_angle_offset = random.uniform(-half_angle_rad, half_angle_rad)
            direction_rad += random_angle_offset
        elif self.shape == "circle":
            direction_rad = random.uniform(0, 2 * Mathf.PI)

        velocity = Vector2(Mathf.cos(direction_rad), Mathf.sin(direction_rad)) * speed

        start_size = random.uniform(self.start_size_min, self.start_size_max)
        end_size = random.uniform(self.end_size_min, self.end_size_max)

        start_color = Color32.lerp(self.start_color_min, self.start_color_max, random.random())
        end_color = Color32.lerp(self.end_color_min, self.end_color_max, random.random())

        start_rotation = random.uniform(self.start_rotation_min, self.start_rotation_max)
        angular_velocity = random.uniform(self.angular_velocity_min, self.angular_velocity_max)


        new_particle = Particle(start_pos, velocity, lifetime,
                                start_size, end_size,
                                start_color, end_color,
                                start_rotation, angular_velocity)
        self.particles.append(new_particle)

    def update_particles(self):
        alive_particles = []
        for particle in self.particles:
            particle.update()
            if self.gravity_modifier != 0:
                particle.velocity.y -= self.gravity_modifier * System.deltaTime
            if particle.is_alive:
                alive_particles.append(particle)
        self.particles = alive_particles

    def render_particles(self):
        if self.sprite_renderer:
            opengl.glEnable(opengl.GL_BLEND)
            opengl.glBlendFunc(opengl.GL_SRC_ALPHA, opengl.GL_ONE_MINUS_SRC_ALPHA)

            for particle in self.particles:
                pos, rot, scale, color = particle.get_current_state()
                self.sprite_renderer.draw(pos, rot, scale, color)
            
            opengl.glDisable(opengl.GL_BLEND)
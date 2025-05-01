import pygame
from PIL import Image


class Explosion:
    def __init__(self, position):
        self.frames = []
        self.load_gif_frames("assets/explosion.gif")  # шлях до гіфки
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=position)
        self.frame_rate = 4  # Чим менше число - тим швидше анімація
        self.frame_counter = 0
        self.finished = False

    def load_gif_frames(self, gif_path, scale=0.55):
        pil_image = Image.open(gif_path)
        total_frames = pil_image.n_frames
        frames_to_load = total_frames // 2  # Завантажити тільки першу половину кадрів

        for frame in range(frames_to_load):
            pil_image.seek(frame)
            frame_image = pil_image.convert('RGBA')
            mode = frame_image.mode
            size = frame_image.size
            data = frame_image.tobytes()

            py_image = pygame.image.fromstring(data, size, mode)

            new_width = int(py_image.get_width() * scale)
            new_height = int(py_image.get_height() * scale)
            py_image = pygame.transform.scale(py_image, (new_width, new_height))

            self.frames.append(py_image)

    def update(self):
        if self.finished:
            return

        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.index += 1
            self.frame_counter = 0
            if self.index >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.index]

    def draw(self, surface):
        if not self.finished:
            surface.blit(self.image, self.rect.topleft)

    def is_finished(self):
        return self.finished

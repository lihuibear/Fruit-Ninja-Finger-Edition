import init
import pygame
class Apple(pygame.sprite.Sprite):
    def __init__(self, speedx, speedy, image):
        super(Apple, self).__init__()
        self.speedx = speedx
        self.speedy = speedy
        self.image = image
        self.rect = self.image.get_rect().move(50, 100)  # 初始位置

    def update(self):
        self.rect.x += self.speedx
        self.rect.y -= self.speedy

        if self.rect.y < 0:
            self.speedy = -self.speedy

    def draw(self, window):
        window.blit(self.image, self.rect)

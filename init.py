import time
from idlelib import window
import pygame
import cv2
import mediapipe as mp
import random
from apple import *
from orbit import *


index_finger_tip_x = 0
index_finger_tip_y = 0
# 帧率
frames =  200
# 出水果速率，越小越快
fruit_num = 20

# 初始化手部识别模型.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# 开启摄像头捕获视频.
cap = cv2.VideoCapture(0)

# 设置新的分辨率值
desired_width = 1280
desired_height = 720
ph = lambda y: desired_height * y
# 设置捕获对象的分辨率（宽度）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)

# 设置捕获对象的分辨率（高度）
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
orbit = []

# 硬件初始化
pygame.init()

#载入音频
collision_sound = pygame.mixer.Sound("./video/3.wav")

# 载入不同水果的图片
apple_img = pygame.image.load("img/apple.png")
banana_img = pygame.image.load("img/banana.png")
peach_img = pygame.image.load("img/peach.png")
sandia_img = pygame.image.load("img/sandia.png")
basaha_img = pygame.image.load("img/basaha.png")

# 背景

background = pygame.image.load("img/background.jpg")
background = pygame.transform.scale(background, (1280, 720))

# 创建不同水果的实例
apples_info = [
    {"speedx": 8, "speedy": 3, "image": apple_img},
    {"speedx": 3, "speedy": 2, "image": banana_img},
    {"speedx": 5, "speedy": 4, "image": peach_img},
    {"speedx": 6, "speedy": 2, "image": sandia_img},
    {"speedx": 5, "speedy": 2, "image": basaha_img}
]

all_apple = pygame.sprite.Group()
for info in apples_info:
    app = Apple(info["speedx"], info["speedy"], info["image"])
    all_apple.add(app)

# 创建手指轨迹对象的实例
orbit_drawer = Orbit(window)

# 设置字体和初始分数
font = pygame.font.Font(None, 36)
score = 0


window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.flip()

clock.tick(frames)

running = True
cnt = 0
zuobiao = []
collided_apples = []
show_split = False
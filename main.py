from init import *
from apple import Apple
def calculate_line_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        points.append((int(round(x)), int(round(y))))
        x += x_increment
        y += y_increment

    return points

while running:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("你摄像头寄了！")
            continue
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_tip_x = int(index_finger_tip.x * image.shape[1])
                index_finger_tip_y = int(index_finger_tip.y * image.shape[0])

                cv2.circle(image, (index_finger_tip_x, index_finger_tip_y), 5, (255, 0, 255), -1)

                # print(f"食指指尖坐标: (x: {index_finger_tip_x}, y: {index_finger_tip_y})")
        zuobiao.append((index_finger_tip_x,index_finger_tip_y))
        orbit.append(time.time_ns() / 1000000)

        cv2.imshow('MediaPipe Hands', image)

        cnt += 1
        if cnt == fruit_num:
            speedx = random.uniform(3, 8)
            speedy = random.uniform(2, 5)
            app = Apple(speedx, speedy, random.choice([apple_img, banana_img, peach_img, sandia_img,basaha_img]))
            all_apple.add(app)
            cnt = 0

        now = time.time_ns() / 1000000
        for i in range(1, len(orbit)):
            pygame.draw.line(window, (255, 255, 255),
                             zuobiao[i - 1], zuobiao[i],
                             int(ph(0.0003) * (orbit[i] + 100 - now))
                             )

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites = all_apple.sprites()
        for app in all_sprites:
            if app.rect.collidepoint((index_finger_tip_x, index_finger_tip_y)):
                collided_apples.append(app)
                score += 1
                collision_sound.play()

        for app in collided_apples:
            app.kill()
            # print("手指和水果碰撞得分！")
            show_split = True


        window.blit(background, (0, 0))

        orbit_drawer.draw(index_finger_tip_x, index_finger_tip_y)

        all_apple.update()
        all_apple.draw(window)

        score_text = font.render(f"score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))

        clock.tick(frames)

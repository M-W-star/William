import pygame
import random

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 5
ROAD_SPEED = 3
OBSTACLE_FREQ = 25  # 障碍物生成频率（值越小生成越快）

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# 初始化游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("简易赛车游戏")
clock = pygame.time.Clock()

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT-100))
        self.speed = PLAYER_SPEED

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 100:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH-100:
            self.rect.x += self.speed

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randint(50,100), 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(
            center=(random.randint(150, WIDTH-150), -20)
        )
        self.speed = ROAD_SPEED + random.randint(1,3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def game_loop():
    player = PlayerCar()
    all_sprites = pygame.sprite.Group(player)
    obstacles = pygame.sprite.Group()
    
    score = 0
    running = True
    
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 生成障碍物
        if random.randint(1, OBSTACLE_FREQ) == 1:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        # 更新状态
        keys = pygame.key.get_pressed()
        player.update(keys)
        obstacles.update()
        
        # 碰撞检测
        if pygame.sprite.spritecollide(player, obstacles, False):
            running = False
            
        # 得分计算
        score += 1

        # 画面渲染
        screen.fill(GRAY)  # 道路颜色
        
        # 绘制道路标线
        pygame.draw.rect(screen, WHITE, (95, 0, 10, HEIGHT))  # 左侧护栏
        pygame.draw.rect(screen, WHITE, (WIDTH-105, 0, 10, HEIGHT))  # 右侧护栏
        
        all_sprites.draw(screen)
        
        # 显示得分
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score//10}", True, BLACK)
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    # 游戏结束界面
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over!", True, RED)
    screen.blit(text, (WIDTH//2-140, HEIGHT//2-40))
    pygame.display.flip()
    pygame.time.wait(2000)
    
    pygame.quit()

if __name__ == "__main__":
    game_loop()

import pygame

class Road:
    """Дорога, которая движется вниз"""
    
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.road_width = 400
        self.base_speed = 5
        self.current_speed = 5
        self.line_offset = 0
        
        # Цвета
        self.grass_color = (0, 180, 0)
        self.road_color = (60, 60, 60)
        self.line_color = (255, 255, 0)
    
    def update(self, player_speed=5):
        """Двигаем разметку вниз с учётом скорости игрока"""
        self.current_speed = player_speed
        self.line_offset += self.current_speed
        if self.line_offset > 60:
            self.line_offset = 0
    
    def draw(self, screen):
        """Рисуем дорогу"""
        # Трава
        screen.fill(self.grass_color)
        
        # Асфальт
        road_x = (self.width - self.road_width) // 2
        pygame.draw.rect(screen, self.road_color, 
                        (road_x, 0, self.road_width, self.height))
        
        # Разметка (движется!)
        for y in range(-60, self.height, 60):
            line_y = y + self.line_offset
            pygame.draw.rect(screen, self.line_color,
                           (self.width // 2 - 5, line_y, 10, 30))
    
    def get_left_edge(self):
        """Левая граница дороги"""
        return (self.width - self.road_width) // 2
    
    def get_right_edge(self):
        """Правая граница дороги"""
        return (self.width + self.road_width) // 2
    
    def get_current_speed(self):
        """Получить текущую скорость дороги"""
        return self.current_speed

# ===== ДЕМО-РЕЖИМ =====
if __name__ == "__main__":
    """Демонстрация класса Road - дорога движется!"""
    
    import pygame
    
    # Инициализация
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🛣️ ДЕМО: Класс Road - Дорога")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    font_large = pygame.font.SysFont(None, 36)
    
    # Создаём дорогу
    road = Road(800, 600)
    
    # Параметры для демо
    speed = 5
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Управление скоростью
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            speed = min(speed + 0.2, 15)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            speed = max(speed - 0.2, 1)
        
        # Обновление дороги
        road.update(speed)
        
        # Рисование
        road.draw(screen)
        
        # Заголовок
        title = font_large.render("ДЕМО: Класс Road 🛣️", True, (255, 255, 255))
        title_bg = pygame.Surface((title.get_width() + 20, title.get_height() + 10))
        title_bg.fill((0, 0, 0))
        title_bg.set_alpha(180)
        screen.blit(title_bg, (5, 5))
        screen.blit(title, (10, 10))
        
        # Параметры дороги
        params = [
            f"Ширина дороги: {road.road_width} px",
            f"Скорость движения: {int(speed * 10)} км/ч",
            f"Смещение разметки: {int(road.line_offset)}",
            f"Левая граница: {road.get_left_edge()}",
            f"Правая граница: {road.get_right_edge()}",
            f"Текущая скорость: {road.get_current_speed()}",
        ]
        
        y_offset = 60
        for param in params:
            bg = pygame.Surface((400, 25))
            bg.fill((0, 0, 0))
            bg.set_alpha(180)
            screen.blit(bg, (5, y_offset - 2))
            surface = font.render(param, True, (255, 255, 255))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        # Управление
        controls = [
            "УПРАВЛЕНИЕ:",
            "↑ W - Увеличить скорость",
            "↓ S - Уменьшить скорость",
            "",
            "Разметка движется вниз!",
        ]
        
        y_offset = 450
        for text in controls:
            bg = pygame.Surface((350, 25))
            bg.fill((0, 0, 0))
            bg.set_alpha(180)
            screen.blit(bg, (5, y_offset - 2))
            surface = font.render(text, True, (255, 255, 0))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
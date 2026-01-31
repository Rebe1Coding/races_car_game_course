import pygame
import random
import os

class ObstacleCar:
    """Встречная машина-препятствие"""
    
    def __init__(self, x, y, speed=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 40
        self.height = 80
        self.image = None
        self.passed = False  # Флаг для подсчёта очков
        
        # Загружаем случайное изображение из папки imgs/obstacles/
        self._load_random_image()
    
    def _load_random_image(self):
        """Загружаем случайное изображение машины"""
        try:
            # Путь к папке с изображениями встречных машин
            obstacles_folder = "imgs/obstacles/"
            
            # Проверяем существование папки
            if os.path.exists(obstacles_folder):
                # Получаем список всех файлов изображений
                image_files = [f for f in os.listdir(obstacles_folder) 
                             if f.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'))]
                
                if image_files:
                    # Выбираем случайный файл
                    random_image = random.choice(image_files)
                    image_path = os.path.join(obstacles_folder, random_image)
                    
                    # Загружаем и масштабируем
                    self.image = pygame.image.load(image_path)
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
                    return
            
            # Если не получилось загрузить - создаём простую машинку
            self._create_simple_car()
        except Exception as e:
            # При любой ошибке - создаём простую машинку
            print(f"Ошибка загрузки изображения: {e}")
            self._create_simple_car()
    
    def _create_simple_car(self):
        """Создаём простое изображение машины"""
        # Случайный цвет
        colors = [
            (0, 0, 255),    # Синий
            (255, 165, 0),  # Оранжевый
            (128, 0, 128),  # Фиолетовый
            (0, 255, 255),  # Голубой
            (255, 192, 203) # Розовый
        ]
        color = random.choice(colors)
        
        # Создаём поверхность
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Рисуем машинку
        # Кузов
        pygame.draw.rect(self.image, color, (10, 20, 40, 50))
        # Крыша
        dark = tuple(c // 2 for c in color)
        pygame.draw.rect(self.image, dark, (15, 10, 30, 25))
        # Колёса
        pygame.draw.circle(self.image, (0, 0, 0), (18, 25), 6)
        pygame.draw.circle(self.image, (0, 0, 0), (42, 25), 6)
        pygame.draw.circle(self.image, (0, 0, 0), (18, 65), 6)
        pygame.draw.circle(self.image, (0, 0, 0), (42, 65), 6)
    
    def update(self):
        """Обновляем позицию - движемся вниз"""
        self.y += self.speed
    
    def draw(self, screen):
        """Рисуем машину"""
        if self.image:
            screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
    
    def is_off_screen(self, screen_height):
        """Проверяем, вышла ли машина за экран"""
        return self.y > screen_height + 50
    
    def get_rect(self):
        """Получаем прямоугольник для проверки столкновений"""
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

# ===== ДЕМО-РЕЖИМ =====
if __name__ == "__main__":
    """Демонстрация класса ObstacleCar - встречные машины!"""
    
    import pygame
    
    # Инициализация
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🚙 ДЕМО: Класс ObstacleCar - Препятствия")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    font_large = pygame.font.SysFont(None, 36)
    
    # Цвета
    grass_color = (0, 180, 0)
    road_color = (60, 60, 60)
    
    # Создаём несколько машин для демонстрации
    obstacles = []
    spawn_timer = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Создаём новую машину по нажатию пробела
                    x = random.randint(250, 550)
                    obstacle = ObstacleCar(x, -50, speed=random.randint(3, 8))
                    obstacles.append(obstacle)
        
        # Автоматическая генерация машин
        spawn_timer += 1
        if spawn_timer > 90:
            x = random.randint(250, 550)
            obstacle = ObstacleCar(x, -50, speed=random.randint(3, 8))
            obstacles.append(obstacle)
            spawn_timer = 0
        
        # Обновление всех машин
        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.is_off_screen(600):
                obstacles.remove(obstacle)
        
        # Рисование
        screen.fill(grass_color)
        
        # Рисуем дорогу
        pygame.draw.rect(screen, road_color, (200, 0, 400, 600))
        
        # Разметка
        for y in range(0, 600, 60):
            pygame.draw.rect(screen, (255, 255, 0), (395, y, 10, 30))
        
        # Рисуем все машины
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Заголовок
        title = font_large.render("ДЕМО: Класс ObstacleCar 🚙", True, (255, 255, 255))
        title_bg = pygame.Surface((title.get_width() + 20, title.get_height() + 10))
        title_bg.fill((0, 0, 0))
        title_bg.set_alpha(200)
        screen.blit(title_bg, (5, 5))
        screen.blit(title, (10, 10))
        
        # Параметры
        params = [
            f"Количество машин: {len(obstacles)}",
            f"Таймер создания: {90 - spawn_timer}",
        ]
        
        y_offset = 60
        for param in params:
            bg = pygame.Surface((350, 25))
            bg.fill((0, 0, 0))
            bg.set_alpha(200)
            screen.blit(bg, (5, y_offset - 2))
            surface = font.render(param, True, (255, 255, 255))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        # Показываем параметры каждой машины
        if obstacles:
            y_offset += 10
            surface = font.render("ПАРАМЕТРЫ МАШИН:", True, (255, 255, 0))
            bg = pygame.Surface((350, 25))
            bg.fill((0, 0, 0))
            bg.set_alpha(200)
            screen.blit(bg, (5, y_offset - 2))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
            
            for i, obs in enumerate(obstacles[:5]):  # Показываем только первые 5
                text = f"Машина {i+1}: X={int(obs.x)} Y={int(obs.y)} Speed={obs.speed}"
                bg = pygame.Surface((500, 20))
                bg.fill((0, 0, 0))
                bg.set_alpha(200)
                screen.blit(bg, (5, y_offset - 2))
                surface = font.render(text, True, (200, 200, 200))
                screen.blit(surface, (10, y_offset))
                y_offset += 20
        
        # Управление
        controls = [
            "УПРАВЛЕНИЕ:",
            "SPACE - Создать новую машину",
            "",
            "Машины автоматически создаются",
            "и двигаются вниз!",
        ]
        
        y_offset = 450
        for text in controls:
            bg = pygame.Surface((400, 25))
            bg.fill((0, 0, 0))
            bg.set_alpha(200)
            screen.blit(bg, (5, y_offset - 2))
            surface = font.render(text, True, (255, 255, 0))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
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
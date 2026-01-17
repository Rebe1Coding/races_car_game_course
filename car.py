import pygame
import numpy as np

class Car:
    """Машинка игрока"""
    
    def __init__(self, x, y, color=(255, 0, 0), number=777):
        self.x = x
        self.y = y
        self.color = color
        self.number = number
        self.image = None
        self.width = 50
        self.height = 50
        
        # Параметры движения
        self.base_speed = 5  # Базовая скорость движения влево/вправо
        self.current_speed = 0  # Текущая скорость игрока
        self.max_speed = 15  # Максимальная скорость
        self.min_speed = 3   # Минимальная скорость
        self.acceleration = 0.3  # Ускорение
        self.deceleration = 0.5  # Торможение
        
        pygame.mixer.init()
        self.beep_sound = None
        self._load_sound()
        
        self.headlights_on = False
        
        # Пробуем загрузить картинку
        try:
            self.image = pygame.image.load("imgs/result.png")
            self.image = pygame.transform.scale(self.image, (80, 80))
        except:
            pass
    
    def _load_sound(self):
        """Загружаем звук сигнала"""
        try:
            self.beep_sound = pygame.mixer.Sound("sounds/beep2.wav")
        except:
            self._create_beep_sound()
    
    def _create_beep_sound(self):
        """Создаём звук сигнала если нет файла"""
        try:
            sample_rate = 22050
            duration = 0.2
            frequency = 500
            
            samples = np.sin(2 * np.pi * frequency * 
                           np.linspace(0, duration, int(sample_rate * duration)))
            samples = (samples * 32767).astype(np.int16)
            stereo_samples = np.column_stack((samples, samples))
            
            self.beep_sound = pygame.sndarray.make_sound(stereo_samples)
        except:
            pass
    
    def accelerate(self):
        """Ускорение"""
        self.current_speed = min(self.current_speed + self.acceleration, self.max_speed)
    
    def brake(self):
        """Торможение"""
        self.current_speed = max(self.current_speed - self.deceleration, self.min_speed)
    
    def update_speed(self):
        """Обновление скорости (естественное замедление)"""
        if self.current_speed > self.min_speed:
            self.current_speed -= 0.05
            if self.current_speed < self.min_speed:
                self.current_speed = self.min_speed
    
    def get_speed(self):
        """Получить текущую скорость для передачи дороге"""
        return self.current_speed
    
    def draw(self, screen):
        """Рисуем машинку"""
        if self.image:
            screen.blit(self.image, (self.x - 40, self.y - 40))
        else:
            self._draw_simple(screen)
        
        if self.headlights_on:
            self._draw_headlights(screen)
    
    def _draw_simple(self, screen):
        """Простое рисование машинки"""
        pygame.draw.rect(screen, self.color, 
                        (self.x - 25, self.y - 20, 50, 40))
        
        dark = tuple(c // 2 for c in self.color)
        pygame.draw.rect(screen, dark, 
                        (self.x - 20, self.y - 30, 40, 20))
        
        black = (0, 0, 0)
        pygame.draw.circle(screen, black, (self.x - 18, self.y - 15), 6)
        pygame.draw.circle(screen, black, (self.x + 18, self.y - 15), 6)
        pygame.draw.circle(screen, black, (self.x - 18, self.y + 15), 6)
        pygame.draw.circle(screen, black, (self.x + 18, self.y + 15), 6)
        
        if self.headlights_on:
            light_color = (255, 255, 100)
        else:
            light_color = (255, 255, 0)
        
        pygame.draw.circle(screen, light_color, (self.x, self.y - 25), 4)
    
    def _draw_headlights(self, screen):
        """Рисуем свет от фар"""
        light_color = (255, 255, 150, 60)
        
        points_left = [
            (self.x - 10, self.y - 25),
            (self.x - 60, self.y - 200),
            (self.x + 10, self.y - 200)
        ]
        
        points_right = [
            (self.x + 10, self.y - 25),
            (self.x - 10, self.y - 200),
            (self.x + 60, self.y - 200)
        ]
        
        pygame.draw.polygon(screen, light_color, points_left)
        pygame.draw.polygon(screen, light_color, points_right)
    
    def move_left(self, speed=5):
        """Движение влево"""
        self.x -= speed
    
    def move_right(self, speed=5):
        """Движение вправо"""
        self.x += speed
    
    def keep_on_road(self, left_edge, right_edge):
        """Не даём выехать за дорогу"""
        if self.x < left_edge + 25:
            self.x = left_edge + 25
        if self.x > right_edge - 25:
            self.x = right_edge - 25
    
    def beep(self):
        """Сигналим!"""
        if self.beep_sound:
            self.beep_sound.play()
        else:
            print("БИП-БИП! 🚗")
    
    def toggle_headlights(self):
        """Включить/выключить фары"""
        self.headlights_on = not self.headlights_on
    
    def get_rect(self):
        """Получаем прямоугольник для проверки столкновений"""
        return pygame.Rect(self.x - 25, self.y - 25, 50, 50)
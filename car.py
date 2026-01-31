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
        self.base_speed = 100  # Базовая скорость движения влево/вправо
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

# ===== ДЕМО-РЕЖИМ =====
if __name__ == "__main__":
    """Демонстрация класса Car - можно управлять машинкой!"""
    
    # Инициализация
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🚗 ДЕМО: Класс Car - Машинка игрока")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    font_large = pygame.font.SysFont(None, 36)
    
    # Создаём машинку в центре экрана
    car = Car(400, 300, color=(255, 0, 0), number=777)
    
    # Простой фон (трава)
    grass_color = (0, 180, 0)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.beep()
                if event.key == pygame.K_e:
                    car.toggle_headlights()
        
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            car.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            car.move_right()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            car.accelerate()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            car.brake()
        
        # Обновление скорости
        car.update_speed()
        
        # Не даём выехать за экран
        if car.x < 50:
            car.x = 50
        if car.x > 750:
            car.x = 750
        
        # Рисование
        screen.fill(grass_color)
        car.draw(screen)
        
        # Заголовок
        title = font_large.render("ДЕМО: Класс Car 🚗", True, (255, 255, 255))
        screen.blit(title, (10, 10))
        
        # Параметры машинки
        params = [
            f"Позиция X: {int(car.x)}",
            f"Позиция Y: {int(car.y)}",
            f"Скорость: {int(car.current_speed * 10)} км/ч",
            f"Фары: {'ВКЛ 💡' if car.headlights_on else 'ВЫКЛ'}",
            f"Цвет: {car.color}",
            f"Номер: {car.number}",
        ]
        
        y_offset = 60
        for param in params:
            surface = font.render(param, True, (255, 255, 255))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        # Управление
        controls = [
            "УПРАВЛЕНИЕ:",
            "← A / → D - Влево/Вправо",
            "↑ W - Ускорение",
            "↓ S - Торможение",
            "SPACE - Сигнал БИП!",
            "E - Включить/выключить фары",
        ]
        
        y_offset = 400
        for text in controls:
            surface = font.render(text, True, (255, 255, 0))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
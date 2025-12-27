import pygame
import numpy as np



class Car:
    """Машинка игрока"""
    
    def __init__(self, x, y, color=(255, 0, 0), number=777):
        self.x = x
        self.y = y
        self.color = color
        self.number = number
        self.image = None  # Для пиксельной картинки
        pygame.mixer.init()
        self.beep_sound = pygame.mixer.Sound("sounds/beep2.wav")
        
        self.headlights_on = False  
          
        
        # Пробуем загрузить картинку
        try:
            self.image = pygame.image.load("imgs/result.png")
            self.image = pygame.transform.scale(self.image, (80, 80))
        except:
            pass
    
    def _create_beep_sound(self):
        """Создаём звук сигнала если нет файла"""
        try:
            # Создаём простой звук БИП (440 Гц)
            sample_rate = 22050
            duration = 1  # 0.2 секунды
            frequency = 500  # Нота "Ля"
            
            
            # Генерируем синусоиду
            samples = np.sin(2 * np.pi * frequency * 
                           np.linspace(0, duration, int(sample_rate * duration)))
            # Делаем звук погромче
            samples = (samples * 32767).astype(np.int16)
            # Создаём стерео звук
            stereo_samples = np.column_stack((samples, samples))
            
            self.beep_sound = pygame.sndarray.make_sound(stereo_samples)
        except:
            # Если и это не работает - ничего страшного
            pass
    
    def draw(self, screen):
        """Рисуем машинку"""
        if self.image:
            # Если есть картинка - показываем её
            screen.blit(self.image, (self.x - 25, self.y - 25))
        else:
            # Иначе рисуем сами
            self._draw_simple(screen)
        
        # Рисуем свет от фар если они включены
        if self.headlights_on:
            self._draw_headlights(screen)
    
    def _draw_simple(self, screen):
        """Простое рисование машинки"""
        # Кузов
        pygame.draw.rect(screen, self.color, 
                        (self.x - 25, self.y - 20, 50, 40))
        
        # Крыша
        dark = tuple(c // 2 for c in self.color)
        pygame.draw.rect(screen, dark, 
                        (self.x - 20, self.y - 30, 40, 20))
        
        # Колёса
        black = (0, 0, 0)
        pygame.draw.circle(screen, black, (self.x - 18, self.y - 15), 6)
        pygame.draw.circle(screen, black, (self.x + 18, self.y - 15), 6)
        pygame.draw.circle(screen, black, (self.x - 18, self.y + 15), 6)
        pygame.draw.circle(screen, black, (self.x + 18, self.y + 15), 6)
        
        # Фары (ярче когда включены!)
        if self.headlights_on:
            light_color = (255, 255, 100)  # Ярко-жёлтый
        else:
            light_color = (255, 255, 0)    # Обычный жёлтый
        
        pygame.draw.circle(screen, light_color, (self.x, self.y - 25), 4)
    
    def _draw_headlights(self, screen):
        """Рисуем свет от фар - конусы света перед машинкой!"""
        # Создаём полупрозрачную поверхность для света
        light_surface = pygame.Surface((self.x + 100, self.y + 100), pygame.SRCALPHA)
        
        # Рисуем два конуса света (левая и правая фара)
        light_color = (255, 255, 150, 60)  # Жёлтый полупрозрачный
        
        # Левый луч фары
        points_left = [
            (self.x - 10, self.y - 25),  # Начало (фара)
            (self.x - 60, self.y - 200),  # Конец слева
            (self.x + 10, self.y - 200)   # Конец справа
        ]
        
        # Правый луч фары
        points_right = [
            (self.x + 10, self.y - 25),  # Начало (фара)
            (self.x - 10, self.y - 200),  # Конец слева
            (self.x + 60, self.y - 200)   # Конец справа
        ]
        
        # Рисуем лучи на экране
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
        if self.x < left_edge:
            self.x = left_edge
        if self.x > right_edge:
            self.x = right_edge
    
    def beep(self):
        """Сигналим! Теперь со звуком!"""
        if self.beep_sound:
            self.beep_sound.play()
        else:
            print("БИП-БИП! 🚗")
    
    def toggle_headlights(self):
        """Включить/выключить фары"""
        self.headlights_on = not self.headlights_on
        if self.headlights_on:
            print("💡 Фары включены!")
        else:
            print("🌑 Фары выключены!")
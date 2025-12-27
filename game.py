import pygame
import sys
from road import Road
from car import Car


class Game:
    """Главный класс игры"""
    
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("🏁 ГОНКИ")
        self.clock = pygame.time.Clock()
        
        # Создаём объекты
        self.road = Road(width, height)
        self.car = Car(width // 2, height - 100)
        
        # Шрифт для подсказок
        self.font = pygame.font.SysFont(None, 24)
    
    def draw_controls(self):
        """Показываем управление"""
        controls = [
            "УПРАВЛЕНИЕ:",
            "← A - Влево",
            "→ D - Вправо", 
            "SPACE - Сигнал",
            "E - Фары вкл/выкл"  # Новая подсказка!
        ]
        
        for i, text in enumerate(controls):
            surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, 10 + i * 30))
    
    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Обрабатываем нажатия кнопок
                if event.type == pygame.KEYDOWN:
                    # Сигнал на ПРОБЕЛ
                    if event.key == pygame.K_SPACE:
                        self.car.beep()
                    
                    # Новое! Фары на кнопку E
                    if event.key == pygame.K_e:
                        self.car.toggle_headlights()
            
            # Управление машинкой
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.car.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.car.move_right()
            
            # Обновление
            self.road.update()
            self.car.keep_on_road(
                self.road.get_left_edge(),
                self.road.get_right_edge()
            )
            
            # Рисование
            self.road.draw(self.screen)
            self.car.draw(self.screen)
            self.draw_controls()
            
            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
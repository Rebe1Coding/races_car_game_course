import pygame
import sys
import random
from road import Road
from car import Car
from obstacle import ObstacleCar
from score_manager import ScoreManager
from game_state import GameState

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
        self.obstacles = []
        self.score_manager = ScoreManager()
        
        # Состояние игры
        self.state = GameState.MENU
        
        # Параметры генерации препятствий
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = 120  # Кадров между появлением машин
        
        # Анимация столкновения
        self.crash_timer = 0
        self.crash_duration = 60  # Кадров анимации
        self.crash_flash = 0
        
        # Шрифты
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_large = pygame.font.SysFont(None, 72)
    
    def reset_game(self):
        """Сброс игры для новой попытки"""
        self.car = Car(self.width // 2, self.height - 100)
        self.obstacles = []
        self.score_manager.reset_current_score()
        self.obstacle_spawn_timer = 0
        self.crash_timer = 0
        self.state = GameState.PLAYING
    
    def spawn_obstacle(self):
        """Создаём новую встречную машину"""
        # Определяем границы дороги
        left_edge = self.road.get_left_edge()
        right_edge = self.road.get_right_edge()
        
        # Случайная позиция на дороге
        x = random.randint(left_edge + 40, right_edge - 40)
        y = -50
        
        # Скорость увеличивается с очками
        base_speed = self.road.get_current_speed() + 2
        bonus_speed = self.score_manager.get_current_score() * 0.1
        speed = base_speed + bonus_speed
        
        obstacle = ObstacleCar(x, y, speed)
        self.obstacles.append(obstacle)
    
    def update_obstacles(self):
        """Обновление всех препятствий"""
        for obstacle in self.obstacles[:]:
            obstacle.update()
            
            # Удаляем машины, вышедшие за экран
            if obstacle.is_off_screen(self.height):
                # Начисляем очко если прошли мимо
                if not obstacle.passed:
                    self.score_manager.add_score(1)
                    obstacle.passed = True
                self.obstacles.remove(obstacle)
    
    def check_collisions(self):
        """Проверка столкновений"""
        car_rect = self.car.get_rect()
        
        for obstacle in self.obstacles:
            obstacle_rect = obstacle.get_rect()
            if car_rect.colliderect(obstacle_rect):
                return True
        return False
    
    def draw_menu(self):
        """Рисуем главное меню"""
        self.screen.fill((0, 100, 0))
        
        # Заголовок
        title = self.font_large.render("ГОНКИ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(title, title_rect)
        
        # Рекорд
        record_text = f"РЕКОРД: {self.score_manager.get_high_score()}"
        record = self.font_medium.render(record_text, True, (255, 255, 0))
        record_rect = record.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(record, record_rect)
        
        # Подсказка
        hint = self.font_small.render("Нажмите ENTER или ПРОБЕЛ чтобы начать", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(self.width // 2, self.height * 2 // 3))
        self.screen.blit(hint, hint_rect)
        
        # Управление
        controls = [
            "УПРАВЛЕНИЕ:",
            "← A - Влево  |  → D - Вправо",
            "↑ W - Ускорение  |  ↓ S - Торможение",
            "SPACE - Сигнал  |  E - Фары"
        ]
        
        y_offset = self.height * 3 // 4
        for text in controls:
            surface = self.font_small.render(text, True, (255, 255, 255))
            rect = surface.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(surface, rect)
            y_offset += 25
    
    def draw_game_over(self):
        """Рисуем экран окончания игры"""
        self.screen.fill((50, 50, 50))
        
        # Заголовок
        title = self.font_large.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 4))
        self.screen.blit(title, title_rect)
        
        # Счёт
        score_text = f"ОЧКИ: {self.score_manager.get_current_score()}"
        score = self.font_medium.render(score_text, True, (255, 255, 255))
        score_rect = score.get_rect(center=(self.width // 2, self.height // 2 - 40))
        self.screen.blit(score, score_rect)
        
        # Рекорд
        record_text = f"РЕКОРД: {self.score_manager.get_high_score()}"
        record = self.font_medium.render(record_text, True, (255, 255, 0))
        record_rect = record.get_rect(center=(self.width // 2, self.height // 2 + 10))
        self.screen.blit(record, record_rect)
        
        # Новый рекорд!
        if self.score_manager.is_new_record():
            new_record = self.font_medium.render("★ НОВЫЙ РЕКОРД! ★", True, (255, 215, 0))
            new_record_rect = new_record.get_rect(center=(self.width // 2, self.height // 2 + 60))
            self.screen.blit(new_record, new_record_rect)
        
        # Подсказка
        hint = self.font_small.render("Нажмите ENTER или ПРОБЕЛ для новой игры", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(self.width // 2, self.height * 3 // 4))
        self.screen.blit(hint, hint_rect)
        
        hint2 = self.font_small.render("ESC - Выход в меню", True, (200, 200, 200))
        hint2_rect = hint2.get_rect(center=(self.width // 2, self.height * 3 // 4 + 30))
        self.screen.blit(hint2, hint2_rect)
    
    def draw_crash_animation(self):
        """Простая анимация столкновения - мигание"""
        # Рисуем обычную сцену
        self.road.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Мигание красным
        if self.crash_flash % 10 < 5:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(100)
            overlay.fill((255, 0, 0))
            self.screen.blit(overlay, (0, 0))
        
        self.car.draw(self.screen)
        
        # Текст "СТОЛКНОВЕНИЕ!"
        crash_text = self.font_large.render("CRASH!", True, (255, 255, 255))
        crash_rect = crash_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(crash_text, crash_rect)
    
    def draw_hud(self):
        """Рисуем интерфейс во время игры"""
        # Текущие очки
        score_text = f"ОЧКИ: {self.score_manager.get_current_score()}"
        score_surface = self.font_medium.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))
        
        # Рекорд
        record_text = f"РЕКОРД: {self.score_manager.get_high_score()}"
        record_surface = self.font_small.render(record_text, True, (255, 255, 0))
        self.screen.blit(record_surface, (10, 50))
        
        # Скорость
        speed_text = f"СКОРОСТЬ: {int(self.car.get_speed())}"
        speed_surface = self.font_small.render(speed_text, True, (200, 200, 200))
        self.screen.blit(speed_surface, (10, 80))
    
    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    # Меню - начать игру
                    if self.state == GameState.MENU:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            self.reset_game()
                    
                    # Game Over - начать заново или выйти в меню
                    elif self.state == GameState.GAME_OVER:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = GameState.MENU
                    
                    # Во время игры
                    elif self.state == GameState.PLAYING:
                        if event.key == pygame.K_SPACE:
                            self.car.beep()
                        if event.key == pygame.K_e:
                            self.car.toggle_headlights()
            
            # Логика игры в зависимости от состояния
            if self.state == GameState.PLAYING:
                # Управление
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.car.move_left()
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.car.move_right()
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.car.accelerate()
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.car.brake()
                
                # Обновление
                self.car.update_speed()
                self.road.update(self.car.get_speed())
                self.car.keep_on_road(
                    self.road.get_left_edge(),
                    self.road.get_right_edge()
                )
                
                # Генерация препятствий
                self.obstacle_spawn_timer += 1
                if self.obstacle_spawn_timer >= self.obstacle_spawn_delay:
                    self.spawn_obstacle()
                    self.obstacle_spawn_timer = 0
                    # Уменьшаем задержку с ростом очков (усложняем игру)
                    min_delay = 60
                    self.obstacle_spawn_delay = max(
                        min_delay,
                        120 - self.score_manager.get_current_score() * 2
                    )
                
                self.update_obstacles()
                
                # Проверка столкновений
                if self.check_collisions():
                    self.state = GameState.CRASH
                    self.crash_timer = 0
                    self.crash_flash = 0
                
                # Рисование
                self.road.draw(self.screen)
                for obstacle in self.obstacles:
                    obstacle.draw(self.screen)
                self.car.draw(self.screen)
                self.draw_hud()
            
            elif self.state == GameState.CRASH:
                # Анимация столкновения
                self.draw_crash_animation()
                self.crash_timer += 1
                self.crash_flash += 1
                
                if self.crash_timer >= self.crash_duration:
                    # Сохраняем рекорд
                    self.score_manager.save_high_score()
                    self.state = GameState.GAME_OVER
            
            elif self.state == GameState.MENU:
                self.draw_menu()
            
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
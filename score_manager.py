import json
import os

class ScoreManager:
    """Управление очками и рекордами"""
    
    def __init__(self, save_file="highscore.json"):
        self.save_file = save_file
        self.current_score = 0
        self.high_score = 0
        
        # Загружаем рекорд при создании
        self.load_high_score()
    
    def load_high_score(self):
        """Загружаем рекорд из файла"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
            else:
                self.high_score = 0
        except:
            # Если не получилось загрузить - начинаем с 0
            self.high_score = 0
    
    def save_high_score(self):
        """Сохраняем рекорд в файл"""
        try:
            data = {'high_score': self.high_score}
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            # Если не получилось сохранить - просто игнорируем
            pass
    
    def add_score(self, points=1):
        """Добавляем очки"""
        self.current_score += points
        
        # Обновляем рекорд если побили
        if self.current_score > self.high_score:
            self.high_score = self.current_score
    
    def reset_current_score(self):
        """Сбрасываем текущий счёт (для новой игры)"""
        self.current_score = 0
    
    def is_new_record(self):
        """Проверяем, установлен ли новый рекорд"""
        return self.current_score == self.high_score and self.current_score > 0
    
    def get_current_score(self):
        """Получаем текущие очки"""
        return self.current_score
    
    def get_high_score(self):
        """Получаем рекорд"""
        return self.high_score

# ===== ДЕМО-РЕЖИМ =====
if __name__ == "__main__":
    """Демонстрация класса ScoreManager - система очков!"""
    
    import pygame
    
    # Инициализация
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🏆 ДЕМО: Класс ScoreManager - Система очков")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    font_large = pygame.font.SysFont(None, 48)
    font_huge = pygame.font.SysFont(None, 72)
    
    # Создаём менеджер очков
    score_manager = ScoreManager("demo_highscore.json")
    
    # Цвета
    bg_color = (20, 20, 40)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Добавляем очко
                    score_manager.add_score(1)
                if event.key == pygame.K_UP:
                    # Добавляем 10 очков
                    score_manager.add_score(10)
                if event.key == pygame.K_r:
                    # Сбрасываем текущий счёт
                    score_manager.reset_current_score()
                if event.key == pygame.K_s:
                    # Сохраняем рекорд
                    score_manager.save_high_score()
                    print("Рекорд сохранён!")
        
        # Рисование
        screen.fill(bg_color)
        
        # Заголовок
        title = font_large.render("ДЕМО: ScoreManager 🏆", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 20))
        
        # Табличка с очками - БОЛЬШАЯ И КРАСИВАЯ!
        table_width = 600
        table_height = 300
        table_x = (800 - table_width) // 2
        table_y = 120
        
        # Фон таблички
        pygame.draw.rect(screen, (40, 40, 60), (table_x, table_y, table_width, table_height), border_radius=20)
        pygame.draw.rect(screen, (100, 100, 150), (table_x, table_y, table_width, table_height), 5, border_radius=20)
        
        # Текущие очки
        current_label = font_large.render("ТЕКУЩИЕ ОЧКИ:", True, (200, 200, 255))
        screen.blit(current_label, (table_x + 50, table_y + 30))
        
        current_score = font_huge.render(str(score_manager.get_current_score()), True, (255, 255, 100))
        screen.blit(current_score, (table_x + table_width // 2 - current_score.get_width() // 2, table_y + 80))
        
        # Разделитель
        pygame.draw.line(screen, (100, 100, 150), (table_x + 50, table_y + 160), (table_x + table_width - 50, table_y + 160), 3)
        
        # Рекорд
        record_label = font_large.render("РЕКОРД:", True, (255, 215, 0))
        screen.blit(record_label, (table_x + 50, table_y + 180))
        
        record_score = font_huge.render(str(score_manager.get_high_score()), True, (255, 215, 0))
        screen.blit(record_score, (table_x + table_width // 2 - record_score.get_width() // 2, table_y + 220))
        
        # Новый рекорд!
        if score_manager.is_new_record():
            new_record_text = font_large.render("★ НОВЫЙ РЕКОРД! ★", True, (255, 0, 0))
            # Мигающий эффект
            if pygame.time.get_ticks() % 1000 < 500:
                screen.blit(new_record_text, (screen.get_width() // 2 - new_record_text.get_width() // 2, table_y + table_height + 20))
        
        # Управление
        controls = [
            "УПРАВЛЕНИЕ:",
            "SPACE - Добавить 1 очко",
            "↑ - Добавить 10 очков",
            "R - Сбросить текущий счёт",
            "S - Сохранить рекорд в файл",
        ]
        
        y_offset = 480
        for text in controls:
            surface = font.render(text, True, (255, 255, 255))
            screen.blit(surface, (screen.get_width() // 2 - surface.get_width() // 2, y_offset))
            y_offset += 25
        
        pygame.display.flip()
        clock.tick(60)
    
    # Сохраняем при выходе
    score_manager.save_high_score()
    pygame.quit()
    
    # Удаляем демо-файл
    import os
    if os.path.exists("demo_highscore.json"):
        os.remove("demo_highscore.json")
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
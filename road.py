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
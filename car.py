import pygame



class Car:
    """Машинка игрока"""
    
    def __init__(self, x, y, color=(255, 0, 0), number=777):
        self.x = x
        self.y = y
        self.color = color
        self.number = number
        self.image = None  # Для пиксельной картинки
        
        # Пробуем загрузить картинку
        try:
            self.image = pygame.image.load("imgs/result.png")
            self.image = pygame.transform.scale(self.image, (80, 80))
        except:
            pass  # Если картинки нет - будем рисовать
    
    def draw(self, screen):
        """Рисуем машинку"""
        if self.image:
            # Если есть картинка - показываем её
            screen.blit(self.image, (self.x - 25, self.y - 25))
        else:
            # Иначе рисуем сами
            self._draw_simple(screen)
    
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
        
        # Фары
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y - 25), 4)
    
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
        """Сигналим!"""
        print("БИП-БИП! 🚗")

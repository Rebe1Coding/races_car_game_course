from enum import Enum

class GameState(Enum):
    """Состояния игры"""
    MENU = 1      # Главное меню
    PLAYING = 2   # Игра идёт
    GAME_OVER = 3 # Игра окончена
    CRASH = 4     # Анимация столкновения
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Boolean, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import random
import uuid

# Модели данных
class Coordinate(ComplexModel):
    """Координата на игровом поле"""
    x = Integer
    y = Integer

class Ship(ComplexModel):
    """Корабль"""
    id = Integer
    size = Integer
    coordinates = Array(Coordinate)
    hits = Integer

class GameBoard(ComplexModel):
    """Игровое поле"""
    ships = Array(Ship)
    shots = Array(Coordinate)

class GameState(ComplexModel):
    """Состояние игры"""
    game_id = Unicode
    player_board = GameBoard
    computer_board = GameBoard
    player_turn = Boolean
    game_over = Boolean
    winner = Unicode
    message = Unicode

# Хранилище игр
games = {}

# Размер игрового поля
BOARD_SIZE = 10

def create_random_ship(board, ship_size):
    """Создает случайный корабль на доске"""
    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        # Выбираем случайную ориентацию (0 - горизонтально, 1 - вертикально)
        orientation = random.randint(0, 1)
        
        if orientation == 0:  # горизонтально
            x = random.randint(0, BOARD_SIZE - ship_size)
            y = random.randint(0, BOARD_SIZE - 1)
            coordinates = [Coordinate(x=x+i, y=y) for i in range(ship_size)]
        else:  # вертикально
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - ship_size)
            coordinates = [Coordinate(x=x, y=y+i) for i in range(ship_size)]
        
        # Проверяем, не пересекается ли корабль с существующими
        valid = True
        for ship in board.ships:
            for ship_coord in ship.coordinates:
                for new_coord in coordinates:
                    # Проверяем сам корабль и область вокруг него (1 клетка)
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if (ship_coord.x == new_coord.x + dx and 
                                ship_coord.y == new_coord.y + dy):
                                valid = False
                                break
                        if not valid:
                            break
                    if not valid:
                        break
                if not valid:
                    break
            if not valid:
                break
        
        if valid:
            return Ship(id=len(board.ships) + 1, size=ship_size, coordinates=coordinates, hits=0)
        
        attempts += 1
    
    return None

def initialize_game_board():
    """Инициализирует игровое поле с кораблями"""
    board = GameBoard(ships=[], shots=[])
    
    # Добавляем корабли разных размеров
    # 1 корабль размером 4 клетки
    ship = create_random_ship(board, 4)
    if ship:
        board.ships.append(ship)
    
    # 2 корабля размером 3 клетки
    for _ in range(2):
        ship = create_random_ship(board, 3)
        if ship:
            board.ships.append(ship)
    
    # 3 корабля размером 2 клетки
    for _ in range(3):
        ship = create_random_ship(board, 2)
        if ship:
            board.ships.append(ship)
    
    # 4 корабля размером 1 клетка
    for _ in range(4):
        ship = create_random_ship(board, 1)
        if ship:
            board.ships.append(ship)
    
    return board

def is_ship_at(board, x, y):
    """Проверяет, есть ли корабль в указанных координатах"""
    for ship in board.ships:
        for coord in ship.coordinates:
            if coord.x == x and coord.y == y:
                return ship
    return None

def is_shot_at(board, x, y):
    """Проверяет, был ли выстрел в указанные координаты"""
    for shot in board.shots:
        if shot.x == x and shot.y == y:
            return True
    return False

def computer_make_shot(game_state):
    """Компьютер делает выстрел"""
    # Простая стратегия: случайный выстрел в непростреленную клетку
    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)
        
        if not is_shot_at(game_state.player_board, x, y):
            return Coordinate(x=x, y=y)
        
        attempts += 1
    
    # Если не нашли свободную клетку, выбираем любую
    return Coordinate(x=random.randint(0, BOARD_SIZE - 1), y=random.randint(0, BOARD_SIZE - 1))

def check_game_over(game_state):
    """Проверяет, закончилась ли игра"""
    # Проверяем, все ли корабли игрока уничтожены
    player_ships_destroyed = True
    for ship in game_state.player_board.ships:
        if ship.hits < ship.size:
            player_ships_destroyed = False
            break
    
    # Проверяем, все ли корабли компьютера уничтожены
    computer_ships_destroyed = True
    for ship in game_state.computer_board.ships:
        if ship.hits < ship.size:
            computer_ships_destroyed = False
            break
    
    if player_ships_destroyed:
        game_state.game_over = True
        game_state.winner = "computer"
        game_state.message = "Компьютер победил! Все ваши корабли уничтожены."
        return True
    
    if computer_ships_destroyed:
        game_state.game_over = True
        game_state.winner = "player"
        game_state.message = "Вы победили! Все корабли компьютера уничтожены."
        return True
    
    return False

# SOAP сервис
class BattleshipService(ServiceBase):
    """Сервис для игры в Морской бой"""
    
    @rpc(_returns=GameState)
    def new_game(ctx):
        """Создать новую игру"""
        game_id = str(uuid.uuid4())
        
        # Инициализируем доски игрока и компьютера
        player_board = initialize_game_board()
        computer_board = initialize_game_board()
        
        # Определяем, кто ходит первым (случайно)
        player_turn = random.choice([True, False])
        
        # Создаем состояние игры
        game_state = GameState(
            game_id=game_id,
            player_board=player_board,
            computer_board=computer_board,
            player_turn=player_turn,
            game_over=False,
            winner="",
            message="Новая игра создана. " + ("Ваш ход!" if player_turn else "Ход компьютера!")
        )
        
        # Если первым ходит компьютер, делаем его ход
        if not player_turn:
            shot = computer_make_shot(game_state)
            game_state = process_shot(game_state, shot, is_player_shot=False)
        
        # Сохраняем игру
        games[game_id] = game_state
        
        return game_state
    
    @rpc(Unicode, Integer, Integer, _returns=GameState)
    def player_shot(ctx, game_id, x, y):
        """Игрок делает выстрел по координатам (x, y)"""
        if game_id not in games:
            return GameState(
                game_id="",
                player_board=GameBoard(ships=[], shots=[]),
                computer_board=GameBoard(ships=[], shots=[]),
                player_turn=False,
                game_over=True,
                winner="",
                message="Игра не найдена"
            )
        
        game_state = games[game_id]
        
        # Проверяем, не закончилась ли игра
        if game_state.game_over:
            return game_state
        
        # Проверяем, ход ли игрока
        if not game_state.player_turn:
            game_state.message = "Сейчас не ваш ход!"
            return game_state
        
        # Проверяем валидность координат
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            game_state.message = "Некорректные координаты выстрела!"
            return game_state
        
        # Проверяем, не стрелял ли игрок уже в эту клетку
        if is_shot_at(game_state.computer_board, x, y):
            game_state.message = "Вы уже стреляли в эту клетку!"
            return game_state
        
        # Делаем выстрел игрока
        shot = Coordinate(x=x, y=y)
        game_state = process_shot(game_state, shot, is_player_shot=True)
        
        # Если игра не закончилась и ход компьютера, делаем его ход
        if not game_state.game_over and not game_state.player_turn:
            computer_shot = computer_make_shot(game_state)
            game_state = process_shot(game_state, computer_shot, is_player_shot=False)
        
        # Обновляем игру в хранилище
        games[game_id] = game_state
        
        return game_state
    
    @rpc(Unicode, _returns=GameState)
    def get_game_state(ctx, game_id):
        """Получить текущее состояние игры"""
        if game_id not in games:
            return GameState(
                game_id="",
                player_board=GameBoard(ships=[], shots=[]),
                computer_board=GameBoard(ships=[], shots=[]),
                player_turn=False,
                game_over=True,
                winner="",
                message="Игра не найдена"
            )
        
        return games[game_id]

def process_shot(game_state, shot, is_player_shot):
    """Обрабатывает выстрел (игрока или компьютера)"""
    if is_player_shot:
        # Игрок стреляет по доске компьютера
        board = game_state.computer_board
        board.shots.append(shot)
        
        ship = is_ship_at(board, shot.x, shot.y)
        if ship:
            # Попадание
            ship.hits += 1
            if ship.hits == ship.size:
                game_state.message = "Вы потопили корабль компьютера!"
            else:
                game_state.message = "Вы попали в корабль компьютера!"
            
            # Игрок ходит снова
            game_state.player_turn = True
        else:
            # Промах
            game_state.message = "Вы промахнулись! Ход компьютера."
            game_state.player_turn = False
    else:
        # Компьютер стреляет по доске игрока
        board = game_state.player_board
        board.shots.append(shot)
        
        ship = is_ship_at(board, shot.x, shot.y)
        if ship:
            # Попадание
            ship.hits += 1
            if ship.hits == ship.size:
                game_state.message += f" Компьютер потопил ваш корабль по координатам ({shot.x}, {shot.y})!"
            else:
                game_state.message += f" Компьютер попал в ваш корабль по координатам ({shot.x}, {shot.y})!"
            
            # Компьютер ходит снова
            game_state.player_turn = False
        else:
            # Промах
            game_state.message += f" Компьютер промахнулся по координатам ({shot.x}, {shot.y})! Ваш ход."
            game_state.player_turn = True
    
    # Проверяем, не закончилась ли игра
    check_game_over(game_state)
    
    return game_state

# Создаем приложение
application = Application(
    [BattleshipService],
    tns='http://battleship.example.com/soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Создаем WSGI приложение
wsgi_app = WsgiApplication(application)

# Запускаем сервер
if __name__ == '__main__':
    server = make_server('127.0.0.1', 8000, wsgi_app)
    print("SOAP сервер игры 'Морской бой' запущен на http://127.0.0.1:8000")
    print("WSDL доступен по адресу: http://127.0.0.1:8000/?wsdl")
    server.serve_forever()
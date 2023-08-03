SCREEN_WIDTH = 600
SCREEN_HEIGHT = 850
PLAYER_HP = 500
PLAYER_MODIFICATOR = 15

PLAYER_BULLET_LST = ['laser_player1', 'laser_player2', 'laser_player3', 'laser_player6', 'laser_player8',
                     'laser_player9', 'laser_player10', 'laser_player11', 'laser_player12', 'laser_player13']
ALIEN_BULLET_LST = ['laser_alien1', 'laser_alien2', 'laser_alien3']

BULLET_DATA = {
    'laser_player1': {'image': 'laser1', 'damage': 20, 'velocity': 500, 'qty': 100},
    'laser_player2': {'image': 'laser2', 'damage': 25, 'velocity': 520, 'qty': 90},
    'laser_player3': {'image': 'laser3', 'damage': 30, 'velocity': 540, 'qty': 80},
    'laser_player6': {'image': 'laser6', 'damage': 35, 'velocity': 560, 'qty': 70},
    'laser_player8': {'image': 'laser8', 'damage': 40, 'velocity': 580, 'qty': 60},
    'laser_player9': {'image': 'laser9', 'damage': 45, 'velocity': 600, 'qty': 50},
    'laser_player10': {'image': 'laser10', 'damage': 35, 'velocity': 620, 'qty': 40},
    'laser_player11': {'image': 'laser11', 'damage': 40, 'velocity': 640, 'qty': 30},
    'laser_player12': {'image': 'laser12', 'damage': 45, 'velocity': 660, 'qty': 20},
    'laser_player13': {'image': 'laser13', 'damage': 50, 'velocity': 680, 'qty': 10},
    'laser_alien1': {'image': 'laser_alien1', 'damage': 50, 'velocity': 540, 'qty': 30},
    'laser_alien2': {'image': 'laser_alien2', 'damage': 60, 'velocity': 550, 'qty': 30},
    'laser_alien3': {'image': 'laser_alien3', 'damage': 70, 'velocity': 560, 'qty': 30}
}

ALIEN_LST = ["alien1", 'alien2', 'alien3', 'alien4', 'alien5', 'alien6', 'alien7']
ALIEN_DATA = {
    'alien1': {'image': 'alien1', 'damage': 50, 'points': 200, 'hp': 30, 'defence': 5},
    'alien2': {'image': 'alien2', 'damage': 50, 'points': 200, 'hp': 35, 'defence': 5},
    'alien3': {'image': 'alien3', 'damage': 60, 'points': 200, 'hp': 45, 'defence': 10},
    'alien4': {'image': 'alien4', 'damage': 60, 'points': 240, 'hp': 55, 'defence': 10},
    'alien5': {'image': 'alien5', 'damage': 80, 'points': 180, 'hp': 60, 'defence': 15},
    'alien6': {'image': 'alien6', 'damage': 80, 'points': 300, 'hp': 70, 'defence': 15},
    'alien7': {'image': 'alien7', 'damage': 100, 'points': 420, 'hp': 80, 'defence': 15}
}
POWERUP_LST = ["power", 'energy', 'bullets']
POWERUP_DATA = {
    'power': {'image': 'power', 'hp': 0, 'points': 3000, 'bullets': None, 'chance': 5},
    'energy': {'image': 'energy', 'hp': 500, 'points': 1500, 'bullets': None, 'chance': 3},
    'bullets': {'image': 'bullets', 'hp': 0, 'points': 1000, 'bullets': 100, 'chance': 4}
}

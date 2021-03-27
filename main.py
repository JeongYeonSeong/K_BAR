import config
import pygame
import random
import threading as th
from time import sleep

"""
1. 음악
2. bet 범위
"""

class GUI:
    def __init__(self):
        pygame.init()

        # pygame.mixer.init()
        # pygame.mixer.music.load('musics/bg.wav')
        # pygame.mixer.music.play(-1)

        self.select = -1
        self.bet = 0
        self.rate = []

        self.horses = []
        self.winner = -1
        self.box_trigger = False

        self.money = config.start_money
        self.horse = config.horse_name
        self.rate_set = config.rate
        self.goal = config.goal_standard
        self.probability = config.probability

        self.scene = ['start', 'main', 'racing']
        self.menu = {'start': ['start', 'quit'], 'main': ['start', 'back to start page'], 'on game':['skip']}

        self.now_scene = 0
        self.target = 0

        self.button = []

        self.condition = []

        self.RED = 255, 0, 0        # 적색:   적 255, 녹   0, 청   0
        self.GREEN = 0, 255, 0      # 녹색:   적   0, 녹 255, 청   0
        self.BLUE = 0, 0, 255       # 청색:   적   0, 녹   0, 청 255
        self.PURPLE = 127, 0, 127   # 보라색: 적 127, 녹   0, 청 127
        self.BLACK = 0, 0, 0        # 검은색: 적   0, 녹   0, 청   0
        self.GRAY = 127, 127, 127   # 회색:   적 127, 녹 127, 청 127
        self.WHITE = 255, 255, 255  # 하얀색: 적 255, 녹 255, 청 255

        #start
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        # SCREEN_RECT = pygame.Rect((0,50), (1280, 620))
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.scenes()

        pygame.display.set_caption('K Bar')

        done = False
        clock = pygame.time.Clock()

        while not done:
            clock.tick(30)
            self.scene_controller(self.now_scene)

    def scene_controller(self, mode):
        game_end = 0

        if mode == 0:
            if len(self.button) == 0:
                self.button.append(Button(self.SCREEN, (640,500), (100,40), 'start', self.btn_start))
                self.button.append(Button(self.SCREEN, (640,580), (100,40), 'quit', self.btn_exit))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if len(self.button) != 0:
                        for btn in self.button:
                            if btn.rect.collidepoint(event.pos):
                                btn.active()
                                btn.function()
                            elif btn.rect.collidepoint(pygame.mouse.get_pos()):
                                btn.above()
            
        elif mode == 1:
            bets = [-10000, -5000, -1000, 1000, 5000, 10000]
            self.set_condition()
            if len(self.button) == 0:
                self.button.append(Button(self.SCREEN, (1100,100), (300,30), 'your money : ' + str(self.money), self.btn_nothing))
                
                self.button.append(Button(self.SCREEN, (1200,590), (120,40), 'RACE', self.btn_race))
                self.button.append(Button(self.SCREEN, (1200,680), (100,30), 'quit', self.btn_exit))
                self.button.append(Button(self.SCREEN, (1200,640), (100,30), 'main', self.btn_resume))
                self.button.append(Button(self.SCREEN, (200,100), (200,25),'CONDITION', self.btn_nothing))
                for i in range(9):
                    text = str(i + 1) + '. ' + self.horse[i] + ' : ' + str(self.condition[i])
                    self.button.append(Button(self.SCREEN, (200, 140 + i * 25), (200,24),text, lambda i=i: self.btn_select(i)))

                for index, i in enumerate(bets):
                    self.button.append(Button(self.SCREEN, (150 + index * 110, 600), (100,25), str(i), lambda i=i: self.btn_bet(i)))
                self.button.append(Button(self.SCREEN, (150, 570), (100,25), 'BETTING', self.btn_nothing))
            
            self.button.append(Button(self.SCREEN, (430, 630), (660,25), str(self.bet), self.btn_nothing))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if len(self.button) != 0:
                        for btn in self.button:
                            if btn.rect.collidepoint(event.pos):
                                btn.active()
                                btn.function()
                            elif btn.rect.collidepoint(pygame.mouse.get_pos()):
                                btn.above()

        elif mode == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if len(self.horses) == 0:
                print(self.condition)
                for i in range(9):
                    self.horses.append(Horse(i, self.condition[i], self.SCREEN))
                sleep(2)
            else:
                self.scenes(3)
                for index, i in enumerate(self.horses):
                    i.running(self.probability)
                    if i.progress >= self.goal:
                        game_end = 1
                        self.winner = index
                sleep(0.05)
            self.condition = []

        elif mode == 4:
            self.button.append(Button(self.SCREEN, (1200,630), (120,40), 'Continue', self.btn_continue))
            self.button.append(Button(self.SCREEN, (1200,680), (100,30), 'quit', self.btn_exit))
            self.button.append(Button(self.SCREEN, (630, 360), (400,100), self.horse[self.winner] + ' Win!!', self.btn_nothing, ftSize=40))
            
            text = ''
            if self.winner == self.select:
                gets = int(self.bet * self.rate[self.select])
                text = 'You Win! You got' + str(gets) + ' (your bet X ' + str(self.rate[self.select] + ')')
                self.money += gets - self.bet
            else: 
                text = 'You Lose! You lost' + str(self.bet)
                self.money -= self.bet
            
            if self.money == 0:
                sleep(1)
                for i in range(len(self.button)):
                    self.button.pop()
                self.now_scene = 5
                self.scenes(5)
                return

            self.button.append(Button(self.SCREEN, (630, 500), (800,100), text, self.btn_nothing, ftSize=30))
            
            self.now_scene = 1
            self.scenes(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if len(self.button) != 0:
                        for btn in self.button:
                            if btn.rect.collidepoint(event.pos):
                                btn.active()
                                btn.function()
                            elif btn.rect.collidepoint(pygame.mouse.get_pos()):
                                btn.above()
            
        elif mode == 5:
            self.button.append(Button(self.SCREEN, (1200,680), (100,30), 'quit', self.btn_exit))
            self.button.append(Button(self.SCREEN, (1200,640), (100,30), 'main', self.btn_resume))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if len(self.button) != 0:
                        for btn in self.button:
                            if btn.rect.collidepoint(event.pos):
                                btn.active()
                                btn.function()
                            elif btn.rect.collidepoint(pygame.mouse.get_pos()):
                                btn.above()

        if mode != 2 or mode != 4:
            if self.box_trigger:
                pygame.draw.rect(self.SCREEN, (0,255,0), pygame.Rect(210, 100, 80, 50))
            for btn in self.button:
                btn.draw()

        if game_end == 1:
            self.horses = []
            
            pygame.display.update()
            self.now_scene = 4
            self.scenes(4)
        else:
            pygame.display.update()

    def set_condition(self):
        if len(self.condition) != 9:
            self.condition = [random.randint(49, 100) for i in range(9)]
            self.set_rate()

    def set_rate(self):
        cond = self.condition[0:]
        cond.sort()
        print('condition :', self.condition)
        print('cond :', cond)
        for i in range(9):
            self.rate.append(self.rate_set[self.condition.index(cond[i])])
        print('rate :', self.rate)
        return

    def btn_race(self):
        self.now_scene = 2
        self.scenes(2)
        self.box_trigger = False
        if len(self.button) >= 1:
            self.button[0].inactive()
        for i in range(len(self.button)):
            self.button.pop()

    def btn_continue(self):
        self.now_scene = 1
        self.scenes(1)
        self.box_trigger = False
        self.bet = 0
        if len(self.button) >= 1:
            self.button[0].inactive()
        for i in range(len(self.button)):
            self.button.pop()
        return

    def btn_nothing(self):
        return

    def btn_select(self, num):
        self.select = num

    def btn_bet(self, bet):
        self.bet += bet
        if self.bet < 0:
            self.bet = 0
        elif self.bet > self.money:
            self.bet = self.money

    def btn_start(self):
        self.now_scene = 1
        self.scenes(1)
        self.box_trigger = False
        if len(self.button) != 0:
            self.button[0].inactive()
        self.button = []

    def btn_resume(self):
        self.now_scene = 0
        self.scenes(0)
        self.box_trigger = False
        self.bet = 0
        self.money = config.start_money
        if len(self.button) != 0:
            self.button[1].inactive()
        self.button = []

    def btn_exit(self):
        exit()

    def scenes(self, scene=0):
        bgs = ['images/start_image.jpeg', 'images/main.jpeg', \
            'images/racing.jpg', 'images/race.png', 'images/racing.jpg', \
            'images/GameOver.jpg']
        bg = pygame.image.load(bgs[scene])
        self.SCREEN.blit(bg,(0,0))
        return

class Horse:
    def __init__(self, index, condition, SCREEN):
        self.condition = condition
        self.lane = index
        self.run = 0
        self.progress = 135
        self.SCREEN = SCREEN
        self.rect = pygame.Rect(0,0, 225,225)
        self.rect.center = (self.progress, self.lane * 200)

    def running(self, probability):
        runs = ['images/run1.png', 'images/run2.png', 'images/run3.png']
        image = pygame.image.load(runs[self.run])
        self.progress += self.racing(probability)
        self.SCREEN.blit(image, (self.progress, 75 + self.lane * 47))
        if self.run == 0:
            self.run = 1
        elif self.run == 1:
            self.run = 2
        elif self.run == 2:
            self.run = 0   
    
    def racing(self, probability):
        move = random.randint(1, probability)

        if move <= self.condition:
            return 10
        return 0

class Button:
    BLACK = (0, 0, 0)
    ABOVE_COLOR = (234, 236, 240)
    ACTIVE_COLOR = (144, 144, 144)
    INACTIVE_COLOR = (215, 215, 215)

    def __init__(self, screen, pos, size, name, call, color=BLACK, ftSize = 20, param=None):
        self.screen = screen
        
        FONT = pygame.font.Font('freesansbold.ttf', ftSize)
        self.text = FONT.render(name, True, color)
        self.text_rect = self.text.get_rect(center = pos)

        self.rect = pygame.Rect(0,0, *size)
        self.rect.center = pos
        self.function = call if param == None else call(param)
        self.color = Button.INACTIVE_COLOR

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def above(self):
        self.color = Button.ABOVE_COLOR

    def active(self):
        self.color = Button.ACTIVE_COLOR

    def inactive(self):
        self.color = Button.INACTIVE_COLOR

if __name__ == '__main__':
    gui = GUI()


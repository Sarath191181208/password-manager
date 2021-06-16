import json
import os
import pygooey
import pygame

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600
# colours
GRAY = (197, 194, 197, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Password's Manager")
FPS = 30


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


defaultPassword = ""


def ASCII(string: str) -> list[int]:
    arr = []
    for i in string:
        arr.append(ord(i))
    # .extend(ord(num) for num in string)
    return arr


def encrypt(passwd: str) -> list[int]:
    encrypt = ASCII(passwd)
    key = ASCII(defaultPassword)
    for i in range(len(encrypt)):
        encrypt[i] += key[i % len(key)]
    encryptStr = ''.join([chr(value)for value in encrypt])
    return encryptStr


def decrypt(passwd: str) -> str:
    decrypt = ASCII(passwd)
    key = ASCII(defaultPassword)
    for i in range(len(decrypt)):
        decrypt[i] -= key[i % len(key)]
    decryptStr = ''.join([chr(value)for value in decrypt])
    return decryptStr


def read(scrollBar=None):
    if os.path.exists('./passwords.json'):
        data = json.load(open('passwords.json'))
        brd.items.clear()
        for i in data:
            brd.items.append(item(i, decrypt(data[i])))
            # print(decrypt(data[i]))
        #scrollbar.image_height = SCREEN_HEIGHT + len(data)
        if scrollBar != None and len(data) != 0:
            scrollBar.image_height = SCREEN_HEIGHT + len(data)
        elif scrollBar != None:
            scrollBar.image_height = SCREEN_HEIGHT + 1
        brd.draw(WIN)
    else:
        print("no current passwords found")


def add(usrName: str, passwd: str) -> None:
    '''
    Adds user name and password into json file
    '''
    dic = {
    }
    if not os.path.exists('./passwords.json'):
        with open('passwords.json', 'a') as outfile:
            json_object = json.dumps({})
            outfile.write(json_object)
            print("Created")
    username = str(usrName)
    password = str(passwd)
    password = encrypt(password)
    dic[username] = password

    with open('passwords.json', 'r+') as outfile:
        # outfile.write(json_object)
        file_data = json.load(outfile)
        # print(outfile)
        # pos = len(file_data)
        outfile.seek(0, 0)
        outfile.truncate()
        file_data.update(dic)
        outfile.write(json.dumps(file_data, indent=4))
    read()


widgets = []


def userName(id, final):
    pass


def password(id, final):
    pass


def changeDefaultPassword(id, final):
    defaultPasswordBox.GivenValue = final


def button_callback(id):
    if userNameBox.final != None and passwordBox.final != None and (userNameBox.final != '' and passwordBox.final != ''):
        add(userNameBox.final, passwordBox.final)
    else:
        print("please enter username and password")


def delete(id):
    with open('passwords.json', 'r+') as outfile:
        # outfile.write(json_object)
        file_data = json.load(outfile)
        del file_data[brd.items[id].username]
        # print(outfile)
        # pos = len(file_data)
        outfile.seek(0, 0)
        outfile.truncate()
        outfile.write(json.dumps(file_data, indent=4))
    read()


# see all settings help(pygooey.TextBox.__init__)
entry_settings = {
    "inactive_on_enter": True,
    'active': False,
    "active_color": (0, 0, 0),
    "clear_on_enter": True,
    "delete_speed": 500
}
userNameBox = pygooey.TextBox(rect=(20, 560, 150, 30),
                              command=userName, **entry_settings)
widgets.append(userNameBox)
passwordBox = pygooey.TextBox(rect=(200, 560, 150, 30),
                              command=password, **entry_settings)
widgets.append(passwordBox)
defaultPasswordBox = pygooey.TextBox(
    rect=(WIN.get_width()/2-90, WIN.get_height()/2-15, 150, 30), command=changeDefaultPassword, **entry_settings)
# see all settings help(pygooey.Button.__init__)
btn_settings = {
    "clicked_font_color": (0, 0, 0),
    'border_hover_color': (150, 150, 150),
    "hover_font_color": (255, 255, 255),
    'font': pygame.font.Font(None, 16),
    'font_color': (255, 255, 255),
    'border_color': (0, 0, 0),
}
btn = pygooey.Button(rect=(420, 563, 105, 25),
                     command=button_callback, text='OK', **btn_settings)
widgets.append(btn)


class board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.items = []
        self.show_items = 6

    def draw(self, win, strt=0):
        del_btn_settings = {
            "color": (0, 0, 0, 0),
            "clicked_font_color": (0, 0, 0),
            'border_hover_color': (150, 150, 150),
            "hover_font_color": (255, 255, 255),
            'font': pygame.font.Font(pygame.font.match_font('calibri', bold=False, italic=False), 16),
            'font_color': (160, 40, 40),
            'border_color': (230, 40, 40),
        }
        win.fill((255, 255, 255))
        lineAt = self.width/self.show_items
        correctionFactor = 120
        stroke = 1
        for i in range(strt, len(self.items)):
            self.items[i].button = pygooey.Button(rect=(self.width - 90, (i-strt)*lineAt+23, 50, 25),
                                                  command=delete, text='DEL', **del_btn_settings)
            self.items[i].button.GivenID = i
        for i in range(self.show_items + 1):
            pygame.draw.line(win, (0, 0, 0), (0, i * lineAt),
                             (self.width, i*lineAt), stroke)
        for i in range(strt, len(self.items)):
            userName = self.items[i].username
            password = self.items[i].password
            userName = PYtxt(userName)
            password = PYtxt(password, 22)
            win.blit(userName, (20, (i-strt) *
                     (lineAt) + userName.get_height()-20))
            win.blit(PYtxt(str(i)+".", 15), (8, (i-strt) *
                     (lineAt) + userName.get_height()-12))
            win.blit(password, (self.width - password.get_width() -
                     correctionFactor, ((i-strt) * lineAt) + password.get_height()+30))
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(0, 540, 540, 60))
        pygame.display.update()


class item:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.button = None


class ScrollBar(object):
    def __init__(self, image_height):
        self.current = 0
        self.y_axis = 0
        self.image_height = image_height
        self.change_y = 0

        # bar_height = int((SCREEN_HEIGHT - 40) /
        #                  (image_height / (SCREEN_HEIGHT * 1.0)))
        # bar_height = int((SCREEN_HEIGHT - 40) /
        #                  (image_height ))
        self.bar_rect = pygame.Rect(SCREEN_WIDTH - 20, 20, 20, 50)
        # self.bar_rect = pygame.Rect(SCREEN_WIDTH - 20, 20, 20, 30)
        self.bar_up = pygame.Rect(SCREEN_WIDTH - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(
            SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20, 20, 20)

        self.bar_up_image = pygame.image.load("up.png").convert()
        self.bar_down_image = pygame.image.load("down.png").convert()

        self.on_bar = False
        self.mouse_diff = 0

    def update(self):
        self.y_axis += self.change_y

        if self.y_axis > 0:
            self.y_axis = 0
        # elif (self.y_axis + self.image_height) < SCREEN_HEIGHT:
        #     self.y_axis = SCREEN_HEIGHT - self.image_height

        height_diff = abs(self.image_height - SCREEN_HEIGHT)

        scroll_length = SCREEN_HEIGHT - self.bar_rect.height - 40
        bar_half_lenght = self.bar_rect.height / 2 + 20

        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (SCREEN_HEIGHT - 20):
                self.bar_rect.bottom = SCREEN_HEIGHT - 20

            self.y_axis = int(height_diff / (scroll_length * 1.0)
                              * (self.bar_rect.centery - bar_half_lenght) * -1)
        else:
            self.bar_rect.centery = scroll_length / \
                (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 5
            elif self.bar_down.collidepoint(pos):
                self.change_y = -5

        if event.type == pygame.MOUSEBUTTONUP:
            self.change_y = 0
            self.on_bar = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_y = 5
            elif event.key == pygame.K_DOWN:
                self.change_y = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.change_y = 0
            elif event.key == pygame.K_DOWN:
                self.change_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.bar_rect)

        screen.blit(self.bar_up_image, (SCREEN_WIDTH - 20, 0))
        screen.blit(self.bar_down_image,
                    (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))


run = True

while (defaultPasswordBox.GivenValue == '' or defaultPasswordBox.GivenValue == None) and run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        defaultPasswordBox.get_event(event)
    defaultPasswordBox.update()
    defaultPasswordBox.draw(WIN)
    pygame.display.update()
defaultPassword = defaultPasswordBox.GivenValue


brd = board(540, 560)

brd.draw(WIN)
scrollbar = ScrollBar(606)
read(scrollbar)
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brd.draw(WIN)
        for w in widgets:
            w.get_event(event)
        for i in brd.items:
            i.button.get_event(event)
        scrollbar.event_handler(event)
    scrollbar.update()
    if scrollbar.current != scrollbar.y_axis:
        brd.draw(WIN, abs(scrollbar.y_axis))
        scrollbar.current = scrollbar.y_axis
    for i in brd.items:
        i.button.update()
        i.button.draw(WIN)
    for w in widgets:
        w.update()
        w.draw(WIN)
    scrollbar.draw(WIN)
    pygame.display.flip()
    # pygame.display.update()
pygame.quit()

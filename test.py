# import pygame
# pygame.init()
# clock = pygame.time.Clock()
# WIN = pygame.display.set_mode((540, 600))
# pygame.display.set_caption('')
# FPS = 20


# def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
#     return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


# # WIN.blit(PYtxt('Solved'), (20, 560) -> position)
# # pygame.display.update()
# # win.blit(text, (x + (colGap/2 - text.get_width()/2),
# #                 y + (rowGap/2 - text.get_height()/2)))
# run = True
# pygame.draw.rect(WIN, (220, 0, 0), pygame.Rect(540, 560, 540, 40))
# while run:
#     clock.tick(FPS)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#     pygame.display.update()
# pygame.quit()
# Importing the library
import pygame

# Initializing Pygame
pygame.init()

# Initializing surface
WIN = pygame.display.set_mode((540, 600))

# Initialing Color
color = (255, 0, 0)

# Drawing Rectangle
pygame.draw.rect(WIN, color, pygame.Rect(0, 540, 540, 60))
pygame.display.flip()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()

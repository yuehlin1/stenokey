import pygame as pg

WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("First game!")
FPS = 60

def draw_window():
    WIN.fill(WHITE)
    pg.display.update()

def main():
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run=False
    pg.quit()

if __name__ == "__main__":
    main()
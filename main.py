# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
import time
import random
from mazetile import mazetile

pygame.font.init()

WIDTH = 820
HEIGHT = 820
FPS = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

BORDER = 10
WALL_SIZE = 1

MAZE_WIDTH = 25
MAZE_HEIGHT = 25


## COLORMAP
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGD_COL = (216, 216, 216)
PALE_COL = (255, 255, 234)
DARK_COL = (31, 26, 56)
ACCENT_COL = (255, 94, 91)
NEUTRAL_COL = (123, 80, 111)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WINNER_FONT = pygame.font.SysFont('Arial', 100)




def draw_maze(tiles, size): # Draw maze at the start as white rectangle + tiles on top
    WIN.fill(BGD_COL)
    s = size - WALL_SIZE
    board = pygame.Rect(BORDER, BORDER, WIDTH-2*BORDER, HEIGHT-2*BORDER)
    pygame.draw.rect(WIN, PALE_COL, board)

    for t in tiles:
        right_passage = 0
        bottom_passage = 0
        if t.right:
            right_passage = WALL_SIZE
        if t.bottom:
            bottom_passage = WALL_SIZE
        tile = pygame.Rect(t.x + BORDER + WALL_SIZE,t.y + BORDER + WALL_SIZE,s + right_passage, s + bottom_passage)
        pygame.draw.rect(WIN, DARK_COL, tile)

    last_tile = pygame.Rect(tiles[-1].x + BORDER + WALL_SIZE + 5, tiles[-1].y + BORDER + WALL_SIZE + 5,
                            s - 10, s - 10)
    pygame.draw.rect(WIN, PALE_COL, last_tile)

    pygame.display.update()

def build_tiles(maze_width,maze_height):
    # Determine size of square
    s = min((WIDTH - 2*BORDER)//MAZE_WIDTH,(HEIGHT - 2*BORDER)//MAZE_HEIGHT)
    tiles = []

    for i in range(maze_width):
        for j in range(maze_height):
            tiles.append(mazetile(i*s, j*s))

    return s, tiles


def find_tile(tiles, step, x, y):
    if x < 0 or y < 0:
        return None

    xn = x//step
    yn = y//step

    if xn>=MAZE_WIDTH or yn>=MAZE_HEIGHT:
        return None
    if xn*MAZE_HEIGHT + yn >= len(tiles):
        return None
    return tiles[xn*MAZE_HEIGHT + yn]


def build_maze(tiles, step):
    stack = []
    visited = []

    # init
    cur_cell = tiles[0]
    stack.append(cur_cell)
    visited.append(cur_cell)

    while len(stack) > 0:
        cell = []

        # is TOP available?
        top_cell = find_tile(tiles, step,cur_cell.x, cur_cell.y - step)
        if top_cell and top_cell not in visited:
            cell.append("top")

        # is BOTTOM available?
        bottom_cell = find_tile(tiles, step, cur_cell.x, cur_cell.y + step)
        if bottom_cell and bottom_cell not in visited:
            cell.append("bottom")

        # is RIGHT available?
        right_cell = find_tile(tiles, step, cur_cell.x + step, cur_cell.y)
        if right_cell and right_cell not in visited:
            cell.append("right")

        # is LEFT available?
        left_cell = find_tile(tiles, step, cur_cell.x - step, cur_cell.y)
        if left_cell and left_cell not in visited:
            cell.append("left")

        if len(cell) > 0:
            cell_chosen = random.choice(cell)

            if cell_chosen == "top":
                cur_cell.top = top_cell
                top_cell.bottom = cur_cell
                cur_cell = top_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

            if cell_chosen == "bottom":
                cur_cell.bottom = bottom_cell
                bottom_cell.top = cur_cell
                cur_cell = bottom_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

            if cell_chosen == "right":
                cur_cell.right = right_cell
                right_cell.left = cur_cell
                cur_cell = right_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

            if cell_chosen == "left":
                cur_cell.left = left_cell
                left_cell.right = cur_cell
                cur_cell = left_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

        else:
            cur_cell = stack.pop()

    return tiles


def move_player(player, cur_tile, next_tile, s):

    tile = pygame.Rect(cur_tile.x + BORDER + WALL_SIZE, cur_tile.y + BORDER + WALL_SIZE,
                       s -WALL_SIZE, s-WALL_SIZE)
    pygame.draw.rect(WIN, DARK_COL, tile)
    # move player to next tile
    player.x = next_tile.x +5 + BORDER + WALL_SIZE
    player.y = next_tile.y +5 + BORDER + WALL_SIZE

    # draw_player
    pygame.draw.rect(WIN, ACCENT_COL, player)

    # update image
    pygame.display.update()
    return player, next_tile

def draw_winner():
    draw_text = WINNER_FONT.render("Bravo!", True, ACCENT_COL)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    step, tiles = build_tiles(MAZE_WIDTH, MAZE_HEIGHT)
    tiles = build_maze(tiles, step)
    draw_maze(tiles, step)

    cur_tile = tiles[0]
    cur_tile.visited = True
    player = pygame.Rect(cur_tile.x + 5 + BORDER + WALL_SIZE, cur_tile.y +5 + BORDER + WALL_SIZE,step -10,step -10)
    pygame.draw.rect(WIN,ACCENT_COL,player)
    pygame.display.update()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and cur_tile.top:
                    player, cur_tile = move_player(player,cur_tile,cur_tile.top,step)

                if event.key == pygame.K_DOWN and cur_tile.bottom:
                    player, cur_tile = move_player(player,cur_tile,cur_tile.bottom,step)

                if event.key == pygame.K_LEFT and cur_tile.left:
                    player, cur_tile = move_player(player,cur_tile,cur_tile.left,step)

                if event.key == pygame.K_RIGHT and cur_tile.right:
                    player, cur_tile = move_player(player,cur_tile,cur_tile.right,step)

        if cur_tile == tiles[-1]:
            draw_winner()
            break

    main()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

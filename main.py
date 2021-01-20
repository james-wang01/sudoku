import copy, sys, pygame
from random import randint, shuffle

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

BLACK = (0, 0 ,0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 230, 215)
BLOCK_HEIGHT = WINDOW_HEIGHT // 9
BLOCK_WIDTH = WINDOW_WIDTH // 9

pygame.font.init()
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 50)
screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption("Sudoku")

def valid(arr, row, col, num):
    # check row
    for r in arr[row]:
        if r == num:
            return False
    # check column
    for c in [r[col] for r in arr]:
        if c == num:
            return False
    # check box
    for i in range(row//3 * 3, row//3 * 3 + 3):
        for j in range(col//3 * 3, col//3 * 3 + 3):
            if arr[i][j] == num:
                return False
    return True

def backtrack(arr, row, col, sols, single = True, show = False):
    count = 0
    if arr[row][col] != 0:
        return backtrackNext(arr, row, col, sols, single, show)
    else:
        num_list = [i for i in range(1,10)]
        shuffle(num_list)
        for i in num_list:
            if valid(arr, row, col, i):
                arr[row][col] = i
                if show:
                    drawGrid()
                    pygame.draw.rect(screen, BLUE, (col*BLOCK_WIDTH,
                        row*BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT))
                    pygame.display.update()
                    pygame.time.wait(50)
                count += backtrackNext(arr, row, col, sols, single, show)
                if (single and count > 0):
                    return 1
                arr[row][col] = 0
        return count

def backtrackNext(arr, row, col, sols, single, show):
    if row == 8 and col == 8:
        sols.append(arr)
        return 1
    elif col == 8:
        return backtrack(arr, row + 1, 0, sols, single, show)
    else:
        return backtrack(arr, row, col + 1, sols, single, show)

def generateGrid():
    arr = [[0 for i in range(9)] for i in range(9)]
    solution = []
    backtrack(arr, 0, 0, solution)
    arr = copy.deepcopy(solution[0])
    solution = solution[0]
    removeNum(arr)
    return arr, solution

def removeNum(arr):
    global difficulty
    t = difficulty
    count = 81
    while(t > 0 and count > 16):
        n = randint(0, 80)
        row = n // 9
        col = n % 9
        if (arr[row][col] != 0):
            temp = arr[row][col]
            arr[row][col] = 0
            if backtrack(arr, 0, 0, [], False) != 1:
                arr[row][col] = temp
                t -= 1
            else:
                count -= 1

def drawGrid():
    blockHeight = WINDOW_HEIGHT // 9
    blockWidth = WINDOW_WIDTH // 9
    screen.fill(WHITE)
    for x in range(9):
        for y in range(9):
            if arr[y][x] != 0:
                pygame.draw.rect(screen, WHITE, (x*blockWidth, y*blockHeight,
                        blockWidth, blockHeight))
                text = font1.render(str(arr[y][x]), True, BLACK)
                screen.blit(text, (x*blockWidth + blockWidth / 2, y*blockHeight
                        + blockHeight / 2))
    for x in range(10):
        if (x % 3 == 0):
            thickness = 6
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (x*blockWidth, 0), (x*blockWidth,
            WINDOW_HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, x*blockHeight), (WINDOW_WIDTH,
            x*blockHeight), thickness)

def promptButton():
    drawGrid()
    ask = pygame.draw.rect(screen, WHITE, (75, 50, 450, 100))
    askText = font2.render("SHOW ALGORITHM?", True, BLACK)
    screen.blit(askText, (125, 100))
    show = pygame.Rect(50, 250, 200, 100)
    noShow = pygame.Rect(350, 250, 200, 100)
    pygame.draw.rect(screen, GREEN, show)
    yesText = font1.render("YES", True, BLACK)
    screen.blit(yesText, (100, 300))
    pygame.draw.rect(screen, RED, noShow)
    noText = font1.render("NO", True, BLACK) 
    screen.blit(noText, (400, 300))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if show.collidepoint(mousePos):
                    return True
                elif noShow.collidepoint(mousePos):
                    return False


def processInput(event):
    global accept, pos_x, pos_y
    val = -1
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        accept = 1
        pos_x, pos_y = pygame.mouse.get_pos()
        pos_x = pos_x // BLOCK_WIDTH
        pos_y = pos_y // BLOCK_HEIGHT
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            show = promptButton()
            showSolution(show)
        elif event.key == pygame.K_r:
            restart()
        elif event.key == pygame.K_n:
            newGame()
        elif accept == 1:
            if event.key == pygame.K_RIGHT:
                pos_x += 1
            elif event.key == pygame.K_LEFT:
                pos_x -= 1
            elif event.key == pygame.K_UP:
                pos_y += 1
            elif event.key == pygame.K_DOWN:
                pos_y -= 1
            elif event.key == pygame.K_1:
                val = 1
            elif event.key == pygame.K_2:
                val = 2
            elif event.key == pygame.K_3:
                val = 3
            elif event.key == pygame.K_4:
                val = 4
            elif event.key == pygame.K_5:
                val = 5
            elif event.key == pygame.K_6:
                val = 6
            elif event.key == pygame.K_7:
                val = 7
            elif event.key == pygame.K_8:
                val = 8
            elif event.key == pygame.K_9:
                val = 9
    if  val != -1:
        checkInput(val)

def checkInput(val):
    global pos_x, pos_y, solution, wrong
    if solution[pos_y][pos_x] == val:
        arr[pos_y][pos_x] = val
    else:
        wrong += 1

def newGame():
    global start, arr, solution
    start, solution = generateGrid()
    restart()

def restart():
    global start, arr, pos_x, pos_y
    pos_x = -1
    pos_y = -1
    arr = copy.deepcopy(start)

def showSolution(show = False):
    global arr, solution
    if show:
        backtrack(arr, 0, 0, sols=[], single=True, show=True)
    else:
        arr = copy.deepcopy(solution)

accept = 0
difficulty = 3
def main():
    newGame()
    print(solution)
    while True:
        drawGrid()
        for event in pygame.event.get():
            processInput(event)
        pygame.display.update()
        

if __name__ == "__main__":
    main()

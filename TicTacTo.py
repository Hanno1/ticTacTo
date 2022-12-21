import pygame
import time
import os

pygame.font.init()
WIDTH, HEIGHT = 900, 800
DIFFICULTY = 5
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# load images
player1 = pygame.image.load(os.path.join("assets", "player_1.png"))
player2 = pygame.image.load(os.path.join("assets", "player_2.png"))


def take_screenshot(screen):
    time_taken = time.asctime(time.localtime(time.time()))
    time_taken = time_taken.replace(" ", "_")
    time_taken = time_taken.replace(":", ".")
    save_file = "screenshots/" + time_taken + ".png"
    pygame.image.save(screen, save_file)
    print("take")


def artificial_int(matrix, number):
    """
    we use the min max principle to determine which move is the best
    :param matrix: current board
    :param number: player 1 or player 2
    :return: row and col for ai move
    """
    liste = []
    if number == 1:
        second_number = 2
    else:
        second_number = 1
    for i in range(0, 3):
        for j in range(0, 3):
            if matrix[i][j] == 0:
                matrix[i][j] = number
                l = mini(matrix, second_number, DIFFICULTY, number)
                liste.append([l, i, j])
                matrix[i][j] = 0
    maxi = liste[0][0]
    x_pos = liste[0][1]
    y_pos = liste[0][2]
    for element in liste:
        if element[0] > maxi:
            x_pos = element[1]
            y_pos = element[2]
    return x_pos, y_pos


def mini(matrix, number, iter, me):
    if number == 1:
        second_number = 2
    else:
        second_number = 1
    liste = []
    full = test_full(matrix)
    win, player = test_win(matrix)
    if iter == 0:
        return board_eval(matrix, me)
    elif full or win:
        if win:
            return board_eval(matrix, me)
        else:
            return 0
    else:
        for i in range(0, 3):
            for j in range(0, 3):
                if matrix[i][j] == 0:
                    matrix[i][j] = number
                    iter -= 1
                    m = mini(matrix, second_number, iter, me)
                    liste.append(m)
                    iter += 1
                    matrix[i][j] = 0
        if second_number == me:
            return min(liste)
        else:
            return max(liste)


def board_eval(matrix, number):
    """
    evaluates the board from sight of number
    :param matrix: board
    :param number: player
    :return: board evaluation
    """
    if number == 1:
        second_number = 2
    else:
        second_number = 1
    val = 0
    win, player = test_win(matrix)
    if win and player == number:
        return 1000
    elif win and player == second_number:
        return -1000
    else:
        for i in range(0, 3):
            if matrix[i][i] == number:
                val += 10
            elif matrix[i][i] == second_number:
                val -= 10
        if matrix[2][0] == number:
            val += 10
        elif matrix[2][0] == second_number:
            val -= 10
        if matrix[0][2] == number:
            val += 10
        elif matrix[0][2] == second_number:
            val -= 10
    return val


class Button:
    BUTTON_FONT = pygame.font.SysFont("comicSans", 50)

    def __init__(self, x, y, width, height, color, textcolor, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.textcolor = textcolor
        self.text = text

    def draw(self, window):
        button = self.BUTTON_FONT.render(self.text, True, self.textcolor)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        window.blit(button, (self.x + self.width / 2 - button.get_width() / 2,
                             self.y + self.height / 2 - button.get_height() / 2))

    def clicked(self, x_pos, y_pos):
        if self.x <= x_pos <= self.x + self.width and self.y <= y_pos <= self.y + self.height:
            return True
        else:
            return False


class GameButton(Button):

    def __init__(self, x, y, width, height, color, row=0, col=0):
        super().__init__(x, y, width, height, color, None, None)
        self.row = row
        self.col = col
        self.img = None

    def draw(self, window):
        if self.img is None:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        else:
            window.blit(self.img, (self.x, self.y))

    def set_image(self, player):
        if player == 1:
            self.img = player1
        elif player == 2:
            self.img = player2


def test_win(matrix):
    """
    :param matrix: parameter in game 1,2 or 0
    :return: game over or not
    """
    i = -1
    for i in range(1, 3):
        # test diagonals and cross
        if matrix[1][1] == i:
            if matrix[0][0] == i and matrix[2][2] == i:
                return True, i
            elif matrix[2][0] == i and matrix[0][2] == i:
                return True, i
            elif matrix[1][0] == i and matrix[1][2] == i:
                return True, i
            elif matrix[0][1] == i and matrix[2][1] == i:
                return True, i
        # tests rows and columns
        if matrix[0][0] == i:
            if matrix[1][0] == i and matrix[2][0] == i:
                return True, i
            elif matrix[0][1] == i and matrix[0][2] == i:
                return True, i
        if matrix[2][2] == i:
            if matrix[2][1] == i and matrix[2][0] == i:
                return True, i
            elif matrix[1][2] == i and matrix[0][2] == i:
                return True, i
    return False, i


def test_full(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if matrix[i][j] == 0:
                return False
    return True


def main(ai=False):
    run = True
    lost = False
    lost_count = 0
    draw = False
    FPS = 60
    main_font = pygame.font.SysFont("comicSans", 100)
    death_font = pygame.font.SysFont("comicSans", 80)

    player = 1
    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    offset = 50

    x = (WIDTH / 2 - 1 * WIDTH / 3 + offset, HEIGHT - 2 * WIDTH / 3 + offset)
    y = (WIDTH / 2 + 1 * WIDTH / 3 - offset, HEIGHT - 2 * WIDTH / 3 + offset)
    z = (WIDTH / 2 - 1 * WIDTH / 3 + offset, HEIGHT - offset)

    length = (2 * WIDTH / 3 - offset) / 3

    offset_button = 20
    button_length = length - 2 * offset_button
    buttons = []
    button00 = GameButton(x[0] + offset_button, x[1] + offset_button, button_length, button_length,
                          (0, 0, 0), 0, 0)
    button01 = GameButton(x[0] + length + offset_button, x[1] + offset_button, button_length, button_length,
                          (0, 0, 0), 0, 1)
    button02 = GameButton(x[0] + 2 * length + offset_button, x[1] + offset_button, button_length, button_length,
                          (0, 0, 0), 0, 2)
    button10 = GameButton(x[0] + offset_button, x[1] + length + offset_button, button_length, button_length,
                          (0, 0, 0), 1, 0)
    button11 = GameButton(x[0] + length + offset_button, x[1] + length + offset_button, button_length, button_length,
                          (0, 0, 0), 1, 1)
    button12 = GameButton(x[0] + 2 * length + offset_button, x[1] + length + offset_button, button_length,
                          button_length, (0, 0, 0), 1, 2)
    button20 = GameButton(x[0] + offset_button, x[1] + 2 * length + offset_button, button_length, button_length,
                          (0, 0, 0), 2, 0)
    button21 = GameButton(x[0] + length + offset_button, x[1] + 2 * length + offset_button, button_length,
                          button_length, (0, 0, 0), 2, 1)
    button22 = GameButton(x[0] + 2 * length + offset_button, x[1] + 2 * length + offset_button, button_length,
                          button_length, (0, 0, 0), 2, 2)

    buttons.append(button00)
    buttons.append(button01)
    buttons.append(button02)
    buttons.append(button10)
    buttons.append(button11)
    buttons.append(button12)
    buttons.append(button20)
    buttons.append(button21)
    buttons.append(button22)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.fill((0, 0, 0))

        for button in buttons:
            button.draw(WIN)

        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(x[0], x[1] + length, 3 * length, 10))
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(x[0], x[1] + 2 * length, 3 * length, 10))
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(x[0] + length, x[1], 10, 3 * length))
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect(x[0] + 2 * length, x[1], 10, 3 * length))

        title = main_font.render("Tic Tac Toe", True, (255, 255, 255))
        WIN.blit(title, (WIDTH/2 - title.get_width()/2 + 30, 50))
        if player == 1:
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(50, 50, player1.get_width(), player1.get_height()), 10)
        else:
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(WIDTH-player2.get_width()-50, 50, player2.get_width(), player2.get_height()), 10)
        WIN.blit(player1, (50, 50))
        WIN.blit(player2, (WIDTH-player2.get_width()-50, 50))

        if lost:
            lost_label_1 = death_font.render("You Won!", True, (0, 255, 0))
            lost_label_2 = death_font.render("You Lost!", True, (255, 0, 0))
            if player == 1:
                WIN.blit(lost_label_2, (WIDTH / 3 - lost_label_2.get_width(), 2*HEIGHT/3))
                WIN.blit(lost_label_1, (2 * WIDTH / 3, 2*HEIGHT/3))
            else:
                WIN.blit(lost_label_1, (WIDTH / 3 - lost_label_1.get_width(), 2*HEIGHT/3))
                WIN.blit(lost_label_2, (2 * WIDTH / 3, 2*HEIGHT/3))

        elif draw:
            draw_label = death_font.render("Draw!", True, (0, 0, 255))
            WIN.blit(draw_label, (WIDTH/2 - draw_label.get_width()/2, 150))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if lost or draw:
            lost_count += 1
            if lost_count > FPS:
                run = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.clicked(x_pos, y_pos) and button.img is None:
                        if player == 1:
                            matrix[button.row][button.col] = 1
                            button.set_image(1)
                            player = 2
                        elif player == 2:
                            matrix[button.row][button.col] = 2
                            button.set_image(2)
                            player = 1
                        break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            take_screenshot(WIN)

        if test_win(matrix)[0]:
            lost = True
        elif test_full(matrix):
            draw = True

        if ai and player == 2 and not lost and not draw:
            x_pos, y_pos = artificial_int(matrix, player)
            for b in buttons:
                if b.row == x_pos and b.col == y_pos and b.img is None:
                    b.set_image(2)
                    matrix[x_pos][y_pos] = 2
                    player = 1
                    break

        redraw_window()


def main_menu():
    run = True
    title_font = pygame.font.SysFont("comicSans", 100)
    button1 = Button(WIDTH/2-30-300, HEIGHT-200, 300, 80, (20, 20, 20), (230, 230, 230), "Single Player")
    button2 = Button(WIDTH/2+30, HEIGHT-200, 300, 80, (20, 20, 20), (230, 230, 230), "Multiplayer")
    while run:
        WIN.fill((0, 0, 0))

        WIN.blit(player1, (50, 50))
        WIN.blit(player2, (WIDTH - player2.get_width() - 50, 50))

        title = title_font.render("Tic Tac Toe", True, (255, 255, 255))
        WIN.blit(title, (WIDTH / 2 - title.get_width() / 2 + 30, 50))

        button1.draw(WIN)
        button2.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = pygame.mouse.get_pos()
                if button1.clicked(x_pos, y_pos):
                    main(True)
                if button2.clicked(x_pos, y_pos):
                    main()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            take_screenshot(WIN)


main_menu()

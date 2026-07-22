import tkinter as tk
import customtkinter as ctk

board_5mok = 15

Nothing = 0
Black = 1
White = 2

stone_count = 0
five_stone_count = 0


# 보드 만들기!! 걍 append 반복으로 만들었다
def CreateBorad():
    new_board = []

    for y in range(board_5mok):
        line = []

        for x in range(board_5mok):
            line.append(Nothing)

        new_board.append(line)

    return new_board


board = CreateBorad()
current_turn = Black

# 숫자값 플레이어 이름으로 변경
def GetName(player):
    if player == Black:
        return "흑돌"
    else:
        return "백돌"


# x y 좌표 범위 확인하기
def CheckXYBoard(x, y):
    if x < 0:
        return False

    if x >= board_5mok:
        return False

    if y < 0:
        return False

    if y >= board_5mok:
        return False

    return True


# 그 위치 빈칸인지 확인 (중복 칸이면 싫어요)
def EmptryPos(x, y):
    if board[y][x] == Nothing:
        return True

    return False


# 착수 가능한 곳만 보기
def CanPlaceStone(x, y):
    if CheckXYBoard(x, y) == False:
        return False

    if EmptryPos(x, y) == False:
        return False

    return True


# while문으로 돌면서 오목판 안에서만 계산 + 다른 돌 있으면 멈춤 -> 그리고 갯수 반환
def CountOneWayStone(x, y, move_x, move_y, player):
    count = 0

    next_x = x + move_x
    next_y = y + move_y

    while CheckXYBoard(next_x, next_y):
        if board[next_y][next_x] == player:
            count = count + 1
            next_x = next_x + move_x
            next_y = next_y + move_y
        else:
            break

    return count


# 위에 있는 CountOneWayStone 써서 갯수 세기
def CountStone(x, y, move_x, move_y, player):
    count = 1

    count = count + CountOneWayStone(x, y, move_x, move_y, player)
    count = count + CountOneWayStone(x, y, -move_x, -move_y, player)

    return count


# 그 값이 5 이상이면 이기게 처리
def CheckWin(x, y, player):
    horizontal = CountStone(x, y, 1, 0, player)
    vertical = CountStone(x, y, 0, 1, player)
    diagonal_down = CountStone(x, y, 1, 1, player)
    diagonal_up = CountStone(x, y, 1, -1, player)

    if horizontal >= 5:
        return True

    if vertical >= 5:
        return True

    if diagonal_down >= 5:
        return True

    if diagonal_up >= 5:
        return True

    return False


# 흑돌이 6개 이상 연결되는지 확인
def CheckSixMok(x, y, player):
    horizontal = CountStone(x, y, 1, 0, player)
    vertical = CountStone(x, y, 0, 1, player)
    diagonal_down = CountStone(x, y, 1, 1, player)
    diagonal_up = CountStone(x, y, 1, -1, player)

    if horizontal >= 6:
        return True

    if vertical >= 6:
        return True

    if diagonal_down >= 6:
        return True

    if diagonal_up >= 6:
        return True

    return False

def illegalMoveThree(x, y, player):
    three_stone_count = 0

    horizontal = CountStone(x, y, 1, 0, player)
    vertical = CountStone(x, y, 0, 1, player)
    diagonal_down = CountStone(x, y, 1, 1, player)
    diagonal_up = CountStone(x, y, 1, -1, player)

    if horizontal == 3:
        three_stone_count += 1

    if vertical == 3:
        three_stone_count += 1

    if diagonal_down == 3:
        three_stone_count += 1

    if diagonal_up == 3:
        three_stone_count += 1

    return three_stone_count >= 2

def illegalMoveFour(x, y, player):
    four_stone_count = 0

    horizontal = CountStone(x, y, 1, 0, player)
    vertical = CountStone(x, y, 0, 1, player)
    diagonal_down = CountStone(x, y, 1, 1, player)
    diagonal_up = CountStone(x, y, 1, -1, player)

    if horizontal == 4:
        four_stone_count += 1

    if vertical == 4:
        four_stone_count += 1

    if diagonal_down == 4:
        four_stone_count += 1

    if diagonal_up == 4:
        four_stone_count += 1

    return four_stone_count >= 2



# 현재 흑돌이면 백돌로 바꾸고 아니면 흑돌로 바꾸기
def ChangeTrun():
    global current_turn

    if current_turn == Black:
        current_turn = White
    else:
        current_turn = Black


# 한 칸의 크기와 돌 주변 여백
cell_size = 42
stone_margin = 4


# 오목판 선과 이미 놓인 돌을 다시 그리기
def DrawBoard():
    canvas.delete("all")

    board_size = board_5mok * cell_size

    for number in range(board_5mok + 1):
        position = number * cell_size
        canvas.create_line(position, 0, position, board_size)
        canvas.create_line(0, position, board_size, position)

    for y in range(board_5mok):
        for x in range(board_5mok):
            if board[y][x] != Nothing:
                DrawStone(x, y, board[y][x])


# 오목판 한 칸에 흑돌 또는 백돌 그리기
def DrawStone(x, y, player):
    left = x * cell_size + stone_margin
    top = y * cell_size + stone_margin
    right = (x + 1) * cell_size - stone_margin
    bottom = (y + 1) * cell_size - stone_margin

    if player == Black:
        canvas.create_oval(left, top, right, bottom, fill="black", outline="black")
    else:
        canvas.create_oval(left, top, right, bottom, fill="white", outline="gray")


# 오목판을 클릭한 위치를 x, y 좌표로 바꾸기
def ClickBoard(event):
    x = event.x // cell_size
    y = event.y // cell_size

    PlaceStone(x, y)


# GUI에서 실제로 돌을 두는 로직
def PlaceStone(x, y):
    global stone_count, game_finished

    if game_finished:
        return

    if CanPlaceStone(x, y) == False:
        status_label.configure(text="이미 돌이 있는 자리입니다.")
        return

    if current_turn == Black:
        board[y][x] = current_turn
        # 금수 검사 동안만 흑돌을 임시 처리 (이 부분 자꾸 두는 돌이 보여서 이 부분만 AI 도움 받음)

        if CheckSixMok(x, y, current_turn):
            board[y][x] = Nothing
            status_label.configure(text="흑돌 6목은 둘 수 없습니다.")
            return

        if illegalMoveThree(x, y, current_turn):
            board[y][x] = Nothing
            status_label.configure(text="흑돌 3-3 금수입니다.")
            return

        if illegalMoveFour(x, y, current_turn):
            board[y][x] = Nothing
            status_label.configure(text="흑돌 4-4 금수입니다.")
            return

        board[y][x] = Nothing

    board[y][x] = current_turn
    stone_count = stone_count + 1
    DrawBoard()

    if CheckWin(x, y, current_turn):
        status_label.configure(text=GetName(current_turn) + " 승리!")
        game_finished = True
        return

    if stone_count >= board_5mok * board_5mok:
        status_label.configure(text="무승부!")
        game_finished = True
        return

    ChangeTrun()
    status_label.configure(text=GetName(current_turn) + " 턴")


def ResetGame():
    global board, current_turn, stone_count, game_finished

    board = CreateBorad()
    current_turn = Black
    stone_count = 0
    game_finished = False

    DrawBoard()
    status_label.configure(text="흑돌 턴")

def GGTheGame():
    global game_finished

    if game_finished:
        return

    ChangeTrun()

    status_label.configure(text=GetName(current_turn) + " 승리!")

    game_finished = True
    


def StartGUI():
    global canvas, status_label, game_finished

    game_finished = False

    app = ctk.CTk()
    app.title("오목조목") 

    status_label = ctk.CTkLabel(app, text="흑돌 턴")
    status_label.pack(pady=10)  

    board_frame = ctk.CTkFrame(app)
    board_frame.pack(padx=10, pady=5)

    board_size = board_5mok * cell_size
    canvas = tk.Canvas(
        board_frame,
        width=board_size,
        height=board_size,
        background="#D4A15F",
        highlightthickness=0
    )
    canvas.pack(padx=10, pady=10)
    canvas.bind("<Button-1>", ClickBoard) # 반환 이벤트 잇는 커맨드였던거임!!!

    DrawBoard()

    reset_button = ctk.CTkButton(app, text="새 게임", command=ResetGame)
    reset_button.pack(pady=10)

    gg_button = ctk.CTkButton(app, text="항복", command=GGTheGame)
    gg_button.pack(pady = 20)

    app.mainloop()


if __name__ == "__main__":
    StartGUI()


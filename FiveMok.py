import tkinter as tk
import customtkinter as ctk

board_5mok = 15

Nothing = 0
Black = 1
White = 2

stone_count = 0


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


# 보드 출력 및 자릿수 계산 (숫자 자리 한칸씩 계속 밀려서 어려웠음)
# 칸 출력 & 종류 따라 백돌 흑돌 계산
def PrintBoard():
    print()
    print("   ", end="")

    for number in range(1, board_5mok + 1):
        if number < 10:
            print(" " + str(number), end=" ")
        else:
            print(str(number), end=" ")

    print()

    for y in range(board_5mok):
        if y + 1 < 10:
            print(" " + str(y + 1), end=" ")
        else:
            print(str(y + 1), end=" ")

        for x in range(board_5mok):
            if board[y][x] == Nothing:
                print(" -", end=" ")
            elif board[y][x] == Black:
                print(" ●", end=" ")
            elif board[y][x] == White:
                print(" ○", end=" ")

        print()

    print()


# 숫자값 플레이어 이름으로 변경
def GetName(player):
    if player == Black:
        return "흑돌"
    else:
        return "백돌"


# 좌표 입력 받기 & 예외처리 except로 해주기 (몰라서 찾아봤음)
def InputPos():
    text = input("좌표 입력 x,y : ")

    if text == "GG" or text == "gg" or text == "항복":
        return "항복"

    if "," not in text:
        return None

    data = text.split(",")

    if len(data) != 2:  # x y 2개 없으면 거르기
        return None

    try:
        x = int(data[0]) - 1
        y = int(data[1]) - 1
    except:
        return None

    return x, y


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


# 현재 흑돌이면 백돌로 바꾸고 아니면 흑돌로 바꾸기
def ChangeTrun():
    global current_turn

    if current_turn == Black:
        current_turn = White
    else:
        current_turn = Black


# 콘솔 버전도 남겨 둠. 지금 실행하면 아래 GUI 버전이 시작된다.
def PlayConsoleGame():
    global stone_count

    while True:
        PrintBoard()
        print(GetName(current_turn), "턴!")

        position = InputPos()

        if position == "항복":
            print(GetName(current_turn), "항복!")

            ChangeTrun()

            print(GetName(current_turn), "승리!")
            break

        if position == None:
            print("입력이 틀렸음... 예시: 1,3")
            continue

        x, y = position

        if CanPlaceStone(x, y) == False:
            print("둘 수 없는 위치!!")
            continue

        if current_turn == Black:
            board[y][x] = current_turn

            if CheckSixMok(x, y, current_turn):
                board[y][x] = Nothing
                print("6목 금수입니둥")
                continue

            board[y][x] = Nothing

        board[y][x] = current_turn
        stone_count = stone_count + 1

        if CheckWin(x, y, current_turn):
            PrintBoard()
            print(GetName(current_turn), "승리!")
            break

        if stone_count >= board_5mok * board_5mok:
            PrintBoard()
            print("무승부!")
            break

        ChangeTrun()


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

    # 흑돌은 기존 6목 금수 검사만 한다. 3-3, 4-4 규칙은 추가하지 않음.
    if current_turn == Black:
        board[y][x] = current_turn

        if CheckSixMok(x, y, current_turn):
            board[y][x] = Nothing
            status_label.configure(text="흑돌 6목은 둘 수 없습니다.")
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


def StartGUI():
    global canvas, status_label, game_finished

    game_finished = False

    app = ctk.CTk()
    app.title("오목")

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
    canvas.bind("<Button-1>", ClickBoard)

    DrawBoard()

    reset_button = ctk.CTkButton(app, text="새 게임", command=ResetGame)
    reset_button.pack(pady=10)

    app.mainloop()


if __name__ == "__main__":
    StartGUI()

board_5mok = 15

Nothing = 0
Black = 1
White = 2

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

    if "," not in text:
        return None

    data = text.split(",")

    if len(data) != 2: # x y 2개 없으면 거르기
        return None

    try: # 이 부분은 진짜 모르겠어서..........
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


# 현재 흑돌이면 백돌로 바꾸고 이미 채워져 있는 칸이면 반환
def ChangeTrun():
    global current_turn

    if current_turn == Black:
        current_turn = White
    else:
        current_turn = Black


# 실제 게임 실행되는 로직
while True:
    PrintBoard()
    print(GetName(current_turn), "턴!")

    position = InputPos()

    if position == None:
        print("입력이 틀렸음... 예시: 1,3")
        continue

    x, y = position

    if CanPlaceStone(x, y) == False:
        print("둘 수 없는 위치!!")
        continue

    board[y][x] = current_turn

    if CheckWin(x, y, current_turn):
        PrintBoard()
        print(GetName(current_turn), "승리!")
        break

    ChangeTrun()
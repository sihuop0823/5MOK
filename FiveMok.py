import tkinter as tk
import customtkinter as ctk

BoardSize = 15

Empty = 0
BlackStone = 1
WhiteStone = 2

StoneCount = 0


# 빈 오목판 만들기
def MakeBoard():
    NewBoard = []

    for Y in range(BoardSize):
        Row = []

        for X in range(BoardSize):
            Row.append(Empty)

        NewBoard.append(Row)

    return NewBoard


Board = MakeBoard()
CurrentTurn = BlackStone


def PrintBoard():
    print()
    print("   ", end="")

    for Number in range(1, BoardSize + 1):
        if Number < 10:
            print(" " + str(Number), end=" ")
        else:
            print(str(Number), end=" ")

    print()

    for Y in range(BoardSize):
        if Y + 1 < 10:
            print(" " + str(Y + 1), end=" ")
        else:
            print(str(Y + 1), end=" ")

        for X in range(BoardSize):
            if Board[Y][X] == Empty:
                print(" -", end=" ")
            elif Board[Y][X] == BlackStone:
                print(" ●", end=" ")
            elif Board[Y][X] == WhiteStone:
                print(" ○", end=" ")

        print()

    print()


def GetStoneName(Player):
    if Player == BlackStone:
        return "흑돌"
    else:
        return "백돌"


def GetInputPosition():
    InputText = input("좌표 입력 x,y : ")

    if InputText == "GG" or InputText == "gg" or InputText == "항복":
        return "항복"

    if "," not in InputText:
        return None

    PositionData = InputText.split(",")

    if len(PositionData) != 2:
        return None

    try:
        X = int(PositionData[0]) - 1
        Y = int(PositionData[1]) - 1
    except:
        return None

    return X, Y


def IsInsideBoard(X, Y):
    if X < 0:
        return False

    if X >= BoardSize:
        return False

    if Y < 0:
        return False

    if Y >= BoardSize:
        return False

    return True


def IsEmptyPosition(X, Y):
    if Board[Y][X] == Empty:
        return True

    return False


def CanPlaceStone(X, Y):
    if IsInsideBoard(X, Y) == False:
        return False

    if IsEmptyPosition(X, Y) == False:
        return False

    return True


def CountOneWayStone(X, Y, MoveX, MoveY, Player):
    Count = 0

    NextX = X + MoveX
    NextY = Y + MoveY

    while IsInsideBoard(NextX, NextY):
        if Board[NextY][NextX] == Player:
            Count = Count + 1
            NextX = NextX + MoveX
            NextY = NextY + MoveY
        else:
            break

    return Count


def CountStone(X, Y, MoveX, MoveY, Player):
    Count = 1

    Count = Count + CountOneWayStone(X, Y, MoveX, MoveY, Player)
    Count = Count + CountOneWayStone(X, Y, -MoveX, -MoveY, Player)

    return Count


def CheckWin(X, Y, Player):
    HorizontalCount = CountStone(X, Y, 1, 0, Player)
    VerticalCount = CountStone(X, Y, 0, 1, Player)
    DiagonalDownCount = CountStone(X, Y, 1, 1, Player)
    DiagonalUpCount = CountStone(X, Y, 1, -1, Player)

    if HorizontalCount >= 5:
        return True

    if VerticalCount >= 5:
        return True

    if DiagonalDownCount >= 5:
        return True

    if DiagonalUpCount >= 5:
        return True

    return False


def CheckSixMok(X, Y, Player):
    HorizontalCount = CountStone(X, Y, 1, 0, Player)
    VerticalCount = CountStone(X, Y, 0, 1, Player)
    DiagonalDownCount = CountStone(X, Y, 1, 1, Player)
    DiagonalUpCount = CountStone(X, Y, 1, -1, Player)

    if HorizontalCount >= 6:
        return True

    if VerticalCount >= 6:
        return True

    if DiagonalDownCount >= 6:
        return True

    if DiagonalUpCount >= 6:
        return True

    return False


def ChangeTurn():
    global CurrentTurn

    if CurrentTurn == BlackStone:
        CurrentTurn = WhiteStone
    else:
        CurrentTurn = BlackStone


def PlayConsoleGame():
    global StoneCount

    while True:
        PrintBoard()
        print(GetStoneName(CurrentTurn), "턴!")

        Position = GetInputPosition()

        if Position == "항복":
            print(GetStoneName(CurrentTurn), "항복!")

            ChangeTurn()

            print(GetStoneName(CurrentTurn), "승리!")
            break

        if Position == None:
            print("입력이 틀렸음... 예시: 1,3")
            continue

        X, Y = Position

        if CanPlaceStone(X, Y) == False:
            print("둘 수 없는 위치!!")
            continue

        if CurrentTurn == BlackStone:
            Board[Y][X] = CurrentTurn

            if CheckSixMok(X, Y, CurrentTurn):
                Board[Y][X] = Empty
                print("6목 금수입니둥")
                continue

            Board[Y][X] = Empty

        Board[Y][X] = CurrentTurn
        StoneCount = StoneCount + 1

        if CheckWin(X, Y, CurrentTurn):
            PrintBoard()
            print(GetStoneName(CurrentTurn), "승리!")
            break

        if StoneCount >= BoardSize * BoardSize:
            PrintBoard()
            print("무승부!")
            break

        ChangeTurn()


CellSize = 42
StoneMargin = 4


def DrawBoard():
    board_canvas.delete("all")

    BoardPixelSize = BoardSize * CellSize

    for Number in range(BoardSize + 1):
        LinePosition = Number * CellSize
        board_canvas.create_line(LinePosition, 0, LinePosition, BoardPixelSize)
        board_canvas.create_line(0, LinePosition, BoardPixelSize, LinePosition)

    for Y in range(BoardSize):
        for X in range(BoardSize):
            if Board[Y][X] != Empty:
                DrawStone(X, Y, Board[Y][X])


def DrawStone(X, Y, Player):
    Left = X * CellSize + StoneMargin
    Top = Y * CellSize + StoneMargin
    Right = (X + 1) * CellSize - StoneMargin
    Bottom = (Y + 1) * CellSize - StoneMargin

    if Player == BlackStone:
        board_canvas.create_oval(Left, Top, Right, Bottom, fill="black", outline="black")
    else:
        board_canvas.create_oval(Left, Top, Right, Bottom, fill="white", outline="gray")


def ClickBoard(MouseEvent):
    X = MouseEvent.x // CellSize
    Y = MouseEvent.y // CellSize

    PlaceStone(X, Y)


def PlaceStone(X, Y):
    global StoneCount, GameFinished

    if GameFinished:
        return

    if CanPlaceStone(X, Y) == False:
        turn_label.configure(text="이미 돌이 있는 자리입니다.")
        return

    if CurrentTurn == BlackStone:
        Board[Y][X] = CurrentTurn

        if CheckSixMok(X, Y, CurrentTurn):
            Board[Y][X] = Empty
            turn_label.configure(text="흑돌 6목은 둘 수 없습니다.")
            return

        Board[Y][X] = Empty

    Board[Y][X] = CurrentTurn
    StoneCount = StoneCount + 1
    DrawBoard()

    if CheckWin(X, Y, CurrentTurn):
        turn_label.configure(text=GetStoneName(CurrentTurn) + " 승리!")
        GameFinished = True
        return

    if StoneCount >= BoardSize * BoardSize:
        turn_label.configure(text="무승부!")
        GameFinished = True
        return

    ChangeTurn()
    turn_label.configure(text=GetStoneName(CurrentTurn) + " 턴")


def ResetGame():
    global Board, CurrentTurn, StoneCount, GameFinished

    Board = MakeBoard()
    CurrentTurn = BlackStone
    StoneCount = 0
    GameFinished = False

    DrawBoard()
    turn_label.configure(text="흑돌 턴")


def StartGui():
    global board_canvas, turn_label, GameFinished

    GameFinished = False

    app_window = ctk.CTk()
    app_window.title("오목")

    turn_label = ctk.CTkLabel(app_window, text="흑돌 턴")
    turn_label.pack(pady=10)

    board_frame = ctk.CTkFrame(app_window)
    board_frame.pack(padx=10, pady=5)

    BoardPixelSize = BoardSize * CellSize
    board_canvas = tk.Canvas(
        board_frame,
        width=BoardPixelSize,
        height=BoardPixelSize,
        background="#D4A15F",
        highlightthickness=0
    )
    board_canvas.pack(padx=10, pady=10)
    board_canvas.bind("<Button-1>", ClickBoard)

    DrawBoard()

    reset_btn = ctk.CTkButton(app_window, text="새 게임", command=ResetGame)
    reset_btn.pack(pady=10)

    app_window.mainloop()


if __name__ == "__main__":
    StartGui()

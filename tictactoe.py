#井字棋Tic Tac Toe
#author OraQra 2022-11-19
 
import random
 
# 显示打印棋盘
def display_Board(board,playerLetter):
    boardColor = [' ']*10
    for i in range(0,10):
        #玩家为绿色棋子 电脑为红色棋子
        if board[i] == playerLetter: 
            boardColor[i] = '\033[1;32;40m'+str(board[i])+'\033[0m'  
        else:
            boardColor[i] = '\033[1;31;40m'+str(board[i])+'\033[0m'
    print('\t\t\t┌──┬──┬──┐')
    print('\t\t\t│ '+boardColor[1]+'│ '+boardColor[2]+'│ '+boardColor[3]+'│')
    print('\t\t\t├──┼──┼──┤')
    print('\t\t\t│ '+boardColor[4]+'│ '+boardColor[5]+'│ '+boardColor[6]+'│')
    print('\t\t\t├──┼──┼──┤')
    print('\t\t\t│ '+boardColor[7]+'│ '+boardColor[8]+'│ '+boardColor[9]+'│')
    print('\t\t\t└──┴──┴──┘')
    print('----------------------------------------')

 
def playAgain():
    # 再玩一次？输入yes或y返回True
    print('\033[1;35;40m-------------------------------------------------------------\033[0m')
    print('想再来一局吗：(yes or no)')
    return input().lower().startswith('y')
 
#判断所给的棋子是否获胜 获胜返回Ture
def isWinner(board, letter):
    # 参数为棋盘上的棋子（列表）和棋子符号
    # 以下是所有可能胜利的情况，共8种
    ways_win = {(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9), (3,5,7)}
    for way in ways_win:
        if board[way[0]] == letter and board[way[1]] == letter and board[way[2]] == letter:
            return True
    return False
    
#复制一份棋盘
def getBoardCopy(board):
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard
    
#从最佳路径中按照顺序选取落子位置,
#如果没有选择None
def chooseMoveFormList(board,bestWays):
    for i in bestWays:
        if board[i] == ' ':
            return i;
    return None;

#随机返回一个可以落子的坐标 
#如果没有所给的位置列表movesList中没有可以落子的，返回None
def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if board[i] == ' ':
            possibleMoves.append(i)
 
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None
 
 #如果棋盘满了，返回True 
def isBoardFull(board):
    for i in range(1, 10):
        if board[i] == ' ':
            return False
    return True

#返回可落子的列表    
def legal_moves(board):
    moves = []
    for i in range(1,10):
        if board[i] == ' ':
            moves.append(i)
    return moves
    
 #获取玩家落子位置并且判断是否为合法位置
def getPlayerMove(board):
    move = input('请选择你要落子的位置(1-9)：')
    while True:
        if move in '1 2 3 4 5 6 7 8 9'.split():
            if board[int(move)] == ' ':
                break;
            else:
                move = input('此位置已经有棋子，请重新输入新位置：')
        else:
            move = input('请输入在1-9范围的位置数字：')
    return int(move)
    
#通过角获取角的1个远角(对角) 2个邻角 2个邻边等所在位置 用于电脑AL路径的选择
def getNode(Angle,Node):
    Nodelist = {1:[9,3,7,2,4],3:[7,1,9,2,6],7:[3,1,9,4,8],9:[1,3,7,6,8]}
    return Nodelist[Angle][Node]
  
#确定电脑的落子位置  #游戏AI核心算法:
def getComputerMove(board, computerLetter, playerLetter, whogoFirst, gameStep,bestWays,computerFirstStep):  

    # Tic Tac Toe AI核心算法:
    #----------------------最优路径选择算法--------------------------
    # 首先判断电脑方能否通过一次落子直接获得游戏胜利
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if copy[i] == ' ':
            copy[i] = computerLetter
            if isWinner(copy, computerLetter):
                return i
 
    # 判断玩家下一次落子能否获得胜利，如果能，给它堵上
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if copy[i] == ' ':
            copy[i] = playerLetter
            if isWinner(copy, playerLetter):
                return i
    
    #电脑先手 电脑的最优策略
    if whogoFirst=='computer':
        #电脑第一步占随机一个角 以此角作为判定其他对角 近边 邻角 
        if gameStep == 1:
            return computerFirstStep;
        
        #电脑第二步根据上一步玩家落子位置确定此局后续路径
        if gameStep == 3:
            cfp = computerFirstStep;
            #游戏第二步 即玩家下在边(2或4或6或8) 系统优先路径(中间，邻边，邻边)为最优策略 电脑必赢
            if board[2] == playerLetter or board[4] == playerLetter or board[6] == playerLetter or board[8] == playerLetter:
                allBestWays = [[5,getNode(cfp,3),getNode(cfp,4)],[5,getNode(cfp,4),getNode(cfp,3)]]
                bestWays.extend(random.choice(allBestWays))
                
            #游戏第二步 即玩家下在邻角  系统后续优先路径(对角)为最优策略 电脑必赢
            elif board[getNode(cfp,1)] == playerLetter or board[getNode(cfp,2)] == playerLetter:
                allBestWays = [[getNode(cfp,0)]]
                bestWays.extend(random.choice(allBestWays))
                
            #游戏第二步 即玩家下在对角  系统后续优先路径(邻角,邻角)为最优策略 电脑必赢
            elif board[getNode(cfp,0)] == playerLetter:
                allBestWays = [[getNode(cfp,1),getNode(cfp,2)],[getNode(cfp,2),getNode(cfp,1)]]
                bestWays.extend(random.choice(allBestWays))
                
        #执行优先路径策略 如果优先路径中所有路径位置都已经落子 则执行默认策略
        if chooseMoveFormList(board,bestWays)!= None:
            return chooseMoveFormList(board,bestWays)
        
    #玩家先手 电脑的最优策略
    else:
        #电脑第一步根据上一步玩家落子位置确定此局后续策略
        if gameStep == 2:
            #玩家先落边上(2或4或6或8) 系统后续优先路径(角，中间)为最优策略 电脑赢或者平
            if board[2] == playerLetter or board[4] == playerLetter or board[6] == playerLetter or board[8] == playerLetter :
                allBestWays = [[1,5],[3,5],[7,5],[9,5]]
                bestWays.extend(random.choice(allBestWays))
            #玩家先落角上 第二步电脑落中间
            #玩家先落中间 第二步电脑落角上
            else:
                bestWays.extend([5])
                
        #执行优先策略 如果关键策略中位置都已经落子 则执行默认策略
        if chooseMoveFormList(board,bestWays)!= None:
            return chooseMoveFormList(board,bestWays) 
    
    #默认策略 角优先 中心其次 边最后 不可更改 会影响上方最优策略选择
    # 如果角上能落子的话，在角上落子
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move
    # 如果能在中心落子的话，在中心落子
    if iboard[5] == ' ':
        return 5
    # 在边上落子
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])
 
 
import os
os.system("")

print('\033[1;35;40m--------------欢迎游玩不可能赢的井字棋！--------------\033[0m')

while True:
    #初始化棋盘
    theBoard = [' '] * 10
    #初始化电脑策略
    bestWays = []
    #初始化电脑第一步位置
    computerFirstStep = -1
    gameStep = 1
    
    #选择棋子
    playerLetter = input("请选择棋子 X 或 Y （X先走,Y后走）：").upper()
    if playerLetter == 'X':
        turn = 'player' #玩家先走
        computerLetter = 'Y'
    else:
        turn = 'computer' #电脑先走
        computerLetter = 'X'
        computerFirstStep = random.choice([1,3,7,9]) #电脑第一步位置为随机一个角
        
    print("{}先走！".format(turn))
    whogoFirst = turn 
    
    gameIsPlaying = True;
    #游戏中,循环轮流落子！
    while gameIsPlaying:
        if turn == 'player': # 玩家回合
            display_Board(theBoard,playerLetter)
            move = getPlayerMove(theBoard) #询问落子位置
            theBoard[move] = playerLetter #落子
            if isWinner(theBoard, playerLetter):  #判断是否获胜
                display_Board(theBoard,playerLetter)
                print('恭喜你获得胜利')
                gameIsPlaying = False;
            else:
                if isBoardFull(theBoard):
                    display_Board(theBoard,playerLetter)
                    print('游戏平局!')
                    gameIsPlaying = False;
                else:
                    turn = 'computer'
            gameStep+=1
        
        else:#电脑回合
            move = getComputerMove(theBoard, computerLetter, playerLetter, whogoFirst,gameStep,bestWays,computerFirstStep)
            theBoard[move] = computerLetter
            print('电脑落子的位置：'+str(move))
            if isWinner(theBoard, computerLetter):
                display_Board(theBoard,playerLetter)
                print('电脑打败了你，很遗憾你输了！')
                gameIsPlaying = False;
            else:
                if isBoardFull(theBoard):
                    display_Board(theBoard,playerLetter)
                    print('游戏平局!')
                    gameIsPlaying = False;
                else:
                    turn = 'player'
            gameStep+=1
        
    if not playAgain():
    #游戏重新开始或者结束
        print('\033[1;35;40m-------------------------Bye Bye！--------------------------\033[0m')
        print('')
        input('输入任意键退出游戏界面...')
        break
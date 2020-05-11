import numpy
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
AI = 2
PLAYER = 1


def create_board():
    # Create board and fill with zeros
    board = numpy.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


def play_move(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    # if location is 0 this means it is valid
    return board[ROW_COUNT-1][col] == 0


def get_next_row(board, col):
    # Get next free row
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r



def calculate_score(board, piece):
    # Calculate three score of AI
    three_score = check_three(board, AI) * 1000
    # Calculate two score of AI
    two_score = check_two(board, AI) * 10
    # Calculate three score of Player
    player_three_score = check_three(board, PLAYER) * 1000
    # Calculate two score of player
    player_two_score = check_two(board, PLAYER) * 10

    # Calculate final score by AI and Player's three's and two's
    score = two_score + three_score - player_two_score - player_three_score

    return score


def check_three(board, piece):
    # Count the how many three in a row piece has
    three_count = 0
    for r in range(ROW_COUNT-1):
        for c in range(COLUMN_COUNT-1):
            if c < COLUMN_COUNT-3:
                # Check horizantal right
                if board[r][c] == board[r][c+1] == board[r][c+2] == piece and board[r][c+3] == 0:
                    three_count += 1
                if r < ROW_COUNT-3:
                    # Check diagonal right
                    if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == piece and board[r+3][c+3] == 0:
                        three_count += 1
            if c >= 3:
                # Check horizantal left
                if board[r][c] == board[r][c-1] == board[r][c-2] == piece and board[r][c-3] == 0:
                    three_count += 1
                if r < ROW_COUNT-3:
                    # Check diagonal left
                    if board[r][c] == board[r+1][c-1] == board[r+2][c-2] == piece and board[r+3][c-3] == 0:
                        three_count += 1
            if r < ROW_COUNT-3:
                # Check vertical
                if board[r][c] == board[r+1][c] == board[r+2][c] == piece and board[r+3][c] == 0:
                    three_count += 1
    return three_count


def check_two(board, piece):
    # Count the how many two in a row piece has
    two_count = 0
    for r in range(ROW_COUNT-1):
        for c in range(COLUMN_COUNT-1):
            if c < COLUMN_COUNT-3:
                # Check horizantal right
                if board[r][c] == board[r][c+1] == piece and board[r][c+2] == board[r][c+3] == 0:
                    two_count += 1
                if r < ROW_COUNT-3:
                    # Check diagonal right
                    if board[r][c] == board[r+1][c+1] == piece and board[r+2][c+2] == board[r+3][c+3] == 0:
                        two_count += 1
            if c >= 3:
                # Check horizantal left
                if board[r][c] == board[r][c-1] == piece and board[r][c-2] == board[r][c-3] == 0:
                    two_count += 1
                if r < ROW_COUNT-3:
                    # Check diagonal left
                    if board[r][c] == board[r+1][c-1] == piece and board[r+2][c-2] == board[r+3][c-3] == 0:
                        two_count += 1
            if r < ROW_COUNT-3:
                # Check vertical
                if board[r][c] == board[r+1][c] == piece and board[r+2][c] == board[r+3][c] == 0:
                    two_count += 1
    return two_count


def pick_best_move(board, piece):

    playable_locations = find_playable_locations(board)
    best_score = float("-inf")
    best_col = random.choice(playable_locations)
    for col in playable_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        play_move(temp_board, row, col, piece)
        if win_check(temp_board, AI):
            score = 100000
        else:
            score = calculate_score(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def minimax(board, depth, alpha, beta, maximizingPlayer):
    # Find every playable locations
    playable_locations = find_playable_locations(board)
    # Check if game over or not
    is_terminal, winner = is_game_over(board)
    if depth == 0 or is_terminal:
        # if game over
        if is_terminal:
            # If AI win return 1000000 score
            if winner == AI:
                return (None, 1000000)
            # If Player win return -1000000 score
            elif winner == PLAYER:
                return (None, -1000000)
            else:
                # If no one win it means it is a tie, return 0 score
                return (None, 0)
        else:
            # If depth equals 0 return calculated score
            return (None, calculate_score(board, AI))
    if maximizingPlayer:
        value = float("-inf")
        column = random.choice(playable_locations)
        for col in playable_locations:
            row = get_next_open_row(board, col)
            # Create a temp board
            temp_board = board.copy()
            # Simulate the move
            play_move(temp_board, row, col, AI)
            # Go until terminal or deepest point
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = float("inf")
        column = random.choice(playable_locations)
        for col in playable_locations:
            row = get_next_open_row(board, col)
            # Create a temp board
            temp_board = board.copy()
            # Simulate the move
            play_move(temp_board, row, col, PLAYER)
            # Go until terminal or deepest point
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def find_playable_locations(board):
    # Find all playable locations
    playable_locations = []
    for col in range(COLUMN_COUNT):
        # If location is valid
        if is_valid_location(board, col):
            # Add it to playable locations
            playable_locations.append(col)
    return playable_locations


def print_board(board):
    print(numpy.flip(board, 0))


def is_game_over(board):
    # Check if game over or not
    # if player 1 wins game is over
    if win_check(board, PLAYER):
        return True, PLAYER
    # if player 2 wins game is over
    if win_check(board, AI):
        return True, AI
    # if there is no space to play game is over
    if len(find_playable_locations(board)) <= 0:
        return True, 0
    return False, -1


def win_check(board, piece):
    # Check for win
    # Check horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check diagonal right
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check diagonal left
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


game_over = False
board = create_board()
print_board(board)

turn = 0

AI_level = 0
AI_level = int(input("Choose AI level (0 = easy , 1 = hard) :"))

# Game Loop
while not game_over:
    if turn == 0:
        # Take input from player
        col = int(input("Player move (1,7) :"))
        # if input is valid
        if is_valid_location(board, col-1):
            print("PLAYER MOVE")
            row = get_next_row(board, col-1)
            # Make move
            play_move(board, row, col-1, PLAYER)
            # Pass turn to AI
            turn = 1
            print_board(board)
            if win_check(board, PLAYER):
                print("PLAYER WINS!")
                game_over = True

            print("----------")
        else:
            print("Column is full")
    else:
        print("AI MOVE")
        # Calculate AI's move using minimax algorithm
        if AI_level == 0:
            col = pick_best_move(board, AI)
        else:
            col, minimax_score = minimax(
                board, 5, float("-inf"), float("inf"), True)
        if is_valid_location(board, col):
            row = get_next_row(board, col)
            play_move(board, row, col, AI)
            turn = 0
            print_board(board)
            if win_check(board, AI):
                print("AI WINS!")
                game_over = True
            print("----------")
        else:
            print("Column is full")

from math import sqrt, floor, inf
from config import players, scores

class Stage:
    def __init__(self, board_string, curr_player):
        """
        A class that represents the current stage.

        board_string: board row by row encoded as a string
        curr_player: current player will make a move shortly
        """
        self.board_string = board_string
        self.d_2 = len(board_string)
        if not self.is_valid():
            raise ValueError("length(board_string) not perfect square")
        self.d = int(sqrt(self.d_2))
        self.curr_player = curr_player
        self.next_player = self.get_next_player(curr_player)

    def is_valid(self):
        """
        Returns True if the board string is valid, returns False otherwise.
        """
        if sqrt(self.d_2) != floor(sqrt(self.d_2)):
            return False
        else:
            return True

    def get_result(self):
        """
        Returns the winner if someone wins; tie if no one wins;
        or None if the game has not finished.
        """
        d = self.d
        board_list = list(self.board_string)
        all_pos = [list(range(d*i, d*(i+1))) for i in range(d)]
        all_pos.extend([[d*i+j for i in range(d)] for j in range(d)])
        all_pos.append([(d+1)*i for i in range(d)])
        all_pos.append([(d-1)*i for i in range(1, d+1)])
        for pos in all_pos:
            if all(board_list[pos[0]] == board_list[p] for p in pos):
                if board_list[pos[0]] == players['Empty']:
                    continue
                elif board_list[pos[0]] == self.curr_player:
                    return self.curr_player
                else:
                    return self.next_player
        for b in board_list:
            if b == players['Empty']:
                return None
        return players['Empty']
    
    def evaluate(self, board_list, player):
        d = self.d
        all_pos = [list(range(d*i, d*(i+1))) for i in range(d)]
        all_pos.extend([[d*i+j for i in range(d)] for j in range(d)])
        all_pos.append([(d+1)*i for i in range(d)])
        all_pos.append([(d-1)*i for i in range(1, d+1)])
        for pos in all_pos:
            if all(board_list[pos[0]] == board_list[p] for p in pos):
                if board_list[pos[0]] == player:
                    return scores['Win']
                elif board_list[pos[0]] == self.get_next_player(player):
                    return scores['Lose']
        return scores['Tie']
    
    def moves_left(self, board_list):
        for b in board_list:
            if b == players['Empty']:
                return True
        return False

    def minimax(self, board, depth: int, is_max: bool, player):
        score = self.evaluate(board, player)

        if score != scores['Tie']:
            return score

        if not self.moves_left(board):
            return scores['Tie']

        if is_max:
            best = -inf
            for i in range(self.d_2):
                if board[i] == players['Empty']:
                    board[i] = player
                    best = max(best, self.minimax(board, depth + 1, not is_max, player))
                    board[i] = players['Empty']
            return best
        else:
            best = inf
            for i in range(self.d_2):
                if board[i] == players['Empty']:
                    board[i] = self.get_next_player(player)
                    best = min(best, self.minimax(board, depth + 1, not is_max, player))
                    board[i] = players['Empty']
            return best
    
    def best_move(self, board, player):
        best_score = -inf

        for i in range(self.d_2):
            if board[i] == players['Empty']:
                board[i] = player
                score = self.minimax(board, 0, False, player)
                board[i] = players['Empty']

                if score > best_score:
                    best_move = i
                    best_score = score

        return best_move

    def get_next_player(self, player):
        if player == players['Human']:
            return players['Bot']
        else:
            return players['Human']

    def next_stage_human(self, row, col):
        """
        Returns a new stage after human makes a move.
        """
        board_list = list(self.board_string)
        if board_list[self.d*row + col] != players['Empty']:
            return Stage(self.board_string, self.curr_player)
        board_list[self.d*row + col] = self.curr_player
        board_string = ''.join(board_list)
        return Stage(board_string, self.next_player)
    
    def next_stage_bot(self):
        """
        Return a new stage after bot makes a move.
        Use the min-max algorithm.
        """
        board_list = list(self.board_string)
        best_move = self.best_move(board_list, self.curr_player)
        if board_list[best_move] != players['Empty']:
            return Stage(self.board_string, self.curr_player)
        board_list[best_move] = self.curr_player
        board_string = ''.join(board_list)
        return Stage(board_string, self.next_player)


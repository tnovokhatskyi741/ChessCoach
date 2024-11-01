import chess


class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            else:
                return False
        except:
            return False

    def get_board_fen(self):
        return self.board.fen()

    def get_board(self):
        return self.board

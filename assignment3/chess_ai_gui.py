
# Chess AI with minimax and a pygame GUI (falls back to ASCII if GUI fails)
import chess
import time
import sys
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

class PygameDisplay:
    def __init__(self, square_size=80):
        self.square_size = square_size
        self.window_size = square_size * 8
        self.screen = None
        self._quit = False
        # Unicode chess glyphs
        self.unicode_map = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }
        self.light_color = (240, 217, 181)
        self.dark_color  = (181, 136, 99)

    def start(self):
        pygame.init()
        pygame.display.set_caption("Chess AI - Simple GUI")
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        font_size = int(self.square_size * 0.75)
        self.font = pygame.font.SysFont("DejaVu Sans", font_size)
        self._quit = False
        return self

    def update(self, fen_or_board, game_board=None):
        if isinstance(fen_or_board, str):
            board = chess.Board(fen_or_board)
        elif isinstance(fen_or_board, chess.Board):
            board = fen_or_board
        else:
            board = chess.Board()

        for rank in range(8, 0, -1):
            for file in range(1, 9):
                x = (file - 1) * self.square_size
                y = (8 - rank) * self.square_size
                square_color = self.light_color if (file + rank) % 2 == 0 else self.dark_color
                pygame.draw.rect(self.screen, square_color,
                                 pygame.Rect(x, y, self.square_size, self.square_size))

        for square, piece in board.piece_map().items():
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            x = file * self.square_size
            y = (7 - rank) * self.square_size
            glyph = self.unicode_map.get(piece.symbol(), '?')
            text = self.font.render(glyph, True, (0, 0, 0))
            rect = text.get_rect(center=(x + self.square_size/2, y + self.square_size/2))
            self.screen.blit(text, rect)

        pygame.display.flip()

    def check_for_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._quit = True
        return self._quit

    def terminate(self):
        pygame.quit()
        self._quit = True


class ASCIIDisplay:
    def start(self): return None
    def update(self, fen_or_board, game_board=None):
        if isinstance(fen_or_board, str):
            b = chess.Board(fen_or_board)
        elif isinstance(fen_or_board, chess.Board):
            b = fen_or_board
        else:
            b = chess.Board()
        print("\n" + str(b) + "\n")
    def check_for_quit(self): return False
    def terminate(self): pass


if PYGAME_AVAILABLE:
    display_impl = PygameDisplay()
else:
    display_impl = ASCIIDisplay()

def start():
    global display_impl
    try:
        return display_impl.start()
    except Exception as e:
        print("GUI start failed, falling back to ASCII (reason):", e, file=sys.stderr)
        display_impl = ASCIIDisplay()
        return display_impl.start()

def update(fen_or_board, game_board=None):
    return display_impl.update(fen_or_board, game_board)

def check_for_quit():
    return display_impl.check_for_quit()

def terminate():
    return display_impl.terminate()


class State:
    def __init__(self, board=None, player=True):
        self.board = chess.Board() if board is None else board
        self.player = player  # True = White, False = Black

    def isTerminal(self):
        return self.board.is_game_over()

    def moveGen(self):
        children = []
        for move in self.board.legal_moves:
            new_board = self.board.copy()
            new_board.push(move)
            children.append(State(new_board, not self.player))
        return children

    def evaluate(self):
        if self.board.is_checkmate():
            return -10000 if self.player else 10000
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():
            return 0

        score = 0
        values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        for sq, piece in self.board.piece_map().items():
            val = values.get(piece.piece_type, 0)
            score += val if piece.color == chess.WHITE else -val

        centers = [chess.D4, chess.E4, chess.D5, chess.E5]
        for sq in centers:
            piece = self.board.piece_at(sq)
            if piece:
                score += 0.25 if piece.color == chess.WHITE else -0.25

        b = self.board.copy()
        b.turn = chess.WHITE
        wm = len(list(b.legal_moves))
        b.turn = chess.BLACK
        bm = len(list(b.legal_moves))
        score += 0.05 * (wm - bm)
        return score

def minimax(state, depth, alpha, beta, maximizingPlayer, maxDepth):
    if state.isTerminal() or depth == maxDepth:
        return state.evaluate(), None

    best_move = None
    if maximizingPlayer:  # White = MAX
        maxEval = float('-inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, False, maxDepth)
            if eval_score > maxEval:
                maxEval, best_move = eval_score, child.board.peek()
            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break
        return maxEval, best_move
    else:  # Black = MIN
        minEval = float('inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, True, maxDepth)
            if eval_score < minEval:
                minEval, best_move = eval_score, child.board.peek()
            beta = min(beta, eval_score)
            if alpha >= beta:
                break
        return minEval, best_move

# game loop

def play_game():
    current_state = State(player=True)
    maxDepth = 3
    game_board = start()

    print("Artificial Intelligence – Chess AI")
    print("You are White. Enter moves in UCI format (e.g., e2e4). Type 'quit' to exit.")

    while not current_state.isTerminal():
        update(current_state.board.fen(), game_board)
        if check_for_quit():
            break

        if current_state.player:
            move_uci = input("Enter your move: ")
            if move_uci.lower() == 'quit':
                break
            try:
                move = chess.Move.from_uci(move_uci)
                if move in current_state.board.legal_moves:
                    b = current_state.board.copy()
                    b.push(move)
                    current_state = State(b, False)
                else:
                    print(" move invalid!")
            except Exception:
                print("invalid format.use UCI like e2e4.")
        else:
            print("AI is thinking...")
            _, best_move = minimax(current_state, 0, float('-inf'), float('inf'), False, maxDepth)
            if best_move:
                b = current_state.board.copy()
                b.push(best_move)
                current_state = State(b, True)
                print(f"AI plays: {best_move.uci()}")

    print("\nGame over!")
    update(current_state.board.fen(), game_board)
    terminate()

if __name__ == "__main__":
    play_game()




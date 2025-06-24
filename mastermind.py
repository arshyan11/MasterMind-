import itertools
import pdb
import random
import pygame

# Constants
COLORS = ['Red', 'Green', 'Yellow', 'Blue', 'Purple', 'Orange']
WIDTH, HEIGHT = 800, 600  # Pygame window dimensions
CODE_LENGTH = 4
PEG_SIZE = 50  # Size of each peg in the visualization


def calculate_feedback(guess: tuple[str, ...], code: tuple[str, ...]) -> tuple[int, int]:
    """
    Calculate feedback for a given guess against the secret code.

    Args:
        guess (tuple): The guessed combination of colors.
        code (tuple): The actual secret code.

    Returns:
        tuple: (correct_position, correct_color)
            - correct_position (int): Number of pegs in the correct position.
            - correct_color (int): Number of pegs of correct color but wrong position.
    """
    # zip() function pairs the elements of guess and code
    # sum() function counts the number of correct positions
    # e.g., guess = ('Red', 'Green', 'Green', 'Blue') and code = ('Red', 'Red', 'Green', 'Yellow')
    # zip(guess, code) -> [('Red', 'Red'), ('Green', 'Red'), ('Green', 'Green'), ('Blue', 'Yellow')]
    # sum(g == c for g, c in zip(guess, code)) -> 2 (Red and Green are in the correct position)
    correct_position = sum(g == c for g, c in zip(guess, code))
    # set(guess) returns the unique colors in the guess. This is done to avoid double counting.
    # min() function determines whether the color exists in the guess or not. It will discard the extra colors.
    # sum() function counts the number of correct colors but wrong positions
    # Subtracting the correct_position from the total correct colors gives the correct colors but wrong positions
    # e.g., guess = ('Red', 'Green', 'Green', 'Blue') and code = ('Red', 'Red', 'Green', 'Yellow')
    # set(guess) -> {'Red', 'Green', 'Blue'}
    # sum(min(guess.count(color), code.count(color)) for color in set(guess)) -> 3 (Red, Green, and Green are correct)
    # correct_position = 2 (Red and Green are in the correct position)
    # correct_color = 3 - 2 = 1 (Green is correct but in the wrong position)
    correct_color = sum(min(guess.count(color), code.count(color)) for color in set(guess)) - correct_position
    return correct_position, correct_color


def draw_button(screen: pygame.Surface, rect: pygame.Rect, text: str, font: pygame.font.Font, color_map: dict[str, tuple[int, int, int]]):
    """Draw a button on the screen with readable text.

    Args:
        screen (pygame.Surface): The surface to draw on.
        rect (pygame.Rect): The rectangle defining the button.
        text (str): The text to display on the button.
        font (pygame.font.Font): The font to use for the text.
        color_map (dict): A dictionary mapping color names to RGB values

    :returns: None
    """
    pygame.draw.rect(screen, (200, 200, 200), rect)  # Light gray background
    pygame.draw.rect(screen, color_map['Black'], rect, 2)  # Black border of width 2
    text_surf = font.render(text, True, color_map['Black'])  # Black text. Anti-aliasing means smooth edges and it is enabled.
    # rect.x and rect.y are the top-left corner of the rectangle
    # rect.width and rect.height are the dimensions of the rectangle
    # rect.x + rect.width // 2 and rect.y + rect.height // 2 are the center of the rectangle
    text_rect = text_surf.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))  # Center the text
    screen.blit(text_surf, text_rect)  # Draw the text on the screen


class MastermindGame:
    """Manages the core logic of the Mastermind game."""

    def __init__(self, allow_duplicates: bool, code_length: int = 4):
        """Initialize the game with the given settings.

        Args:
            allow_duplicates (bool): Whether the secret code can have duplicate colors.
            code_length (int): Number of pegs in the secret code.

        Returns:
            None
        """
        self.allow_duplicates = allow_duplicates  # Whether the secret code can have duplicate colors
        self.code_length = code_length  # Number of pegs in the secret code
        self.all_codes = (
            list(itertools.product(COLORS, repeat=code_length))  # All possible codes with or without duplicates
            if allow_duplicates
            else list(itertools.permutations(COLORS, code_length))  # All possible codes without duplicates
        )
        self.secret_code = tuple(random.sample(COLORS, code_length))  # Randomly generated secret code
        self.possible_codes = self.all_codes[:]  # Copy the all_codes list to initialize the possible_codes list
        self.guesses = []  # List to store all guesses made by the agent
        self.feedbacks = []  # List to store the feedback for each guess

    def play_turn(self, guess: tuple[str, ...]) -> bool:
        """Make a guess and get feedback. Returns True if the game is solved.

        Args:
            guess (tuple): The guessed combination of colors.

        Returns:
            bool: True if the game is solved, False otherwise
        """
        feedback = calculate_feedback(guess, self.secret_code)  # Calculate feedback for the guess
        self.guesses.append(guess)  # Add the guess to the list of guesses
        self.feedbacks.append(feedback)  # Add the feedback to the list of feedbacks

        # Check if the code has been solved
        # If the feedback is (4, 0), it means that all the colors are correct and in the correct position
        if feedback == (self.code_length, 0):
            return True

        # Filter possible codes based on feedback
        # This will reduce the solution space by eliminating codes that do not match the feedback
        self.possible_codes = [code for code in self.possible_codes if calculate_feedback(guess, code) == feedback]
        return False  # Game is not solved yet

    def next_guess(self) -> tuple[str, ...]:
        """Get the next guess using the minimax strategy.

        Returns:
            tuple: The next guess to make.
        """
        # If only one code remains, it must be the solution
        if len(self.possible_codes) == 1:
            return self.possible_codes[0]
        # Use Minimax strategy to select the next guess
        print('MiniMax Guess')
        return self._minimax_guess()

    def _minimax_guess(self) -> tuple[str, ...]:
        """Find the guess that minimizes the maximum eliminations.

        Returns:
            tuple: The next guess to make.
        """
        best_guess = None  # Initialize the best guess
        min_max_eliminations = float('inf')  # Initialize the minimum maximum eliminations. It means the maximum number of codes that can be eliminated.

        # Iterate over all possible codes to determine the best guess
        i=1
        for guess in self.all_codes:
            print(f'Guess {i} / {len(self.all_codes)}')
            i+=1
            # Dictionary to store feedback counts
            feedback_counts = {}

            # Simulate feedback for this guess against all possible codes
            for code in self.possible_codes:
                feedback = calculate_feedback(guess, code)  # Calculate feedback for the guess
                feedback_counts[feedback] = feedback_counts.get(feedback, 0) + 1  # Count the feedback

            # Calculate the maximum eliminations for this guess
            # This is done to determine the guess that will eliminate the maximum number of codes
            max_eliminations = max(feedback_counts.values())

            # Select the guess that minimizes the maximum eliminations
            if max_eliminations < min_max_eliminations:
                min_max_eliminations = max_eliminations
                best_guess = guess
        # e.g., possible_codes = [('Red', 'Red', 'Green', 'Green'), ('Red', 'Green', 'Green', 'Red')]
        # all_codes = [('Red', 'Red', 'Red', 'Red'), ('Red', 'Red', 'Red', 'Green'), ('Red', 'Red', 'Red', 'Yellow'), ...]
        # guess = ('Red', 'Red', 'Red', 'Red')
        # feedback_counts = {(4, 0): 1, (3, 0): 6, (2, 0): 12, (1, 0): 6, (0, 0): 1, (2, 1): 6, (1, 1): 6, (0, 1): 6}
        # max_eliminations = 12
        # min_max_eliminations = 6
        # best_guess = ('Red', 'Red', 'Red', 'Green')
        return best_guess


class GameUI:
    """Handles the user interface and interactions for the Mastermind game."""

    def __init__(self):
        """Initialize the Pygame window and fonts."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Mastermind Solver')
        self.font = pygame.font.Font(None, 36)
        self.color_map = {
            'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Yellow': (255, 255, 0),
            'Blue': (0, 0, 255),
            'Purple': (128, 0, 128),
            'Orange': (255, 165, 0),
            'Black': (0, 0, 0),
            'White': (255, 255, 255),
        }

    def show_menu(self) -> bool | None:
        """Display the main menu to ask if duplicates are allowed.

        Returns:
            bool: True if duplicates are allowed, False otherwise
        """
        allow_duplicates = None
        # Loop until the user selects an option. Loop actually keeps the window open.
        while allow_duplicates is None:
            self.screen.fill(self.color_map['White'])  # Fill the screen with white color
            question_text = self.font.render('Allow duplicates in the secret code?', True, self.color_map['Black'])
            self.screen.blit(question_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))  # Draw the question text

            yes_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 80, 40)
            no_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2, 80, 40)
            draw_button(self.screen, yes_button, 'Yes', self.font, self.color_map)
            draw_button(self.screen, no_button, 'No', self.font, self.color_map)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(event.pos):
                        allow_duplicates = True
                    elif no_button.collidepoint(event.pos):
                        allow_duplicates = False

            pygame.display.flip()  # Update the display
        return allow_duplicates

    def draw_guess(self, guess: tuple[str, ...], feedback: tuple[int, int], row: int):
        """Draw a guess and its feedback on the screen.

        Args:
            guess (tuple): The guessed combination of colors.
            feedback (tuple): The feedback for the guess.
            row (int): The row number to display the guess.

        Returns:
            None
        """
        x_offset = 50  # Horizontal offset for the guess. It is the distance from the left edge of the window.
        # PEG_SIZE is the diameter of the peg.
        # PEG_SIZE + 10 is the distance between two peg
        # row * (PEG_SIZE + 10) is the vertical offset for the guess. It is the distance from the top edge of the window.
        y_offset = 60 + row * (PEG_SIZE + 10)  # Vertical offset for the guess. It is the distance from the top edge of the window.

        # Draw the guess pegs
        for i, color in enumerate(guess):
            # i * (PEG_SIZE + 10) Adds the horizontal offset for each peg from the previous peg and x_offset is the initial offset from the left edge of the window.
            # y_offset is the vertical offset for the guess.
            # PEG_SIZE // 2 is the radius of the peg.
            pygame.draw.circle(self.screen, self.color_map[color], (x_offset + i * (PEG_SIZE + 10), y_offset), PEG_SIZE // 2)

        feedback_text = self.font.render(f'Correct: {feedback[0]} | Misplaced: {feedback[1]}', True, self.color_map['Black'])
        # CODE_LENGTH * (PEG_SIZE + 20) is the total width of the guess area (Circle + Padding).
        # x_offset + CODE_LENGTH * (PEG_SIZE + 20) is the distance from the left edge of the window.
        self.screen.blit(feedback_text, (x_offset + CODE_LENGTH * (PEG_SIZE + 20), y_offset - 10))

    def fade_overlay(self):
        """Draw a semi-transparent overlay to fade the background."""
        overlay = pygame.Surface((WIDTH, HEIGHT))  # Create a new surface with the same dimensions as the window
        overlay.set_alpha(150)  # Set the transparency level (0-255)
        overlay.fill(self.color_map['Black'])  # Fill the surface with black color
        self.screen.blit(overlay, (0, 0))  # Draw the overlay on the screen in the top-left corner

    def restart_screen(self, game: MastermindGame) -> bool:
        """Display the restart screen over the solved solution.

        Args:
            game (MastermindGame): The Mastermind game object.

        Returns:
            bool: True if the game should be restarted, False if the game should be exited.
        """
        while True:
            self.screen.fill(self.color_map['White'])

            # Draw all guesses and feedbacks
            for i, (guess, feedback) in enumerate(zip(game.guesses, game.feedbacks)):
                self.draw_guess(guess, feedback, i)
            self.fade_overlay()  # Fade the background

            restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 100, 40)  # At left of the center
            exit_button = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 - 30, 80, 40)  # At right of the center
            draw_button(self.screen, restart_button, 'Restart', self.font, self.color_map)
            draw_button(self.screen, exit_button, 'Exit', self.font, self.color_map)

            pygame.display.flip()  # Update the display

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        return True
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        return False


def run_game():
    """
    Run the Mastermind game with the agent making guesses.

    Returns:
        None
    """
    ui = GameUI()
    while True:
        allow_duplicates = ui.show_menu()
        if allow_duplicates is None:
            return  # Exit the game if the user closes the window

        game = MastermindGame(allow_duplicates, CODE_LENGTH)
        solved = False

        while not solved:
            ui.screen.fill(ui.color_map['White'])

            # Draw all guesses and feedbacks
            for i, (guess, feedback) in enumerate(zip(game.guesses, game.feedbacks)):
                ui.draw_guess(guess, feedback, i)

            # If no guesses have been made, use the default guess
            if not game.guesses:
                # Initial guess is fixed (Knuth's recommendation)
                # This guess is because it will eliminate the maximum number of codes as suggested by Knuth
                # Calculate the number of repetitions needed for the initial guess
                half_length = CODE_LENGTH // 2
                initial_guess = tuple(COLORS[0] if i < half_length else COLORS[1] for i in range(CODE_LENGTH))

                # Use the dynamic initial guess
                guess = initial_guess
            else:
                # Get the next guess using the minimax strategy
                guess = game.next_guess()

            solved = game.play_turn(guess)
            pygame.display.flip()
            pygame.time.delay(2000)  # Delay to show the guess and feedback

        if not ui.restart_screen(game):
            break  # Exit the game if the user closes the window or selects Exit

    pygame.quit()


if __name__ == '__main__':
    run_game()

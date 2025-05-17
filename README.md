# Pygame AI vs AI Chess Game

## 📖 Overview

This project is a fully automated chess game where two AI opponents play against each other. The game is built using Python and the Pygame library for the graphical user interface. You can sit back and watch the AIs battle it out on the chessboard!

The AI uses the Minimax algorithm with alpha-beta pruning to determine its moves. While not at the level of professional chess engines like Stockfish, it provides a demonstration of classic game tree search in action.

## ✨ Features

* **Graphical User Interface:** A visual chessboard rendered using Pygame.
* **Automated Gameplay:** Two AI players (White and Black) play against each other.
* **AI Opponent:** Implements the Minimax algorithm with alpha-beta pruning.
    * Configurable search depth for the AI.
* **Visual "Thinking" Process:** A configurable delay is introduced when an AI is "thinking" to make the game flow more observable.
* **Standard Chess Rules:** Includes basic piece movements (Pawn, Rook, Knight, Bishop, Queen, King).
    * Basic pawn promotion (auto-promotes to Queen).
* **Check Detection:** Identifies when a King is in check.
* **Checkmate and Stalemate Detection:** The game correctly identifies checkmate and stalemate conditions to end the game.
* **Clear Game Status Display:** Shows whose turn it is, check status, and game over messages.

## 🛠️ Technologies Used

* **Python 3:** The core programming language.
* **Pygame:** A cross-platform set of Python modules designed for writing video games. Used for graphics, event handling, and sound (though sound is not currently implemented).

## ⚙️ Setup and Installation

1.  **Ensure Python is Installed:**
    You'll need Python 3.6 or newer. You can download it from [python.org](https://www.python.org/downloads/).

2.  **Install Pygame:**
    Open your terminal or command prompt and install Pygame using pip:
    ```bash
    pip install pygame
    ```

3.  **Clone the Repository (Optional, if you have the files locally):**
    If you're getting this from GitHub:
    ```bash
    git clone [https://github.com/YourUsername/YourRepositoryName.git](https://github.com/YourUsername/YourRepositoryName.git)
    cd YourRepositoryName
    ```
    (Replace `YourUsername/YourRepositoryName` with the actual path to your repository)

4.  **Project Files:**
    Ensure you have the main Python script (e.g., `chess_game_ai.py` or `Basics.py` as seen in previous discussions) in your project directory.

## 🚀 How to Run the Game

1.  Navigate to the project directory in your terminal.
2.  Run the main Python script:
    ```bash
    python your_chess_script_name.py
    ```
    (Replace `your_chess_script_name.py` with the actual name of your Python file, e.g., `Basics.py`)

The game window will open, and the AI players will start their match.

## 🔧 Customization

You can modify the behavior of the game and the AI by changing the constants at the top of the Python script:

* `PLAYER_WHITE_IS_AI = True`
* `PLAYER_BLACK_IS_AI = True`
    * Set these to `False` if you want to re-introduce human player control for either side (requires re-enabling mouse input logic in the main loop).
* `AI_DEPTH = 2`
    * Controls how many moves ahead the AI looks. Higher values mean stronger AI but significantly slower thinking times. `2` or `3` is generally reasonable for this Python implementation.
* `AI_THINKING_DURATION = 5000`
    * The duration in milliseconds (e.g., 5000ms = 5 seconds) that the game will pause and display "[Color] is thinking..." before the AI makes its move.

## 📦 Creating an Executable (Standalone Game)

You can create a standalone executable file so that the game can be run on computers without Python or Pygame installed. We recommend using **PyInstaller**.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Navigate to your script's directory in the terminal.**
3.  **Run PyInstaller:**
    For a single executable file without a console window (recommended for games):
    ```bash
    pyinstaller --onefile --windowed your_chess_script_name.py
    ```
4.  **Find your executable:**
    The executable will be located in the `dist` folder that PyInstaller creates.

    *(For more details on PyInstaller, including handling assets or troubleshooting, please refer to the [PyInstaller documentation](https://pyinstaller.readthedocs.io/en/stable/) or the "Guide to Creating a Pygame Executable" provided earlier.)*

## 🔮 Potential Future Enhancements

* **More Sophisticated AI Evaluation Function:** Include positional awareness, king safety, pawn structure, control of center, etc.
* **Opening Book:** Implement a basic opening book for the AI.
* **Endgame Tablebases:** For perfect play in certain endgame scenarios (very advanced).
* **Move History / PGN Export:** Display a list of moves made and allow exporting them.
* **Selectable Piece Promotion:** Allow the player (if human) or AI to choose which piece to promote a pawn to.
* **Implement All Special Moves:** Castling, En Passant.
* **Sound Effects:** Add sounds for moves, checks, captures.
* **UI Improvements:** More polished graphics, options menu, ability to reset the game or choose AI difficulty.
* **Human vs. AI Mode:** Easily switch between AI vs. AI and Human vs. AI.

## 🙏 Acknowledgements

* **Pygame Community:** For the excellent Pygame library.
* **Unicode Chess Pieces:** The visual representation of pieces relies on standard Unicode characters.

---

Happy Watching!

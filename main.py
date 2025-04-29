import argparse
from game.game_logic import Game

def main():
    parser = argparse.ArgumentParser(description="Duck Hunt Game")
    parser.add_argument('--difficulty', choices=['easy', 'hard'], default='easy', help='Виберіть рівень складності')
    args = parser.parse_args()

    game = Game(difficulty=args.difficulty)
    game.start()

if __name__ == "__main__":
    main()
import pygame
import classes
import time
import random
import csv

def main():
    (width, height) = (600, 400)
    screen = pygame.display.set_mode((width, height))
    ref_piece = classes.GamePiece(-100,-100)
    num_pieces_width = round(width/ref_piece.width)
    num_pieces_height = round(height/ref_piece.height)
    num_threads =2
    pieces = []

    for row_num in range(num_pieces_height):
        pieces.append([])
        for col_num in range(num_pieces_width):
            pieces[row_num].append(classes.GamePiece(ref_piece.width * col_num, ref_piece.height * row_num))
            pieces[row_num][col_num].alive = random.getrandbits(1)

    handler = classes.GameHandler(pieces)
    generations = 0
    max_generations = 200
    running = True
    start = time.time()
    while running:
        generations += 1
        handler.apply_rules_mp(num_threads)
        for row in pieces:
            for piece in row:
                piece.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if generations >= max_generations:
            running = False
    end = time.time()
    time_to_finish = end - start
    gen_per_s = generations/time_to_finish
    print(f"Program took {round(time_to_finish, 4)}s to complete with {round(gen_per_s, 4)} generations per second")
    with open("program_log.txt", "a", newline="") as log_file:
        csv_writer = csv.writer(log_file)
        csv_writer.writerow([
            time_to_finish,
            generations,
            gen_per_s,
            f"{width}*{height}",
            f"{ref_piece.width}*{ref_piece.height}",
            num_pieces_width*num_pieces_height,
            num_threads])

if __name__ == '__main__':
    main()

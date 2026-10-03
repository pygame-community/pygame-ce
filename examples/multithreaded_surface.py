import random
import sys
import threading
from time import perf_counter

import numpy
import pygame

pygame.init()

print(f"{sys._is_gil_enabled() = }")

WIDTH, HEIGHT = 100, 100
NUM_THREADS = 10
surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill("black")

LERP_OFFSET = 0.01


def get_random_color() -> pygame.Color:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = 255
    return pygame.Color(r, g, b, a)


def multithreaded_func(
    surf: pygame.Surface, target_pixel: tuple[int, int], target_color: pygame.Color
) -> None:
    lerp_distance = 0

    original_color = surf.get_at(target_pixel)

    while (surf.get_at(target_pixel) != target_color) and lerp_distance < 1:
        lerp_distance += LERP_OFFSET
        new_color = original_color.lerp(target_color, lerp_distance)
        surf.set_at(target_pixel, new_color)


if "--load" not in sys.argv:
    pixels = [(col, row) for col in range(WIDTH) for row in range(HEIGHT)]
    colors = [get_random_color() for _ in range(WIDTH * HEIGHT)]
    with open("params.txt", "w") as param_file:
        lines = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                color = colors[y * WIDTH + x]
                lines.append(f"{x};{y};{color.r};{color.g};{color.b};{color.a}\n")
        param_file.writelines(lines)
else:
    with open("params.txt", "r") as param_file:
        pixels = []
        colors = []
        lines = param_file.readlines()
        for line in lines:
            split_line = line.strip().split(";")
            x = int(split_line[0])
            y = int(split_line[1])
            color = pygame.Color("white")
            color.r = int(split_line[2])
            color.g = int(split_line[3])
            color.b = int(split_line[4])
            color.a = int(split_line[5])
            pixel = (x, y)

            pixels.append(pixel)
            colors.append(color)


args = [(pixel, colors[i]) for i, pixel in enumerate(pixels)]
batches = {
    i: args[i * NUM_THREADS : (i + 1) * NUM_THREADS]
    for i in range(WIDTH * HEIGHT // NUM_THREADS)
}

start = perf_counter()
for batch in batches.values():
    threads: list[threading.Thread] = []
    for pixel, color in batch:
        new_thread = threading.Thread(
            target=multithreaded_func, args=(surface, pixel, color)
        )
        new_thread.start()
        threads.append(new_thread)

    for t in threads:
        t.join()
end = perf_counter()

pygame.image.save(pygame.transform.scale_by(surface, 10), "out.png")

print(f"time taken: {end - start}")

for pixel, color in zip(pixels, colors):
    surface.set_at(pixel, color)
pygame.image.save(pygame.transform.scale_by(surface, 10), "comparison.png")

threaded_surf = pygame.image.load("out.png")
compare_surf = pygame.image.load("comparison.png")

threaded_arr = pygame.surfarray.array3d(threaded_surf)
compare_arr = pygame.surfarray.array3d(compare_surf)

threaded_alpha = pygame.surfarray.array_alpha(threaded_surf)
compare_alpha = pygame.surfarray.array_alpha(compare_surf)

numpy.testing.assert_array_equal(threaded_arr, compare_arr)
numpy.testing.assert_array_equal(threaded_alpha, compare_alpha)

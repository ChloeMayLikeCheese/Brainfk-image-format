import pygame
import re

def brainfk_to_int(bf):
    count = 0
    factor = 1
    for char in reversed(bf):
        if char == '+':
            count += factor
        elif char == '>':
            factor *= 10
    return count

def parse_bfif_file(input_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    pixels = []
    resolution = (0, 0)
    
    for line in lines:
        if line.startswith("Resolution:"):
            resolution_match = re.search(r"Resolution: (\d+)x(\d+)", line)
            if resolution_match:
                width = int(resolution_match.group(1))
                height = int(resolution_match.group(2))
                resolution = (width, height)
                print(f"Resolution found: {width}x{height}")
        elif line.startswith("`~") and line.endswith("~`\n"):
            continue
        elif line.startswith("`Width: ~") or line.startswith("`Height: ~"):
            continue
        else:
            match = re.search(r"`~(.+)~` @ ~(.+)~ # ~(.+)~ $ ~(.+)~", line)
            if match:
                r = brainfk_to_int(match.group(2))
                g = brainfk_to_int(match.group(3))
                b = brainfk_to_int(match.group(4))
                pixels.append((r, g, b))
                # Debug print
                print(f"Pixel parsed: R={r} G={g} B={b}")

    return pixels, resolution

def display_image(pixels, resolution):
    pygame.init()
    width, height = resolution
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('bfif viewer')

    # Create surface to draw pixels
    surface = pygame.Surface((width, height))

    # Set pixel colors
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if index < len(pixels):
                color = pixels[index]
                # Ensure color values are within valid range
                color = tuple(min(255, max(0, c)) for c in color)
                surface.set_at((x, y), color)
            else:
                # Default to black if index is out of range
                surface.set_at((x, y), (0, 0, 0))
    
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    # Main loop to keep the window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    input_path = '/home/chloe/Documents/Image-Test/test.bfif'  # Replace with your input .bfif file path
    pixels, resolution = parse_bfif_file(input_path)
    
    if resolution == (0, 0):
        print("Error: Resolution not found in the .bfif file.")
    else:
        display_image(pixels, resolution)


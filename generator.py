from PIL import Image

def int_to_brainfk(n):
    result = []
    while n > 0:
        if n > 10:
            result.append('>')
            result.append(int_to_brainfk(n // 10))
            result.append('[<++++++++++>-]<')
            n %= 10
        else:
            result.append('+' * n)
            n = 0
    return ''.join(result) + '.'

def process_image(image_path, output_path):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size
    
    # Check if the image resolution is above 720p
    if width > 1280 or height > 720:
        print("Error, image too large")
        return
    
    pixels = list(image.getdata())
    
    with open(output_path, 'w') as f:
        # Write pixel Brainfk numbers
        for i, pixel in enumerate(pixels):
            f.write(f"`~{int_to_brainfk(i)}~`\n")
        
        # Write RGB values in Brainfk numbers
        for i, pixel in enumerate(pixels):
            r, g, b = pixel[:3]
            f.write(f"`~{int_to_brainfk(i)}~` @ ~{int_to_brainfk(r)}~ # ~{int_to_brainfk(g)}~ $ ~{int_to_brainfk(b)}~\n")
            # Debug print
            print(f"Pixel {i}: R={r} G={g} B={b}")

        # Write image resolution in Brainfk numbers
        f.write(f"Resolution: {width}x{height}\n")
        f.write(f"`Width: ~{int_to_brainfk(width)}~`\n")
        f.write(f"`Height: ~{int_to_brainfk(height)}~`\n")

    print(f"Image processed: {width}x{height}")

if __name__ == "__main__":
    image_path = '/home/chloe/Pictures/Doom_720p.png'  # Image file path
    output_path = '/home/chloe/Documents/Image-Test/test.bfif'  # Output file path (.bfif)
    process_image(image_path, output_path)


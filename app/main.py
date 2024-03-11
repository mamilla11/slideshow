import glob
import os

import pygame
from pygame.locals import *
import serial
from dotenv import load_dotenv


load_dotenv()


IMAGE_FOLDER = 'app/Samples'
PORT = os.environ.get('PORT', '/dev/tty0')
BAUDRATE = int(os.environ.get('BAUDRATE', 9600))
SCALE_FACTOR = float(os.environ.get('SCALE_FACTOR', 0.5))
print(PORT)


# Initialize image viewer
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Image Viewer')
pygame.mouse.set_visible(False)


def list_images(folder):
    return glob.glob(os.path.join(folder, '*.jpg')) + glob.glob(os.path.join(folder, '*.png'))


def display_image(image_path):
    # Load the image
    original_image = pygame.image.load(image_path)

    # Calculate the scale factor to fit the image on the screen
    screen_width, screen_height = pygame.display.get_surface().get_size()
    image_width, image_height = original_image.get_size()

    # Scale the image
    scaled_image = pygame.transform.scale(original_image, (int(image_width * SCALE_FACTOR), int(image_height * SCALE_FACTOR)))

    # Calculate the position to center the image
    x = (screen_width - scaled_image.get_width()) // 2
    y = (screen_height - scaled_image.get_height()) // 2

    screen.blit(scaled_image, (x, y))
    pygame.display.flip()


def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False


def run():
    image_files = list_images(IMAGE_FOLDER)
    current_image_index = 0
    port = serial.Serial(PORT, baudrate=BAUDRATE, timeout=1)
    display_image(image_files[current_image_index])

    while not quit():
        command = port.readline().strip().decode('utf-8')
        print(command)  # TODO: for debug, remove later
        if not command == 'Next':
            continue
        current_image_index = (current_image_index + 1) % len(image_files)
        display_image(image_files[current_image_index])
        pygame.display.update()

    port.close()
    pygame.quit()


if __name__ == '__main__':
    run()

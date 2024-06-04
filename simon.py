import RPi.GPIO as GPIO
# gpiozero - reccomended library
from time import sleep
from random import randint
import pygame

DEBUG = False

# Pygame setup
pygame.init()
sounds = [
    pygame.mixer.Sound("one.wav"),
    pygame.mixer.Sound("two.wav"),
    pygame.mixer.Sound("three.wav"),
    pygame.mixer.Sound("four.wav"),
]

# GPIO setup
switches = [20, 16, 12, 26]
leds = [6, 13, 19, 21]
GPIO.setmode(GPIO.BCM)
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leds, GPIO.OUT)

# Some functions
def all_on():
    GPIO.output(leds, True)

def all_off():
    GPIO.output(leds, False)

def lose():
    for  in range(4):
        all_on()
        sleep(0.5)
        all_off()
        sleep(0.5)

# Game setup
sequence = [
    randint(0, 3),
    randint(0, 3),
]

WELCOME_MESSAGE = "Welcome to Simon!\n\
    Try to play the sequence back by pressing the switches.\n\
    Press ctrl + c to exit..."

print(WELCOME_MESSAGE)


# Game loop
try:
    while True:
        # generate the next item in the sequence
        new_color = randint(0, 3)
        sequence.append(new_color)

        # play out the sequence
        if DEBUG:
            print(f"sequence={sequence}")

        for color_value in sequence:
            GPIO.output(leds[color_value], True)
            sounds[color_value].play()
            sleep(1)
            GPIO.output(leds[color_value], False)
            sleep(0.5)

        # loooops
        switch_count = 0
        while switch_count < len(sequence):
            # waiting for an input
            # detect the button that is pressed
            pressed = False
            while not pressed:
                for i in range(len(switches)):
                    while GPIO.input(switches[i]) == True:
                        val = i # take note of which one was pressed
                        pressed = True

            # respond based on the press
            if DEBUG:
                print(val)

            GPIO.output(leds[val], True)
            sounds[val].play()
            sleep(1)
            GPIO.output(leds[val], False)
            sleep(0.25)

            # check for loss
            if val != sequence[switch_count]:
                lose()
                GPIO.cleanup()
                exit()

            # move on
            switch_count += 1

except KeyboardInterrupt:
    GPIO.cleanup()
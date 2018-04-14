#!/usr/bin/env python
import os.path
from dalek import debug
from termcolor import colored
from dalek import head_controller


def you_selected_challenge(current_challenge):
    if current_challenge == 1:
        debug.print_to_all_devices("You selected Obstacle Course", "OC")
    elif current_challenge == 2:
        debug.print_to_all_devices(
            "You selected Straight-Line Speed Test", "StL")
    elif current_challenge == 3:
        debug.print_to_all_devices("You selected Minimal Maze", "MM")
    elif current_challenge == 4:
        debug.print_to_all_devices(
            "You selected Somewhere Over The Rainbow", "OR")
    elif current_challenge == 5:
        debug.print_to_all_devices("You selected PiNoon", "PN")
    elif current_challenge == 6:
        debug.print_to_all_devices("You selected Duck Shoot", "DS")
    elif current_challenge == 7:
        debug.print_to_all_devices("You selected Slightly Deranged Golf", "DG")
    else:
        display_selected_challenge(current_challenge)


def display_selected_challenge(current_challenge):
    # Prints out the Challenge menu
    # It is preformated.

    os.system('clear')
    head_controller.leds_change_color(head_controller.leds_color['red'])
    head_controller.leds_flash(False)
    debug.print_to_all_devices(
        colored("\n\n\n\n           Challenge Select \n", 'red'))
    if current_challenge == 1:
        debug.print_to_all_devices(
            colored("        >>> Obstacle Course <<<", 'green'))
    else:
        debug.print_to_all_devices("           Obstacle Course")
    if current_challenge == 2:
        debug.print_to_all_devices(
            colored("        >>> Straight-Line Speed Test <<<", 'green'))
        head_controller.leds_change_color(head_controller.leds_color['green'])
        head_controller.leds_flash(True)
    else:
        debug.print_to_all_devices("           Straight-Line Speed Test")
    if current_challenge == 3:
        debug.print_to_all_devices(
            colored("        >>> Minimal Maze <<<", 'green'))
        head_controller.leds_change_color(head_controller.leds_color['blue'])
        head_controller.leds_flash(True)
    else:
        debug.print_to_all_devices("           Minimal Maze")
    if current_challenge == 4:
        debug.print_to_all_devices(
            colored("        >>> Somewhere Over The Rainbow <<<", 'green'))
        head_controller.leds_change_color(head_controller.leds_color['white'])
        head_controller.leds_flash(True)
    else:
        debug.print_to_all_devices("           Somewhere Over The Rainbow")
    if current_challenge == 5:
        debug.print_to_all_devices(colored("        >>> PiNoon <<<", 'green'))
    else:
        debug.print_to_all_devices("           PiNoon")
    if current_challenge == 6:
        debug.print_to_all_devices(
            colored("        >>> Duck Shoot <<<", 'green'))
    else:
        debug.print_to_all_devices("           Duck Shoot")
    if current_challenge == 7:
        debug.print_to_all_devices(
            colored("        >>> Slightly Deranged Golf <<<", 'green'))
    else:
        debug.print_to_all_devices("           Slightly Deranged Golf")

    debug.print_to_all_devices(
        colored("\n           Use UP and DOWN D-Pad Then Select", 'yellow'))
    if current_challenge == 1:  # output for onboard device
        debug.print_to_all_devices("", "OC")
    elif current_challenge == 2:
        debug.print_to_all_devices("", "StL")
    elif current_challenge == 3:
        debug.print_to_all_devices("", "MM")
    elif current_challenge == 4:
        debug.print_to_all_devices("", "OR")
    elif current_challenge == 5:
        debug.print_to_all_devices("", "PN")
    elif current_challenge == 6:
        debug.print_to_all_devices("", "DS")
    elif current_challenge == 7:
        debug.print_to_all_devices("", "DG")

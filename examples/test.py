#!/usr/bin/env python

# Copyright (c) 2020 Ryo Sakagami
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

"""
Main function
"""

import anki_vector
from vectify.util import init_spotify_client, show_current_track

def main():
    spotify = init_spotify_client()
    current_track = spotify.current_user_playing_track()

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        # Move Vector's Head and Lift for better visibility
        robot.behavior.set_head_angle(anki_vector.util.degrees(25.0))
        robot.behavior.set_lift_height(0.0)

        # Show current track info on Vector's face
        show_current_track(robot, current_track)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

# Copyright (c) 2020 Ryo Sakagami
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

"""
Check constantly if spotify is playing a track or not.
If yes, and if a new track starts, Vector tells us its information!
"""
import time
from threading import Timer, RLock, Thread, Event

import anki_vector
from vectify.util import init_spotify_client, show_current_track


class SpotifyTrackChecker(Thread):

    def __init__(self, robot, interval_s=5, max_show_trial=1):
        Thread.__init__(self)
        self.robot = robot
        self.interval_s = interval_s
        self.max_show_trial = max_show_trial

        self.spotify = init_spotify_client()
        self.stopped = Event()
        self.track = {}
        self.track_info = {}
        self.timer_cb_lock = RLock()

    def run(self):
        while not self.stopped.wait(self.interval_s):
            self.timer_cb()

    def parse_track_info(self, track):
        parsed_track = {}
        parsed_track['artwork_url'] = track['item']['album']['images'][1]['url']
        parsed_track['track_name'] = track['item']['name']
        parsed_track['artist_name_list'] = [artist['name'] for artist in track['item']['album']['artists']]
        return parsed_track

    def show(self):
        current_show_trial = 0
        while current_show_trial < self.max_show_trial:
            try:
                # Connect to Vector and overrides its behavior
                self.robot.conn.request_control()

                # Move Vector's Head and Lift for better visibility
                self.robot.behavior.set_head_angle(anki_vector.util.degrees(25.0))
                self.robot.behavior.set_lift_height(0.0)

                # Show current track info on Vector's face
                show_current_track(self.robot, self.track)

                # Release connection to Vector
                self.robot.conn.release_control()
                return
            except anki_vector.exceptions.VectorControlTimeoutException as e:
                print("Unable to show current track info: {}".format(e))
                current_show_trial += 1

    def timer_cb(self):
        print("SpotifyTrackChecker.timer_cb is called")
        # Ensure that this function is not called multiple times in parallel
        with self.timer_cb_lock:
            print("Acquired mutex")
            # Check the current track
            current_track = self.spotify.current_user_playing_track()
            current_track_info = self.parse_track_info(current_track)
            print("current track info: {}".format(current_track_info))

            # Check if the current track is new or not
            is_new_track = current_track_info != self.track_info

            # Update latest track info
            self.track = current_track
            self.track_info = current_track_info

            # If it is new, show its info on Vector's screen
            if is_new_track:
                print("New track detected!")
                self.show()


def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        print("Release control so Vector will do his normal behaviors")
        robot.conn.release_control()

        print("Ctrl+C to terminate the program")
        try:
            print("Initialize spotify track checker")
            spotify_track_checker = SpotifyTrackChecker(robot)
            spotify_track_checker.start()
            while True:
                time.sleep(1.)
        except KeyboardInterrupt:
            return

if __name__ == "__main__":
    main()

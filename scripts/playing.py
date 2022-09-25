import time
import pygame
import numpy
import cv2
from ffpyplayer.player import MediaPlayer


class VideoPlayer:
    def __init__(self, filepath):
        self.is_playing = False
        self.start_time = 0
        self.current_frame = 0

        self.vid_cap = cv2.VideoCapture(filepath)
        self.audio_player = MediaPlayer(filepath)

        self.fps = self.vid_cap.get(cv2.CAP_PROP_FPS)
        self.frame_width = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.frame_surf = pygame.Surface((self.frame_width, self.frame_height))

    def play(self):
        if not self.is_playing:
            self.is_playing = True
            self.start_time = time.time()

    def stop(self):
        if self.is_playing:
            self.is_playing = False
            self.audio_player.close_player()
            self.vid_cap.release()

    def get_frame(self):
        if not self.is_playing:
            return

        elapsed_frames = int((time.time() - self.start_time) * self.fps)
        if self.current_frame >= elapsed_frames:
            return

        for _ in range(elapsed_frames - self.current_frame):
            success, frame = self.vid_cap.read()
            # audio_frame, val = self.ff.get_frame()

        self.current_frame = elapsed_frames
        pygame.pixelcopy.array_to_surface(
            self.frame_surf, numpy.flip(numpy.rot90(frame[::-1]))
        )

    def draw_to(self, surface, pos):
        if self.is_playing:
            self.get_frame()
            surface.blit(self.frame_surf, pos)

    def get_size(self):
        return self.frame_width, self.frame_height

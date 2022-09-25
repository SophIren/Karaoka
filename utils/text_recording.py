import pygame
import time
import os

from scripts.playing import VideoPlayer


class LyricsRecorder:
    def __init__(self, input_lyrics_path, input_video_path):
        self.input_lyrics_path = input_lyrics_path
        self.input_file = None
        self.input_video_path = input_video_path
        self.output_lyrics_path = os.path.splitext(
            self.input_lyrics_path)[0] + '_out.lt'
        self.output_file = None

        self.surface = None

        self.done = False
        self.start_time = None

        pygame.init()
        self.player = VideoPlayer(self.input_video_path)

    def start(self):
        self.input_file = open(self.input_lyrics_path, encoding='utf-8')
        self.output_file = open(self.output_lyrics_path,
                                'w', encoding='utf-8')

        self.surface = pygame.display.set_mode(self.player.get_size())
        self.player.play()

        self.start_time = time.time()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.record_line()

            self.player.draw_to(self.surface, (0, 0))
            pygame.display.update()

    def record_line(self):
        line = self.input_file.readline()
        timestamp = time.time() - self.start_time
        while line == '\n':
            line = self.input_file.readline()
            if not line:
                self.stop()
                return

        self.output_file.write(f'{timestamp}~{line}')
        print(f'{timestamp}\n{line}\n\n')

    def stop(self):
        self.done = True
        self.input_file.close()
        self.output_file.close()


if __name__ == "__main__":
    recorder = LyricsRecorder('../songs/lyrics/Cheri Cheri Lady.txt',
                              '../songs/media/Cheri Cheri Lady.mp4')
    recorder.start()

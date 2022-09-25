import time
import pyaudio
from pydub import AudioSegment


class Recorder:
    DEFAULT_FRAMES = 512

    def __init__(self, song_path):
        self.song_path = song_path

        self.audio = pyaudio.PyAudio()

        self.out_rec = None
        self.in_stream = None
        self.out_device = None
        self.in_device = None

        self.channels_count = None
        self.frame_rate = None

        self.speaker_frames = []
        self.mic_frames = []

    def start_recording(self):
        self.speaker_frames = []
        self.mic_frames = []

        self.in_device = self.audio.get_default_input_device_info()
        self.channels_count = self.in_device['maxInputChannels']
        self.frame_rate = int(self.in_device['defaultSampleRate'])

        self.in_stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels_count,
            rate=self.frame_rate,
            input=True,
            frames_per_buffer=self.DEFAULT_FRAMES,
            input_device_index=self.in_device['index'],
            stream_callback=self.mic_callback)

    def mic_callback(self, in_data, frame_count, time_info, status):
        self.mic_frames.append(in_data)
        return None, pyaudio.paContinue

    def stop_recording(self):
        if self.in_stream is None:
            return
        self.in_stream.stop_stream()
        self.in_stream.close()

    @staticmethod
    def set_loudness(sound, target_dbfs=-20):
        loudness_difference = target_dbfs - sound.dBFS
        return sound.apply_gain(loudness_difference)

    @staticmethod
    def get_average_dbfs(dbfs1, dbfs2):
        if dbfs1 < -65:
            return dbfs2
        if dbfs2 < -65:
            return dbfs1
        return int((dbfs1 + dbfs2) / 2)

    def save_overlapped(self, file_name='output.wav'):
        mic_segment = AudioSegment(
            b''.join(self.mic_frames),
            sample_width=pyaudio.get_sample_size(pyaudio.paInt16),
            frame_rate=self.frame_rate,
            channels=self.channels_count)
        song_segment = AudioSegment.from_file(self.song_path)

        avg_dbfs = self.get_average_dbfs(mic_segment.dBFS, song_segment.dBFS)
        mic_segment = self.set_loudness(mic_segment, avg_dbfs)
        song_segment = self.set_loudness(song_segment, avg_dbfs)

        combined = mic_segment.overlay(song_segment)
        combined.export(file_name, format='wav')

# if __name__ == "__main__":
#     rec = Recorder()
#     rec.start_recording()
#     for _ in range(100):
#         time.sleep(1)
#         print(_)
#     rec.stop_recording()
#     rec.save_overlapped()

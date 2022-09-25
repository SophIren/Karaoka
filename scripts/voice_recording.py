import pyaudio
from pydub import AudioSegment
import os
import glob


class Recorder:
    OUTPUT_FOLDER_NAME = 'recordings'
    DEFAULT_FRAMES = 512

    def __init__(self, song_path):
        self.song_path = song_path
        if not os.path.exists(self.OUTPUT_FOLDER_NAME):
            os.makedirs(self.OUTPUT_FOLDER_NAME)

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
    def get_average_dbfs(dBFS1, dBFS2):
        if dBFS1 < -65:
            return dBFS2
        if dBFS2 < -65:
            return dBFS1
        return int((dBFS1 + dBFS2) / 2)

    @staticmethod
    def get_output_file_name_from_input(input_file_name):
        no_ext_name = os.path.splitext(
            os.path.basename(input_file_name)
        )[0]
        recordings_made = glob.glob(os.path.join(Recorder.OUTPUT_FOLDER_NAME,
                                                 f'{no_ext_name}_?.wav'))
        return f'{no_ext_name}_{len(recordings_made)}.wav'

    def save_overlapped(self, file_name=None):
        if file_name is None:
            file_name = self.get_output_file_name_from_input(self.song_path)

        mic_segment = AudioSegment(
            b''.join(self.mic_frames),
            sample_width=pyaudio.get_sample_size(pyaudio.paInt16),
            frame_rate=self.frame_rate,
            channels=self.channels_count)
        song_segment = AudioSegment.from_file(self.song_path)

        print(mic_segment.dBFS, song_segment.dBFS)
        avg_dbfs = self.get_average_dbfs(mic_segment.dBFS, song_segment.dBFS)
        if mic_segment.dBFS > -60:
            mic_segment = self.set_loudness(mic_segment, avg_dbfs)
        if song_segment.dBFS > -60:
            song_segment = self.set_loudness(song_segment, avg_dbfs)

        combined = mic_segment.overlay(song_segment)
        combined.export(os.path.join(self.OUTPUT_FOLDER_NAME, file_name),
                        format='wav')

# if __name__ == "__main__":
#     rec = Recorder()
#     rec.start_recording()
#     for _ in range(100):
#         time.sleep(1)
#         print(_)
#     rec.stop_recording()
#     rec.save_overlapped()

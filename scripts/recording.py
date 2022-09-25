import time
import pyaudio
from pydub import AudioSegment


class Recorder:
    DEFAULT_FRAMES = 512
    FRAME_RATE = 48000
    SAMPLE_WIDTH = 2
    CHANNEL_COUNT = 2

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.out_rec = None
        self.in_rec = None
        self.out_device = None
        self.in_device = None
        self.speaker_frames = []
        self.mic_frames = []

    def start_recording(self):
        self.speaker_frames = []
        self.mic_frames = []

        self.in_device = self.audio.get_default_input_device_info()
        self.in_rec = self.create_stream(self.in_device['index'], False,
                                         self.mic_callback)

        self.out_device = self.get_default_wasapi_device()
        self.out_rec = self.create_stream(self.out_device['index'], True,
                                          self.speaker_callback)

    def stop_recording(self):
        if self.out_rec is not None:
            self.out_rec.stop_stream()
            self.out_rec.close()
        if self.in_rec is not None:
            self.in_rec.stop_stream()
            self.in_rec.close()

    def save_recorded_frames(self, file_name='output.wav'):
        mic_segment = AudioSegment(b''.join(self.mic_frames),
                                   sample_width=self.SAMPLE_WIDTH,
                                   frame_rate=self.FRAME_RATE,
                                   channels=self.CHANNEL_COUNT)
        speaker_segment = AudioSegment(b''.join(self.speaker_frames),
                                       sample_width=self.SAMPLE_WIDTH,
                                       frame_rate=self.FRAME_RATE,
                                       channels=self.CHANNEL_COUNT)

        combined = mic_segment.overlay(speaker_segment)
        combined.export(file_name, format='wav')

    def speaker_callback(self, in_data, frame_count, time_info, status):
        self.speaker_frames.append(in_data)
        return None, pyaudio.paContinue

    def mic_callback(self, in_data, frame_count, time_info, status):
        self.mic_frames.append(in_data)
        return None, pyaudio.paContinue

    def create_stream(self, device_index, as_loopback, callback):
        return self.audio.open(
            format=pyaudio.paInt16,
            channels=self.CHANNEL_COUNT,
            rate=self.FRAME_RATE,
            input=True,
            frames_per_buffer=self.DEFAULT_FRAMES,
            input_device_index=device_index,
            stream_callback=callback,
            as_loopback=as_loopback)

    def get_default_wasapi_device(self):
        def_out = self.audio.get_default_output_device_info()

        for i in range(self.audio.get_device_count()):
            device = self.audio.get_device_info_by_index(i)
            host = self.audio \
                .get_host_api_info_by_index(device['hostApi'])['name']
            if device['name'] == def_out['name'] and host == 'Windows WASAPI':
                return device

        return None


if __name__ == "__main__":
    rec = Recorder()
    rec.start_recording()
    for _ in range(100):
        time.sleep(1)
        print(_)
    rec.stop_recording()
    rec.save_recorded_frames()

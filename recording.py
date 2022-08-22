import time
import pyaudio
import wave
import audioop
import samplerate as sr


class Recorder:
    DEFAULT_FRAMES = 512

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.resampler = sr.Resampler()
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
        self.in_rec = self.create_stream(self.in_device, False)

        self.out_device = self.get_default_wasapi_device()
        self.out_rec = self.create_stream(self.out_device, True)

    def stop_recording(self):
        if self.out_rec is not None:
            self.out_rec.stop_stream()
            self.out_rec.close()
        if self.in_rec is not None:
            self.in_rec.stop_stream()
            self.in_rec.close()

    def save_recorded_frames(self, file_name='output.wav'):
        channel_count = max(self.in_device['maxInputChannels'],
                            self.out_device['maxOutputChannels'])
        sample_rate = max(self.out_device["defaultSampleRate"],
                          self.in_device["defaultSampleRate"])
        waveFile = wave.open(file_name, 'wb')
        waveFile.setnchannels(channel_count)
        waveFile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(sample_rate)

        self.mic_frames = b''.join(self.mic_frames)
        self.speaker_frames = b''.join(self.speaker_frames)
        l = min(len(self.mic_frames), len(self.speaker_frames))
        waveFile.writeframes(audioop.add(self.mic_frames[:l],
                                         self.speaker_frames[:l], 2))
        waveFile.close()

    def speaker_callback(self, in_data):
        self.speaker_frames.append(in_data)
        return None, pyaudio.paContinue

    def mic_callback(self, in_data):
        self.mic_frames.append(in_data)
        return None, pyaudio.paContinue

    def create_stream(self, device, as_loopback):
        if as_loopback:
            callback = lambda in_data, frame_count, time_info, status: \
                self.speaker_callback(in_data)
        else:
            callback = lambda in_data, frame_count, time_info, status: \
                self.mic_callback(in_data)

        return self.audio.open(
            format=pyaudio.paInt16,
            channels=device['maxOutputChannels'] if as_loopback
            else device['maxInputChannels'],
            rate=48000,
            input=True,
            frames_per_buffer=self.DEFAULT_FRAMES,
            input_device_index=device["index"],
            stream_callback=callback,
            as_loopback=as_loopback)

    def get_default_wasapi_device(self):
        def_out = self.audio.get_default_output_device_info()

        for i in range(self.audio.get_device_count()):
            device = self.audio.get_device_info_by_index(i)
            host = self.audio.get_host_api_info_by_index(
                device['hostApi'])['name']
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

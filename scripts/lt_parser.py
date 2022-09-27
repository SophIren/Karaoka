import datetime


class LTParser:
    SPLITTER = '~'
    ENCODING = 'utf-8'

    def __init__(self, file_path):
        self.file_path = file_path
        self.lyrics = []
        self.current_time = 0
        self.pointer = 0

    def parse(self):
        for line in open(self.file_path, encoding=LTParser.ENCODING):
            verse, timestamp = line.split(LTParser.SPLITTER)
            self.lyrics.append({
                'text': verse,
                'time': datetime.timedelta(seconds=float(timestamp))
            })

    def actualize_time(self, time):
        if time < self.current_time:
            return
        self.current_time = time

        for i in range(self.pointer, len(self.lyrics)):
            if self.lyrics[i]['time'] > self.current_time:
                self.pointer = i
                break

    def get_next_n_lines(self, n):
        for i in range(self.pointer, self.pointer + n):
            yield self.lyrics[self.pointer]['text']

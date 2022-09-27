class LTParser:
    SPLITTER = '~'
    ENCODING = 'utf-8'

    def __init__(self, file_name):
        self.lyrics = self._parse(file_name)
        self.current_time = 0
        self.pointer = 0

    @staticmethod
    def _parse(file_name):
        lyrics = []
        for line in open(file_name, encoding=LTParser.ENCODING):
            timestamp, verse = line.split(LTParser.SPLITTER)
            lyrics.append({
                'text': verse,
                'time': float(timestamp)
            })
        return lyrics

    def actualize_time(self, time):
        if time < self.current_time:
            return
        self.current_time = time

        for i in range(max(0, self.pointer), len(self.lyrics)):
            if self.lyrics[i]['time'] > self.current_time:
                self.pointer = i - 1
                break

    def get_next_n_lines(self, n):
        for i in range(self.pointer, min(self.pointer + n, len(self.lyrics))):
            if i == -1:
                yield ' '
            else:
                yield self.lyrics[i]['text'].rstrip().replace('′', '\'')

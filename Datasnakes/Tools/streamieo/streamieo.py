from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue, Empty
from Datasnakes.Tools.logit import LogIt
# Implemented from http://www.sharats.me/posts/the-ever-useful-and-neat-subprocess-module/
# In the "Watching both stdout and stderr" section


class StreamIEO(object):

    def __init__(self):
        """
        A class that individually threads the capture of the stdout stream and the stderr stream of a system command.
        The stdout/stderr are queued in the order they occur.  As the que populates another thread, parse the que and
        prints to the screen using the LogIT class.
        """
        self.io_q = Queue()
        self.streamieolog = LogIt().default(logname="streamieo", logfile=None)

    def streamer(self, cmd):
        process = Popen([cmd], stdout=PIPE, stderr=PIPE)
        # Watch the standard output and add it to the que
        Thread(target=self._stream_watcher, name='stdout-watcher', args=('STDOUT', process.stdout)).start()
        # Watch the standard input and add it to the que
        Thread(target=self._stream_watcher, name='stderr-watcher', args=('STDERR', process.stderr)).start()
        # As items are added, print the stream.
        Thread(target=self._printer, name='_printer', args=process).start()

    def _stream_watcher(self, identifier, stream):
        # Watch the stream and add to the que dynamically
        # This runs in tandem with the printer.  So as the stdout/stderr streams are queued here,
        # the que is parsed and printed in the printer function.
        for line in stream:
            self.io_q.put((identifier, line))
        if not stream.closed:
            stream.close()

    def _printer(self, process):
        # Prints the que as it is populated with stdout/stderr dynamically.
        while True:
            try:
                # Block for 1 second.
                item = self.io_q.get(True, 1)
            except Empty:
                # No output in either streams for a second. Are we done?
                if process.poll() is not None:
                    break
            else:
                identifier, line = item
                if identifier == "STDERR":
                    self.streamieolog.error(line)
                elif identifier == "STDOUT":
                    self.streamieolog.info(line)
                else:
                    self.streamieolog.critical(identifier + ':' + line)

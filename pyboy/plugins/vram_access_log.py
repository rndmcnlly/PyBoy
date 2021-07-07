import array

from pyboy.plugins.base_plugin import PyBoyPlugin

class ReadSnoop(object):
    def __init__(self, target, callback):
        self.target = target
        self.callback = callback
    
    def __getitem__(self, key):
        self.callback(key)
        return self.target[key]

    def __setitem__(self, key, value):
        self.target[key] = value


class VramAccessLog(PyBoyPlugin):
    argv = [("--vram_access_log", {"help": "Path to new VRAM access log file (int32 array, -1 each frame)"})]

    def __init__(self, *args):
        if not self.enabled():
            return
        
        self.log_file = open(self.pyboy_argv.get("vram_access_log"), "wb")
        self.log_array = array.array('i')
        self.log_array.append(-1)

        self.mb.lcd.VRAM = ReadSnoop(
            self.mb.lcd.VRAM,
            lambda key: self.log_array.append(key))

    def post_tick(self):
        self.log_array.tofile(self.log_file)
        del self.log_array[:]
        self.log_array.append(-1)
    
    def stop(self):
        self.log_file.close()

    def enabled(self):
        return self.pyboy_argv.get("vram_access_log")
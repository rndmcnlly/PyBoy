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


class CartRamAccessLog(PyBoyPlugin):
    argv = [("--cart_ram_access_log", {"help": "Path to new cartridge RAM access log file (int32 array, -1 each frame)"})]

    def __init__(self, *args):
        if not self.enabled():
            return

        self.log_file = open(self.pyboy_argv.get("cart_ram_access_log"), "wb")
        self.log_array = array.array('i')
        self.log_array.append(-1)

        def make_logging_callback(base):
            log = self.log_array
            return lambda offset: log.append(base + offset)

        self.mb.cartridge.rambanks = [
            ReadSnoop(bank, make_logging_callback(0x2000*i))
            for i,bank in enumerate(self.mb.cartridge.rambanks)]

    def post_tick(self):
        self.log_array.tofile(self.log_file)
        del self.log_array[:]
        self.log_array.append(-1)
    
    def stop(self):
        self.log_file.close()

    def enabled(self):
        return self.pyboy_argv.get("cart_ram_access_log")
import logging
from os.path import expanduser, join, isdir
from os import mkdir


class Configuration:
    def __init__(self):
        self._home = expanduser("~")

        self.config_dir = join(self._home, ".timescribe")
        if not isdir(self.config_dir):
            mkdir(self.config_dir)

        # TODO: config should probably come from a file
        self.connection_string = "sqlite:///%s" % join(self.config_dir, "activity_log.db")
        self.log_level = logging.DEBUG


config = Configuration()
logging.basicConfig(format="%(asctime)s %(message)s", level=config.log_level)

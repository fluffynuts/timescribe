from time import sleep
from sqlalchemy.orm import sessionmaker
from get_current_activity import get_current_activity, ActivityInfo
from config import config
from models.activity import Activity
from models.base import Base
from sqlalchemy import create_engine
import logging as log


def _initialise_database():
    engine = create_engine(config.connection_string)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    return sessionmaker(bind=engine)


class Collector:
    def __init__(self):
        self._create_db_session = _initialise_database()
        self.running = False
        self._stop = False
        self._last_activity: ActivityInfo = None

    def start(self):
        self.running = True
        self._stop = False
        self._last_activity = None
        while not self._stop:
            current_activity = get_current_activity()
            if self._activity_changed(current_activity):
                activity = Activity(current_activity.name, current_activity.title, current_activity.args)
                log.debug("gathering activity: %s" % activity.name)
                session = self._create_db_session()
                session.add(activity)
                session.commit()
            sleep(1)

    def stop(self):
        self._stop = True

    def _activity_changed(self, current_activity: ActivityInfo):
        if self._last_activity is None:
            self._last_activity = current_activity
            return True
        # window title may change on same process, but it might be interesting
        #  to record that as a "new activity" anyway
        result = self._last_activity.name != current_activity.name or \
                 self._last_activity.title != current_activity.title or \
                 self._last_activity.args != current_activity.args
        if result:
            log.debug("activity change: name:  %s => %s" % (self._last_activity.name, current_activity.name))
            log.debug("activity change: title: %s => %s" % (self._last_activity.title, current_activity.title))
            log.debug("activity change: args:  %s => %s" % (self._last_activity.args, current_activity.args))
        self._last_activity = current_activity
        return result


if __name__ == "__main__":

    def signal_handler(sig, frame):
        print("Exiting on signal...")
        collector.stop()
        while collector.running:
            sleep(50)


    collector = Collector()
    collector.start()

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

class ActivityInfo:
    def __init__(self, name: str, args: str, title: str):
        self.name = name
        self.title = title
        self.args = args


def get_current_activity() -> ActivityInfo:
    """
    Get the currently active window.

    Returns
    -------
    string :
        Name of the currently active window.
    """
    import sys
    title = None
    process_name = None
    process_args = None
    if sys.platform in ['linux', 'linux2']:
        # Alternatives: http://unix.stackexchange.com/q/38867/4784
        # TODO: get the process name
        try:
            import wnck
        except ImportError:
            logging.info("wnck not installed")
            wnck = None
        if wnck is not None:
            screen = wnck.screen_get_default()
            screen.force_update()
            window = screen.get_active_window()
            if window is not None:
                pid = window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    title = f.read()
        else:
            try:
                from gi.repository import Gtk, Wnck
                gi = "Installed"
            except ImportError:
                logging.info("gi.repository not installed")
                gi = None
            if gi is not None:
                Gtk.init([])  # necessary if not using a Gtk.main() loop
                screen = Wnck.Screen.get_default()
                screen.force_update()  # recommended per Wnck documentation
                active_window = screen.get_active_window()
                pid = active_window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    title = f.read()
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        # http://stackoverflow.com/a/608814/562769
        import win32gui
        import win32process
        from wmi import WMI

        wmi = WMI()
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in wmi.query("SELECT Name, Commandline from Win32_Process where ProcessId = %s" % str(pid)):
            process_name = p.Name
            process_args = " ".join(p.Commandline.split(" ")[1:])
            break
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        # TODO: get process name
        # http://stackoverflow.com/a/373310/562769
        from AppKit import NSWorkspace
        title = (NSWorkspace.sharedWorkspace()
                              .activeApplication()['NSApplicationName'])
    return ActivityInfo(process_name, title, process_args)

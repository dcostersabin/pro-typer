import pyautogui
from plyer import notification
from pynput.keyboard import Listener as KeyBoardListener
from pynput.keyboard import Controller as KeyController
from pynput.mouse import Controller
from abc import abstractmethod, ABC


class Trigger(ABC):

    def __init__(self):
        self._notify_start()
        self.key_board_listener = KeyBoardListener(on_press=self.on_keydown)
        self.keyboard_controller = KeyController()
        super().__init__()
        with self.key_board_listener as key:
            key.join()

    @staticmethod
    def _notify_start():
        notification.notify(
            title="Started Tracking",
            message="Mouse And Keyboard",
            app_icon=None,
            timeout=2,

        )

    @staticmethod
    def _notify_end():
        notification.notify(
            title="Stopped Tracking",
            message="Mouse And Keyboard",
            app_icon=None,
            timeout=2,

        )

    @abstractmethod
    def on_keydown(self, key):
        # do stuff
        pass


class ImageSize:

    def __init__(self):
        self.start = None
        self.end = None

    def is_valid(self):
        if self.start is None or self.end is None:
            self.invalid_notify()
            return False

        height, width = self.height_width
        x_valid = self.start[0] < self.end[0]
        y_valid = self.start[1] > self.end[1]
        h_w_valid = height > 28 and width > 28

        status = x_valid and y_valid and h_w_valid

        if not status:
            self.invalid_notify()

        return status

    @property
    def valid_region(self):
        h, w = self.height_width
        return self.start[0], self.end[1], w, h

    @property
    def height_width(self):
        height = self.start[1] - self.end[1]
        width = self.end[0] - self.start[0]
        return height, width

    @property
    def start_coordinate(self):
        return f"x:{self.start[0]} y:{self.start[1]}"

    @property
    def end_coordinate(self):
        return f"x:{self.end[0]} y:{self.end[1]}"

    @staticmethod
    def invalid_notify():
        notification.notify(
            title='Invalid Coordinates',
            message="Try Again",
            app_icon=None,
            timeout=2

        )


class Screenshot:

    def __init__(self, callbacks=None):
        self.image = None
        self.callbacks = callbacks
        self.image_size = ImageSize()
        self.mouse_controller = Controller()
        super().__init__()

    def _call_callbacks(self):
        _ = None if self.callbacks is None else [calls(self.image) for calls in self.callbacks]

    def take_screenshot(self):
        region = self.image_size.valid_region if self.image_size.is_valid() else None

        if region is not None:
            self.image = pyautogui.screenshot(region=region)
        self._call_callbacks()

    def take_x(self):
        self.image_size.start = self.mouse_controller.position
        notification.notify(title="Captured Starting Coordinates",
                            message=self.image_size.start_coordinate, app_icon=None,
                            timeout=2)

    def take_y(self):
        self.image_size.end = self.mouse_controller.position
        notification.notify(title="Captured Ending Coordinates",
                            message=self.image_size.end_coordinate, app_icon=None,
                            timeout=2)

from OCR import ImageToChar
from pynput.keyboard import Key
from image_utils import Trigger, Screenshot
import numpy as np
from plyer import notification


class SysController(Trigger, ImageToChar):

    def __init__(self, save=False):
        self.text = None
        self.save = save
        self.sc = Screenshot(callbacks=[self.predict_callback])
        super().__init__()

    @staticmethod
    def notify_ready():
        notification.notify(
            title='Ready',
            message="Press Insert To Type",
            app_icon=None,
            timeout=3
        )

    def predict_callback(self, image):
        if image is None:
            return
        if self.save:
            image.save('captured.png')
        self.image = np.array(image)
        self.predict()
        self.notify_ready()

    def paste_prediction(self):
        if self.prediction is None:
            return
        words = self.prediction.replace('\x0c', '').replace("'", "").replace('\n', " ")
        words = words.split(' ')

        for word in words:
            for letter in word:
                self.keyboard_controller.press(str(letter))
                self.keyboard_controller.release(str(letter))

            self.keyboard_controller.press(Key.space)
            self.keyboard_controller.release(Key.space)

    def on_keydown(self, key):
        key = key if hasattr(key, 'name') else key.char

        match key:

            case Key.ctrl:
                self.sc.take_screenshot()

            case Key.esc:
                self.key_board_listener.stop()
                self._notify_end()
                exit(code=1)

            case Key.shift:
                self.sc.take_x()

            case Key.alt:
                self.sc.take_y()

            case Key.down:
                self.paste_prediction()

            case _:
                pass

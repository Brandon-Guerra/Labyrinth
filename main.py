from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

class Player(Widget):
    exist = True

class MazeGame(Widget):
    player1 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MazeGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.player1.y += 10
        elif keycode[1] == 's':
            self.player1.y -= 10
        elif keycode[1] == 'a':
            self.player1.x -= 10
        elif keycode[1] == 'd':
            self.player1.x += 10
        return True


class MazeApp(App):
    def build(self):
        game = MazeGame()
        return game


if __name__ == '__main__':
    MazeApp().run()
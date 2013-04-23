import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.graphics import Callback
from kivy.properties import NumericProperty, ObjectProperty
from kivy.graphics.opengl import glBlendFunc, GL_SRC_ALPHA, GL_ONE, GL_ZERO, GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR, GL_ONE_MINUS_SRC_ALPHA, GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA, GL_DST_COLOR, GL_ONE_MINUS_DST_COLOR

BLEND_FUNC = {0: GL_ZERO,
            1: GL_ONE,
            0x300: GL_SRC_COLOR,
            0x301: GL_ONE_MINUS_SRC_COLOR,
            0x302: GL_SRC_ALPHA,
            0x303: GL_ONE_MINUS_SRC_ALPHA,
            0x304: GL_DST_ALPHA,
            0x305: GL_ONE_MINUS_DST_ALPHA,
            0x306: GL_DST_COLOR,
            0x307: GL_ONE_MINUS_DST_COLOR
}

class RootWidget(Widget):
    pass

class ScrollableGridLayout(Widget):
    pass

class BlendFuncChoices(Popup):

    def __init__(self, func_chooser, **kwargs):
        super(BlendFuncChoices, self).__init__(**kwargs)
        self.func_chooser = func_chooser
        self.populate_list()
        

    def populate_list(self):
        self.src_choices_box.clear_widgets()
        self.dest_choices_box.clear_widgets()
        label = Label(text = 'Source')
        self.src_choices_box.add_widget(label)
        label = Label(text = 'Dest')
        self.dest_choices_box.add_widget(label)
        for each in BLEND_FUNC:
            
            button = ToggleButton(text = str(self.func_chooser.translate_blend_func_value(each)), font_size = self.size[0]*.12, id = str(each), group = 'func_choices')
            self.src_choices_box.add_widget(button)
            button.bind(on_press=self.press_src_button)
            if self.func_chooser.current_src == each:
                button.state = 'down'
            button = ToggleButton(text = str(self.func_chooser.translate_blend_func_value(each)), font_size = self.size[0]*.12, id = str(each), group = 'func_choices2')
            button.bind(on_press=self.press_dest_button)
            self.dest_choices_box.add_widget(button)
            if self.func_chooser.current_dest == each:
                button.state = 'down'
        

    def press_src_button(self, instance):
        self.func_chooser.set_source_text(instance.text, instance.id, instance.state)

    def press_dest_button(self, instance):
        self.func_chooser.set_dest_text(instance.text, instance.id, instance.state)
            
    

class BlendFuncChooser(BoxLayout):
    func_choices = ObjectProperty(None)
    current_src = NumericProperty(None)
    current_dest = NumericProperty(None)
    canvas_to_blend = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BlendFuncChooser, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_chooser)

    def setup_chooser(self, dt):
        self.func_choices = BlendFuncChoices(self)

    def open_popup(self):
        self.func_choices.open()

    def on_current_src(self, instance, value):
        source_text = str(self.translate_blend_func_value(self.current_src))
        dest_text = str(self.translate_blend_func_value(self.current_dest))
        self.blend_button.text = source_text + ' -> ' + dest_text
        self.canvas_to_blend.blend_factor_source = self.current_src


    def on_current_dest(self, instance, value):
        source_text = str(self.translate_blend_func_value(self.current_src))
        dest_text = str(self.translate_blend_func_value(self.current_dest))
        self.blend_button.text = source_text + ' -> ' + dest_text
        self.canvas_to_blend.blend_factor_dest = self.current_dest

    def set_source_text(self, text, button_id, state):
        if state == 'down':
            self.current_src = int(button_id)
            

    def set_dest_text(self, text, button_id, state):
        print 'setting dest', state
        if state == 'down':
            self.current_dest = int(button_id)

    def translate_blend_func_value(self, func_value):
        blend_func_names = {0: 'GL_ZERO',
            1: 'GL_ONE',
            0x300: 'GL_SRC_COLOR',
            0x301: 'GL_ONE_MINUS_SRC_COLOR',
            0x302: 'GL_SRC_ALPHA',
            0x303: 'GL_ONE_MINUS_SRC_ALPHA',
            0x304: 'GL_DST_ALPHA',
            0x305: 'GL_ONE_MINUS_DST_ALPHA',
            0x306: 'GL_DST_COLOR',
            0x307: 'GL_ONE_MINUS_DST_COLOR'
        }

        if func_value in blend_func_names:
            return blend_func_names[func_value]
        else:
            return func_value

class TextureMaskWidget(Widget):
    blend_factor_source = NumericProperty(GL_ZERO)
    blend_factor_dest = NumericProperty(GL_SRC_ALPHA)
    reset_blend_factor_source = NumericProperty(GL_SRC_ALPHA)
    reset_blend_factor_dest = NumericProperty(GL_ONE_MINUS_SRC_ALPHA)
    def __init__(self, **kwargs):
        super(TextureMaskWidget, self).__init__(**kwargs)

        with self.canvas.before:
            Callback(self._set_blend_func)
        with self.canvas.after:
            Callback(self._reset_blend_func)
    
    def _set_blend_func(self, instruction):
        glBlendFunc(self.blend_factor_source, self.blend_factor_dest)

    def _reset_blend_func(self, instruction):
        glBlendFunc(self.reset_blend_factor_source, self.reset_blend_factor_dest)

class CustomGridLayout(GridLayout):

    def __init__(self, **kwargs):
        super(CustomGridLayout, self).__init__(**kwargs)
        Clock.schedule_once(self.create_buttons)

    def create_buttons(self, dt):
        for i in range(19):
            btn = Button(text=str('Oak Groove'), size_hint= (1., None), height = 30)
            self.update_size(30)
            self.add_widget(btn)

    def update_size(self, button_height):
        self.size = self.size[0], self.size[1] + button_height + self.spacing

class ScrollViewApp(App):
    def build(self):
        pass


if __name__ == '__main__':

    ScrollViewApp().run()
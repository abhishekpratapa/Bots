from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')
Config.set('graphics','resizable',0)

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # spacer
        self.add_widget(Label(text=' '))
        self.add_widget(Label(text=' '))

        # spacer
        self.add_widget(Label(text='Bot Login', font_size='20sp'))
        self.add_widget(Label(text=' '))

        #spacer
        self.add_widget(Label(text=' '))
        self.add_widget(Label(text=' '))

        #username
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        #password
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        # spacer
        self.add_widget(Label(text=' '))
        self.add_widget(Label(text=' '))

        #button login
        self.add_widget(Label(text=' '))
        self.hello = Button(text='Submit')
        self.hello.bind(on_press=self.auth)
        self.add_widget(self.hello)

        # spacer
        self.add_widget(Label(text=' '))
        self.add_widget(Label(text=' '))

    def auth(self,instance):

        '''
        self.username.text
        self.password.text
        '''

class TestApp(App):
    def build(self):
        return LoginScreen()

TestApp().run()
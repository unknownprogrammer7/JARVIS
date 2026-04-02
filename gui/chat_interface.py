from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class ChatBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Chat history label
        self.chat_history = Label(size_hint_y=None)
        self.chat_history.bind(size=lambda *x: self.chat_history.setter('text_size')(self.chat_history, (self.chat_history.width, None)))
        self.chat_history.text_size = (self.width, None)
        self.add_widget(self.chat_history)

        # Text input for new messages
        self.message_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.message_input)

        # Send button
        self.send_button = Button(text='Send', size_hint_y=None, height=30)
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            self.chat_history.text += f\"\nUser: {message}\"
            self.message_input.text = ''

class ChatApp(App):
    def build(self):
        return ChatBox()

if __name__ == '__main__':
    ChatApp().run()
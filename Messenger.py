from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy_socket_messenger.connect import Client
import threading

client = Client(8080, host="127.0.0.1")

class InterfaceServ(BoxLayout):
    def send(self, text):
        client.message = text
        print(text)
        self.ids._messege_text.text = ""


class ServMsgApp(App):
    def build(self):
        self.layout = InterfaceServ()
        Clock.schedule_interval(self.update_message, 1.0 / 60.0)
        return self.layout

    def update_message(self, dt):
        self.layout.ids._messenger.text = client.message_read



def view():
    ServMsgApp().run()

def controll():
    client.run()


vThread = threading.Thread(target=view)
vThread.daemon = True

cThread = threading.Thread(target=controll)
cThread.daemon = True
cThread.start()
vThread.start()

cThread.join()
vThread.join()


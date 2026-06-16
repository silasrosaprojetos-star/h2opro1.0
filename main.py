import threading
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty
from kivy.metrics import dp

try:
    from jnius import autoclass
    import android
    ON_ANDROID = True
except ImportError:
    ON_ANDROID = False

KV = '''
Screen:
    canvas.before:
        Color:
            rgba: 0.08, 0.08, 0.08, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: "52dp"
            padding: "12dp", "8dp"
            Label:
                text: "H2O PRO"
                color: 0, 0.8, 1, 1
                bold: True
            Button:
                text: "INFO"
                on_release: app.mostrar_info()
        BoxLayout:
            padding: "10dp"
            spacing: "10dp"
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.4
                canvas.before:
                    Color:
                        rgba: 0.13, 0.13, 0.13, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [14]
                Widget:
                    canvas:
                        Color:
                            rgba: 0, 0.5, 0.9, 0.85
                        Rectangle:
                            pos: self.x, self.y
                            size: self.width, app.nivel_grafico
            BoxLayout:
                orientation: 'vertical'
                Button:
                    text: "LIGAR"
                    on_release: app.enviar_comando('L')
                Button:
                    text: "DESLIGAR"
                    on_release: app.enviar_comando('D')
                Button:
                    text: app.texto_conexao
                    on_release: app.alternar_conexao()
'''

class SupervisorioTechApp(MDApp):
    status_bomba = StringProperty("DESCONECTADO")
    cor_bomba = ColorProperty([0.5, 0.5, 0.5, 1])
    nivel_grafico = NumericProperty(0)
    texto_conexao = StringProperty("CONECTAR")
    conectado = BooleanProperty(False)

    def build(self):
        self.socket_bluetooth = None
        self.output_stream = None
        return Builder.load_string(KV)

    def on_start(self):
        if ON_ANDROID:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.BLUETOOTH, Permission.BLUETOOTH_ADMIN, 
                                 Permission.BLUETOOTH_CONNECT, Permission.BLUETOOTH_SCAN,
                                 Permission.ACCESS_FINE_LOCATION])

    def alternar_conexao(self):
        if not self.conectado:
            self.conectar_bluetooth()
        else:
            self.desconectar_bluetooth()

    def conectar_bluetooth(self):
        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()
            device = adapter.getRemoteDevice("E1:EF:6B:52:BF:16")
            UUID = autoclass('java.util.UUID')
            spp_uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
            self.socket_bluetooth = device.createRfcommSocketToServiceRecord(spp_uuid)
            self.socket_bluetooth.connect()
            self.output_stream = self.socket_bluetooth.getOutputStream()
            self.conectado = True
            self.texto_conexao = "DESCONECTAR"
            self.status_bomba = "CONECTADO"
        except Exception:
            self.status_bomba = "ERRO"

    def enviar_comando(self, comando):
        if self.output_stream:
            self.output_stream.write(comando.encode('utf-8'))

    def mostrar_info(self):
        self.status_bomba = "H2O Pro v1.1"

if __name__ == '__main__':
    SupervisorioTechApp().run()
'''

# ============================================================
#  H2O Pro v1.1 - Supervisório Bluetooth
#  Farad Automação / S.ROSA ENGENHARIA.
#  Compatível com firmware H2O Pro v1.0 (Arduino UNO + HC-06)
#  Protocolo RX: "BOMBA;BOIA_BAIXA;BOIA_ALTA\n"
#  Protocolo TX: 'L' = Ligar | 'D' = Desligar | 'R' = Reset
# ============================================================


    # ============================================================
#  H2O Pro v1.1 - Supervisório Bluetooth
#  Farad Automação / S.ROSA ENGENHARIA.
# ============================================================

import threading
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty
from kivy.metrics import dp

try:
    from jnius import autoclass
    import android  # noqa
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
        
        # ── Topbar ──
        BoxLayout:
            size_hint_y: None
            height: "52dp"
            padding: "12dp", "8dp"
            canvas.before:
                Color:
                    rgba: 0.05, 0.05, 0.05, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "H2O PRO"
                color: 0, 0.8, 1, 1
                bold: True
            Button:
                text: "INFO"
                on_release: app.mostrar_info()

        # ── Corpo Principal ──
        BoxLayout:
            padding: "10dp"
            spacing: "10dp"
            
            # Reservatório
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
                Label:
                    text: "NIVEL"
                Widget:
                    canvas:
                        Color:
                            rgba: 0, 0.5, 0.9, 0.85
                        Rectangle:
                            pos: self.x, self.y
                            size: self.width, app.nivel_grafico

            # Controles
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
    # Propriedades para o Kivy acessar
    nome_estado = StringProperty("STATUS")
    cor_estado = ColorProperty([1, 1, 1, 1])
    status_bomba = StringProperty("DESCONECTADO")
    cor_bomba = ColorProperty([0.5, 0.5, 0.5, 1])
    nivel_grafico = NumericProperty(0)
    pct_nivel = StringProperty("0%")
    texto_conexao = StringProperty("CONECTAR")
    cor_conexao = ColorProperty([0.2, 0.2, 0.2, 1])
    conectado = BooleanProperty(False)
    cor_agua = ColorProperty([0, 0.5, 0.9, 0.85])
    cor_led_verde = ColorProperty([0.2, 0.2, 0.2, 1])
    cor_led_amarelo = ColorProperty([0.2, 0.2, 0.2, 1])
    cor_led_vermelho = ColorProperty([0.2, 0.2, 0.2, 1])

    def build(self):
        self.socket_bluetooth = None
        self.input_stream = None
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
        # Lógica de conexão (substitua o MAC pelo do seu HC-05)
        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()
            device = adapter.getRemoteDevice("00:14:03:06:12:84")
            UUID = autoclass('java.util.UUID')
            spp_uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
            self.socket_bluetooth = device.createRfcommSocketToServiceRecord(spp_uuid)
            self.socket_bluetooth.connect()
            self.input_stream = self.socket_bluetooth.getInputStream()
            self.output_stream = self.socket_bluetooth.getOutputStream()
            self.conectado = True
            self.texto_conexao = "DESCONECTAR"
        except Exception as e:
            self.status_bomba = "ERRO"

    def enviar_comando(self, comando):
        if self.output_stream:
            self.output_stream.write(comando.encode('utf-8'))

    def mostrar_info(self):
        self.status_bomba = "H2O Pro v1.1"

if __name__ == '__main__':
    SupervisorioTechApp().run()


from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty
import threading

try:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.BLUETOOTH_CONNECT,
        Permission.BLUETOOTH_SCAN,
        Permission.ACCESS_FINE_LOCATION
    ])
    ON_ANDROID = True
except ImportError:
    ON_ANDROID = False

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.bg_dark

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "H2O PRO - SISTEMA SUPERVISÓRIO"
            elevation: 4
            pos_hint: {"top": 1}
            md_bg_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 0, 0.8, 1, 1
            right_action_items: [["water-pump", lambda x: app.mostrar_info()]]

        MDGridLayout:
            cols: 2
            padding: "15dp"
            spacing: "15dp"

            MDCard:
                orientation: 'vertical'
                padding: "10dp"
                size_hint: 1, 1
                elevation: 2
                radius: [15, ]
                md_bg_color: 0.15, 0.15, 0.15, 1

                MDLabel:
                    text: "NÍVEL DO RESERVATÓRIO"
                    halign: "center"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    size_hint_y: None
                    height: "30dp"

                MDRelativeLayout:
                    size_hint: None, None
                    size: "120dp", "250dp"
                    pos_hint: {"center_x": .5}

                    MDCard:
                        size_hint: 1, 1
                        md_bg_color: 0.3, 0.3, 0.3, 1
                        radius: [0, 0, 20, 20]

                    MDCard:
                        size_hint: 1, None
                        height: app.nivel_grafico
                        md_bg_color: 0, 0.5, 0.9, 0.8
                        radius: [0, 0, 20, 20]
                        pos_hint: {"bottom": 1}

                    MDLabel:
                        text: "100%"
                        pos_hint: {"top": 1.1, "x": 1.1}
                        theme_text_color: "Hint"
                    MDLabel:
                        text: "0%"
                        pos_hint: {"bottom": 0.9, "x": 1.1}
                        theme_text_color: "Hint"

            MDBoxLayout:
                orientation: 'vertical'
                spacing: "15dp"

                MDCard:
                    padding: "15dp"
                    elevation: 1
                    radius: [15, ]
                    md_bg_color: 0.12, 0.12, 0.12, 1
                    size_hint_y: None
                    height: "100dp"

                    MDIcon:
                        icon: "engine"
                        font_size: "48sp"
                        theme_text_color: "Custom"
                        text_color: app.cor_bomba
                        pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: ["15dp", 0, 0, 0]
                        MDLabel:
                            text: "ESTADO DO MOTOR"
                            theme_text_color: "Hint"
                            font_style: "Caption"
                        MDLabel:
                            text: app.status_bomba
                            font_style: "H5"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.cor_bomba

                MDCard:
                    orientation: 'vertical'
                    padding: "15dp"
                    spacing: "10dp"
                    elevation: 1
                    radius: [15, ]
                    md_bg_color: 0.12, 0.12, 0.12, 1

                    MDLabel:
                        text: "SENSORES DE NÍVEL"
                        font_style: "Subtitle1"
                        theme_text_color: "Primary"

                    MDBoxLayout:
                        MDIcon:
                            icon: "arrow-up-bold-circle"
                            text_color: app.cor_alto
                            theme_text_color: "Custom"
                        MDLabel:
                            text: "Nível Alto (Boia)"
                            theme_text_color: "Custom"
                            text_color: app.cor_alto

                    MDBoxLayout:
                        MDIcon:
                            icon: "arrow-down-bold-circle"
                            text_color: app.cor_baixo
                            theme_text_color: "Custom"
                        MDLabel:
                            text: "Nível Baixo (Boia)"
                            theme_text_color: "Custom"
                            text_color: app.cor_baixo

                MDFillRoundFlatIconButton:
                    icon: "bluetooth"
                    text: app.texto_conexao
                    md_bg_color: app.cor_conexao
                    size_hint_x: 1
                    height: "50dp"
                    on_release: app.alternar_conexao()

        MDBoxLayout:
            size_hint_y: None
            height: "80dp"
            padding: "10dp"
            spacing: "10dp"

            MDRaisedButton:
                text: "FORÇAR LIGAR"
                md_bg_color: 0, 0.7, 0.3, 1
                size_hint_x: 0.5
                on_release: app.enviar_comando('L')

            MDRaisedButton:
                text: "FORÇAR DESLIGAR"
                md_bg_color: 0.8, 0.1, 0.1, 1
                size_hint_x: 0.5
                on_release: app.enviar_comando('D')
'''

class SupervisorioTechApp(MDApp):
    status_bomba  = StringProperty("DESCONECTADO")
    cor_bomba     = ColorProperty([0.5, 0.5, 0.5, 1])
    nivel_grafico = NumericProperty(0)
    cor_alto      = ColorProperty([0.3, 0.3, 0.3, 1])
    cor_baixo     = ColorProperty([0.3, 0.3, 0.3, 1])
    texto_conexao = StringProperty("CONECTAR")
    cor_conexao   = ColorProperty([0.2, 0.2, 0.2, 1])
    conectado     = BooleanProperty(False)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.socket_bluetooth = None
        self.input_stream = None
        self.output_stream = None
        return Builder.load_string(KV)

    def alternar_conexao(self):
        if not self.conectado:
            self.conectar_bluetooth()
        else:
            self.desconectar_bluetooth()

    def conectar_bluetooth(self):
        if not ON_ANDROID:
            self.atualizar_interface_simulada()
            self.status_bomba = "MODO TESTE"
            self.cor_conexao = [0, 0.7, 0.3, 1]
            self.texto_conexao = "DESCONECTAR"
            self.conectado = True
            return
        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            UUID = autoclass('java.util.UUID')
            adaptador = BluetoothAdapter.getDefaultAdapter()
            if not adaptador.isEnabled():
                self.status_bomba = "ATIVE O BT"
                return
            MAC_HC05 = "00:14:03:06:12:84"
            dispositivo = adaptador.getRemoteDevice(MAC_HC05)
            spp_uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
            self.socket_bluetooth = dispositivo.createRfcommSocketToServiceRecord(spp_uuid)
            self.socket_bluetooth.connect()
            self.input_stream = self.socket_bluetooth.getInputStream()
            self.output_stream = self.socket_bluetooth.getOutputStream()
            self.texto_conexao = "CONECTADO"
            self.cor_conexao = [0, 0.7, 0.3, 1]
            self.conectado = True
            threading.Thread(target=self.ler_dados_serial, daemon=True).start()
        except Exception:
            self.texto_conexao = "ERRO CONEXÃO"
            self.cor_conexao = [0.8, 0.1, 0.1, 1]

    def desconectar_bluetooth(self):
        self.conectado = False
        self.texto_conexao = "CONECTAR"
        self.cor_conexao = [0.2, 0.2, 0.2, 1]
        self.nivel_grafico = 0
        self.cor_alto = [0.3, 0.3, 0.3, 1]
        self.cor_baixo = [0.3, 0.3, 0.3, 1]
        self.status_bomba = "DESCONECTADO"
        self.cor_bomba = [0.5, 0.5, 0.5, 1]
        if self.socket_bluetooth:
            self.socket_bluetooth.close()

    def ler_dados_serial(self):
        buffer = ""
        while self.conectado:
            try:
                if self.input_stream.available() > 0:
                    char_lido = chr(self.input_stream.read())
                    if char_lido == '\n':
                        dados = buffer.strip()
                        Clock.schedule_once(lambda dt, d=dados: self.processar_dados_arduino(d))
                        buffer = ""
                    else:
                        buffer += char_lido
            except:
                break

    def processar_dados_arduino(self, pacote_dados):
        try:
            partes = pacote_dados.split(';')
            if len(partes) == 3:
                st_bomba, st_baixo, st_alto = partes
                if st_bomba == "LIGADA":
                    self.status_bomba = "EM OPERAÇÃO"
                    self.cor_bomba = [0, 1, 0.5, 1]
                else:
                    self.status_bomba = "PARADO"
                    self.cor_bomba = [1, 0.2, 0.2, 1]
                if st_alto == "COM_AGUA":
                    self.nivel_grafico = 250
                    self.cor_alto = [0, 0.8, 1, 1]
                    self.cor_baixo = [0, 0.8, 1, 1]
                elif st_baixo == "COM_AGUA":
                    self.nivel_grafico = 125
                    self.cor_alto = [0.3, 0.3, 0.3, 1]
                    self.cor_baixo = [0, 0.8, 1, 1]
                else:
                    self.nivel_grafico = 10
                    self.cor_alto = [0.3, 0.3, 0.3, 1]
                    self.cor_baixo = [1, 0.6, 0, 1]
        except Exception:
            pass

    def enviar_comando(self, comando):
        if self.output_stream and self.conectado:
            try:
                comando_byte = autoclass('java.lang.String')(comando).getBytes()
                self.output_stream.write(comando_byte)
            except Exception:
                pass

    def mostrar_info(self):
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text="H2O Pro v1.0 - Monitoramento Ativo").open()

    def atualizar_interface_simulada(self):
        self.nivel_grafico = 125
        self.cor_baixo = [0, 0.8, 1, 1]
        self.cor_alto = [0.3, 0.3, 0.3, 1]
        self.status_bomba = "SIMULAÇÃO ON"
        self.cor_bomba = [0, 1, 0.5, 1]

if __name__ == '__main__':
    SupervisorioTechApp().run()

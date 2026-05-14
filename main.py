from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty
from kivy.metrics import dp
import threading

try:
    from jnius import autoclass
    import android  # noqa
    ON_ANDROID = True
except ImportError:
    ON_ANDROID = False

KV = '''
MDScreen:
    md_bg_color: 0.1, 0.1, 0.1, 1

    MDBoxLayout:
        orientation: 'vertical'

        # Top bar manual
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            padding: "12dp", "8dp"
            spacing: "8dp"
            md_bg_color: 0.08, 0.08, 0.08, 1

            MDLabel:
                text: "H2O PRO - SISTEMA SUPERVISORIO"
                font_style: "titleMedium"
                theme_text_color: "Custom"
                text_color: 0, 0.8, 1, 1
                halign: "left"
                valign: "center"

            MDIconButton:
                icon: "information-outline"
                theme_icon_color: "Custom"
                icon_color: 0, 0.8, 1, 1
                size_hint_x: None
                width: "48dp"
                on_release: app.mostrar_info()

        # Grade principal
        MDBoxLayout:
            orientation: 'horizontal'
            padding: "12dp"
            spacing: "12dp"
            size_hint_y: 1

            # Card reservatorio
            MDCard:
                size_hint_x: 0.45
                padding: "10dp"
                radius: [15,]
                md_bg_color: 0.15, 0.15, 0.15, 1

                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "8dp"

                    MDLabel:
                        text: "NIVEL"
                        halign: "center"
                        font_style: "labelLarge"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        size_hint_y: None
                        height: "24dp"

                    MDLabel:
                        text: "RESERVATORIO"
                        halign: "center"
                        font_style: "labelSmall"
                        theme_text_color: "Custom"
                        text_color: 0.7, 0.7, 0.7, 1
                        size_hint_y: None
                        height: "20dp"

                    Widget:
                        size_hint: None, None
                        size: "90dp", "220dp"
                        pos_hint: {"center_x": .5}
                        canvas:
                            Color:
                                rgba: 0.3, 0.3, 0.3, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [0, 0, 14, 14]
                            Color:
                                rgba: 0, 0.5, 0.9, 0.85
                            RoundedRectangle:
                                pos: self.pos
                                size: self.width, app.nivel_grafico
                                radius: [0, 0, 14, 14]

            # Coluna direita
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.55
                spacing: "10dp"

                # Card motor
                MDCard:
                    size_hint_y: None
                    height: "90dp"
                    padding: "12dp"
                    radius: [15,]
                    md_bg_color: 0.12, 0.12, 0.12, 1

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: "8dp"

                        MDIcon:
                            icon: "engine"
                            font_size: "40sp"
                            theme_text_color: "Custom"
                            text_color: app.cor_bomba
                            size_hint_x: None
                            width: "48dp"
                            pos_hint: {"center_y": .5}

                        MDBoxLayout:
                            orientation: 'vertical'
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "ESTADO DO MOTOR"
                                theme_text_color: "Custom"
                                text_color: 0.6, 0.6, 0.6, 1
                                font_style: "labelSmall"
                                size_hint_y: None
                                height: "20dp"

                            MDLabel:
                                text: app.status_bomba
                                font_style: "titleMedium"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.cor_bomba

                # Card sensores
                MDCard:
                    size_hint_y: None
                    height: "110dp"
                    padding: "12dp"
                    radius: [15,]
                    md_bg_color: 0.12, 0.12, 0.12, 1

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: "8dp"

                        MDLabel:
                            text: "SENSORES DE NIVEL"
                            font_style: "labelMedium"
                            theme_text_color: "Custom"
                            text_color: 0.8, 0.8, 0.8, 1
                            size_hint_y: None
                            height: "20dp"

                        MDBoxLayout:
                            spacing: "8dp"
                            size_hint_y: None
                            height: "28dp"
                            MDIcon:
                                icon: "arrow-up-bold-circle"
                                theme_text_color: "Custom"
                                text_color: app.cor_alto
                                size_hint_x: None
                                width: "28dp"
                            MDLabel:
                                text: "Boia Alta"
                                theme_text_color: "Custom"
                                text_color: app.cor_alto
                                font_style: "bodySmall"

                        MDBoxLayout:
                            spacing: "8dp"
                            size_hint_y: None
                            height: "28dp"
                            MDIcon:
                                icon: "arrow-down-bold-circle"
                                theme_text_color: "Custom"
                                text_color: app.cor_baixo
                                size_hint_x: None
                                width: "28dp"
                            MDLabel:
                                text: "Boia Baixa"
                                theme_text_color: "Custom"
                                text_color: app.cor_baixo
                                font_style: "bodySmall"

                # Botao Bluetooth
                MDButton:
                    style: "filled"
                    size_hint_x: 1
                    height: "48dp"
                    on_release: app.alternar_conexao()
                    pos_hint: {"center_x": .5}
                    theme_bg_color: "Custom"
                    md_bg_color: app.cor_conexao

                    MDButtonIcon:
                        icon: "bluetooth"

                    MDButtonText:
                        text: app.texto_conexao

        # Botoes LIGAR / DESLIGAR
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "12dp", "8dp"
            spacing: "12dp"

            MDButton:
                style: "filled"
                size_hint_x: 0.5
                height: "50dp"
                theme_bg_color: "Custom"
                md_bg_color: 0, 0.7, 0.3, 1
                on_release: app.enviar_comando('L')

                MDButtonText:
                    text: "LIGAR"

            MDButton:
                style: "filled"
                size_hint_x: 0.5
                height: "50dp"
                theme_bg_color: "Custom"
                md_bg_color: 0.8, 0.1, 0.1, 1
                on_release: app.enviar_comando('D')

                MDButtonText:
                    text: "DESLIGAR"
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

    def on_start(self):
        # ✅ Permissoes pedidas DEPOIS do app estar pronto — evita crash
        if ON_ANDROID:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.BLUETOOTH,
                Permission.BLUETOOTH_ADMIN,
                Permission.BLUETOOTH_CONNECT,
                Permission.BLUETOOTH_SCAN,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
            ])

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
            self.texto_conexao = "ERRO CONEXAO"
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
            try:
                self.socket_bluetooth.close()
            except Exception:
                pass
            self.socket_bluetooth = None

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
            except Exception:
                break

    def processar_dados_arduino(self, pacote_dados):
        try:
            partes = pacote_dados.split(';')
            if len(partes) == 3:
                st_bomba, st_baixo, st_alto = partes
                if st_bomba == "LIGADA":
                    self.status_bomba = "EM OPERACAO"
                    self.cor_bomba = [0, 1, 0.5, 1]
                else:
                    self.status_bomba = "PARADO"
                    self.cor_bomba = [1, 0.2, 0.2, 1]

                if st_alto == "COM_AGUA":
                    self.nivel_grafico = dp(220)
                    self.cor_alto = [0, 0.8, 1, 1]
                    self.cor_baixo = [0, 0.8, 1, 1]
                elif st_baixo == "COM_AGUA":
                    self.nivel_grafico = dp(110)
                    self.cor_alto = [0.3, 0.3, 0.3, 1]
                    self.cor_baixo = [0, 0.8, 1, 1]
                else:
                    self.nivel_grafico = dp(10)
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
        from kivymd.uix.snackbar import MDSnackbar
        from kivymd.uix.label import MDLabel
        snack = MDSnackbar(
            MDLabel(text="H2O Pro v1.0 - Monitoramento Ativo"),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9,
        )
        snack.open()

    def atualizar_interface_simulada(self):
        self.nivel_grafico = dp(110)
        self.cor_baixo = [0, 0.8, 1, 1]
        self.cor_alto = [0.3, 0.3, 0.3, 1]
        self.status_bomba = "SIMULACAO ON"
        self.cor_bomba = [0, 1, 0.5, 1]


if __name__ == '__main__':
    SupervisorioTechApp().run()

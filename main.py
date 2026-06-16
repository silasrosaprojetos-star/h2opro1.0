from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
import threading

try:
    from jnius import autoclass
    import android  # noqa
    ON_ANDROID = True
except ImportError:
    ON_ANDROID = False

BLE_MAC = "E1:EF:6B:52:BF:16"
BLE_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
BLE_CHAR_NOTIFY  = "0000ffe1-0000-1000-8000-00805f9b34fb"
BLE_CHAR_WRITE   = "0000ffe2-0000-1000-8000-00805f9b34fb"

KV = '''
Screen:
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: None
            height: "56dp"
            padding: "12dp", "8dp"
            spacing: "8dp"
            canvas.before:
                Color:
                    rgba: 0.08, 0.08, 0.08, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "H2O PRO - SUPERVISORIO"
                color: 0, 0.8, 1, 1
                bold: True
                font_size: "14sp"
                halign: "left"
                valign: "center"
                text_size: self.size

            Button:
                text: "INFO"
                size_hint_x: None
                width: "60dp"
                background_normal: ''
                background_color: 0, 0.5, 0.8, 1
                color: 1, 1, 1, 1
                font_size: "11sp"
                on_release: app.mostrar_info()

        BoxLayout:
            orientation: 'horizontal'
            padding: "10dp"
            spacing: "10dp"
            size_hint_y: 1

            BoxLayout:
                size_hint_x: 0.42
                orientation: 'vertical'
                spacing: "6dp"
                canvas.before:
                    Color:
                        rgba: 0.15, 0.15, 0.15, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [14, 14, 14, 14]

                Label:
                    text: "NIVEL DO\\nRESERVATORIO"
                    color: 1, 1, 1, 1
                    bold: True
                    font_size: "11sp"
                    halign: "center"
                    size_hint_y: None
                    height: "44dp"

                Widget:
                    size_hint: None, None
                    size: "75dp", "200dp"
                    pos_hint: {"center_x": .5}
                    canvas:
                        Color:
                            rgba: 0.3, 0.3, 0.3, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [0, 0, 12, 12]
                        Color:
                            rgba: 0, 0.5, 0.9, 0.85
                        RoundedRectangle:
                            pos: self.pos
                            size: self.width, app.nivel_grafico
                            radius: [0, 0, 12, 12]

                Label:
                    text: ""
                    size_hint_y: 1

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.58
                spacing: "8dp"

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: "85dp"
                    padding: "10dp"
                    spacing: "4dp"
                    canvas.before:
                        Color:
                            rgba: 0.12, 0.12, 0.12, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [14, 14, 14, 14]

                    Label:
                        text: "ESTADO DO MOTOR"
                        color: 0.5, 0.5, 0.5, 1
                        font_size: "10sp"
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: "18dp"

                    Label:
                        text: app.status_bomba
                        color: app.cor_bomba
                        bold: True
                        font_size: "15sp"
                        halign: "left"
                        text_size: self.size

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: "100dp"
                    padding: "10dp"
                    spacing: "4dp"
                    canvas.before:
                        Color:
                            rgba: 0.12, 0.12, 0.12, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [14, 14, 14, 14]

                    Label:
                        text: "SENSORES DE NIVEL"
                        color: 0.7, 0.7, 0.7, 1
                        font_size: "10sp"
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: "18dp"

                    Label:
                        text: "▲ Boia Alta"
                        color: app.cor_alto
                        font_size: "13sp"
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: "26dp"

                    Label:
                        text: "▼ Boia Baixa"
                        color: app.cor_baixo
                        font_size: "13sp"
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: "26dp"

                Button:
                    text: app.texto_conexao
                    size_hint_y: None
                    height: "44dp"
                    background_normal: ''
                    background_color: app.cor_conexao
                    color: 1, 1, 1, 1
                    bold: True
                    font_size: "12sp"
                    on_release: app.alternar_conexao()

                Widget:
                    size_hint_y: 1

        BoxLayout:
            size_hint_y: None
            height: "65dp"
            padding: "10dp", "6dp"
            spacing: "10dp"

            Button:
                text: "LIGAR"
                background_normal: ''
                background_color: 0, 0.7, 0.3, 1
                color: 1, 1, 1, 1
                bold: True
                font_size: "15sp"
                on_release: app.enviar_comando('L')

            Button:
                text: "DESLIGAR"
                background_normal: ''
                background_color: 0.8, 0.1, 0.1, 1
                color: 1, 1, 1, 1
                bold: True
                font_size: "15sp"
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
        self.gatt         = None
        self.char_write   = None
        self.callback_obj = None
        return Builder.load_string(KV)

    def on_start(self):
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
            self.conectar_ble()
        else:
            self.desconectar_ble()

    def conectar_ble(self):
        if not ON_ANDROID:
            self._simular()
            return
        threading.Thread(target=self._conectar_ble_thread, daemon=True).start()

    def _conectar_ble_thread(self):
        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()
            if not adapter.isEnabled():
                Clock.schedule_once(lambda dt: setattr(self, 'status_bomba', 'ATIVE O BT'))
                return

            device = adapter.getRemoteDevice(BLE_MAC)

            Context     = autoclass('android.content.Context')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            ctx = PythonActivity.mActivity

            CallbackClass = autoclass('com.h2opro.BleCallback') if False else None

            # Usa BluetoothGattCallback via reflection
            BluetoothGattCallback = autoclass('android.bluetooth.BluetoothGattCallback')
            BluetoothGatt         = autoclass('android.bluetooth.BluetoothGatt')
            BluetoothGattService  = autoclass('android.bluetooth.BluetoothGattService')
            UUID                  = autoclass('java.util.UUID')

            app = self

            class GattCallback(BluetoothGattCallback):
                def onConnectionStateChange(self, gatt, status, newState):
                    if newState == 2:  # STATE_CONNECTED
                        gatt.discoverServices()
                        Clock.schedule_once(lambda dt: app._on_connected(gatt))
                    else:
                        Clock.schedule_once(lambda dt: app._on_disconnected())

                def onServicesDiscovered(self, gatt, status):
                    try:
                        svc_uuid  = UUID.fromString(BLE_SERVICE_UUID)
                        char_uuid = UUID.fromString(BLE_CHAR_WRITE)
                        svc  = gatt.getService(svc_uuid)
                        char = svc.getCharacteristic(char_uuid)
                        app.char_write = char

                        # Habilita notificações
                        notify_uuid = UUID.fromString(BLE_CHAR_NOTIFY)
                        notify_char = svc.getCharacteristic(notify_uuid)
                        gatt.setCharacteristicNotification(notify_char, True)
                    except Exception as e:
                        Clock.schedule_once(lambda dt: setattr(app, 'status_bomba', 'ERRO SERVICO'))

                def onCharacteristicChanged(self, gatt, characteristic):
                    try:
                        data = characteristic.getStringValue(0)
                        Clock.schedule_once(lambda dt, d=data: app.processar_dados_arduino(d))
                    except Exception:
                        pass

            self.callback_obj = GattCallback()
            self.gatt = device.connectGatt(ctx, False, self.callback_obj)

        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_erro_conexao())

    def _on_connected(self, gatt):
        self.gatt = gatt
        self.conectado = True
        self.texto_conexao = "CONECTADO"
        self.cor_conexao   = [0, 0.7, 0.3, 1]
        self.status_bomba  = "CONECTADO"

    def _on_disconnected(self):
        self.conectado     = False
        self.texto_conexao = "CONECTAR"
        self.cor_conexao   = [0.2, 0.2, 0.2, 1]
        self.status_bomba  = "DESCONECTADO"
        self.cor_bomba     = [0.5, 0.5, 0.5, 1]
        self.nivel_grafico = 0
        self.cor_alto      = [0.3, 0.3, 0.3, 1]
        self.cor_baixo     = [0.3, 0.3, 0.3, 1]

    def _on_erro_conexao(self):
        self.texto_conexao = "ERRO CONEXAO"
        self.cor_conexao   = [0.8, 0.1, 0.1, 1]

    def desconectar_ble(self):
        self.conectado = False
        if self.gatt:
            try:
                self.gatt.disconnect()
                self.gatt.close()
            except Exception:
                pass
            self.gatt = None
        self._on_disconnected()

    def enviar_comando(self, comando):
        if not self.conectado:
            return
        if not ON_ANDROID:
            self.status_bomba = "LIGADA" if comando == 'L' else "PARADO"
            self.cor_bomba    = [0, 1, 0.5, 1] if comando == 'L' else [1, 0.2, 0.2, 1]
            return
        try:
            self.char_write.setValue(comando.encode('utf-8'))
            self.gatt.writeCharacteristic(self.char_write)
        except Exception:
            pass

    def processar_dados_arduino(self, pacote_dados):
        try:
            partes = pacote_dados.strip().split(';')
            if len(partes) == 3:
                st_bomba, st_baixo, st_alto = partes
                if st_bomba == "LIGADA":
                    self.status_bomba = "EM OPERACAO"
                    self.cor_bomba    = [0, 1, 0.5, 1]
                else:
                    self.status_bomba = "PARADO"
                    self.cor_bomba    = [1, 0.2, 0.2, 1]

                if st_alto == "COM_AGUA":
                    self.nivel_grafico = dp(200)
                    self.cor_alto      = [0, 0.8, 1, 1]
                    self.cor_baixo     = [0, 0.8, 1, 1]
                elif st_baixo == "COM_AGUA":
                    self.nivel_grafico = dp(100)
                    self.cor_alto      = [0.3, 0.3, 0.3, 1]
                    self.cor_baixo     = [0, 0.8, 1, 1]
                else:
                    self.nivel_grafico = dp(10)
                    self.cor_alto      = [0.3, 0.3, 0.3, 1]
                    self.cor_baixo     = [1, 0.6, 0, 1]
        except Exception:
            pass

    def mostrar_info(self):
        self.status_bomba = "H2O Pro v1.0 BLE"
        Clock.schedule_once(lambda dt: self.resetar_status(), 2)

    def resetar_status(self):
        if not self.conectado:
            self.status_bomba = "DESCONECTADO"

    def _simular(self):
        self.nivel_grafico = dp(100)
        self.cor_baixo     = [0, 0.8, 1, 1]
        self.cor_alto      = [0.3, 0.3, 0.3, 1]
        self.status_bomba  = "SIMULACAO ON"
        self.cor_bomba     = [0, 1, 0.5, 1]
        self.conectado     = True
        self.texto_conexao = "DESCONECTAR"
        self.cor_conexao   = [0, 0.7, 0.3, 1]


if __name__ == '__main__':
    SupervisorioTechApp().run()

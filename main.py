# ============================================================
#  H2O Pro v1.1 - Supervisório Bluetooth
#  Farad Automação
#  Compatível com firmware H2O Pro v1.0 (Arduino UNO + HC-05)
#  Protocolo RX: "BOMBA;BOIA_BAIXA;BOIA_ALTA\n"
#  Protocolo TX: 'L' = Ligar | 'D' = Desligar
# ============================================================

from kivymd.app import MDApp
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

# ============================================================
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
        spacing: 0

        # ── Topbar ──────────────────────────────────────────
        BoxLayout:
            size_hint_y: None
            height: "52dp"
            padding: "12dp", "8dp"
            spacing: "8dp"
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
                font_size: "16sp"
                halign: "left"
                valign: "center"
                text_size: self.size
                size_hint_x: None
                width: "90dp"

            Label:
                text: app.nome_estado
                color: app.cor_estado
                bold: True
                font_size: "11sp"
                halign: "center"
                valign: "center"
                text_size: self.size

            Button:
                text: "INFO"
                size_hint_x: None
                width: "52dp"
                background_normal: ''
                background_color: 0, 0.4, 0.7, 1
                color: 1, 1, 1, 1
                font_size: "10sp"
                on_release: app.mostrar_info()

        # ── Corpo principal ──────────────────────────────────
        BoxLayout:
            orientation: 'horizontal'
            padding: "10dp"
            spacing: "10dp"
            size_hint_y: 1

            # Coluna esquerda - reservatório
            BoxLayout:
                size_hint_x: 0.40
                orientation: 'vertical'
                spacing: "6dp"
                canvas.before:
                    Color:
                        rgba: 0.13, 0.13, 0.13, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [14]

                Label:
                    text: "NÍVEL DO\\nRESERVATÓRIO"
                    color: 1, 1, 1, 1
                    bold: True
                    font_size: "10sp"
                    halign: "center"
                    size_hint_y: None
                    height: "40dp"

                # Tanque animado
                Widget:
                    size_hint: None, None
                    size: "72dp", "190dp"
                    pos_hint: {"center_x": .5}
                    canvas:
                        Color:
                            rgba: 0.25, 0.25, 0.25, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [0, 0, 10, 10]
                        Color:
                            rgba: app.cor_agua
                        RoundedRectangle:
                            pos: self.pos
                            size: self.width, app.nivel_grafico
                            radius: [0, 0, 10, 10]
                        # Linha boia superior
                        Color:
                            rgba: 1, 0.3, 0.3, 0.8
                        Rectangle:
                            pos: self.x, self.y + self.height * 0.80
                            size: self.width, dp(1.5)
                        # Linha boia inferior
                        Color:
                            rgba: 1, 0.7, 0, 0.8
                        Rectangle:
                            pos: self.x, self.y + self.height * 0.35
                            size: self.width, dp(1.5)

                Label:
                    text: app.pct_nivel
                    color: 0, 0.8, 1, 1
                    bold: True
                    font_size: "14sp"
                    halign: "center"
                    size_hint_y: None
                    height: "28dp"

                # LEDs indicadores
                BoxLayout:
                    size_hint_y: None
                    height: "28dp"
                    spacing: "8dp"
                    padding: "12dp", 0
                    Label:
                        text: "●"
                        color: app.cor_led_verde
                        font_size: "18sp"
                        halign: "center"
                    Label:
                        text: "●"
                        color: app.cor_led_amarelo
                        font_size: "18sp"
                        halign: "center"
                    Label:
                        text: "●"
                        color: app.cor_led_vermelho
                        font_size: "18sp"
                        halign: "center"

                Label:
                    text: "V    A    R"
                    color: 0.4, 0.4, 0.4, 1
                    font_size: "9sp"
                    halign: "center"
                    size_hint_y: None
                    height: "16dp"

                Widget:
                    size_hint_y: 1

            # Coluna direita
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.60
                spacing: "8dp"

                # Card bomba
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: "76dp"
                    padding: "10dp"
                    spacing: "2dp"
                    canvas.before:
                        Color:
                            rgba: 0.11, 0.11, 0.11, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12]
                    Label:
                        text: "ESTADO DA BOMBA"
                        color: 0.5, 0.5, 0.5, 1
                        font_size: "9sp"
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: "18dp"
                    Label:
                        text: app.status_bomba
                        color: app.cor_bomba
                        bold: True
                        font_size: "14sp"
                        halign: "left"
                        text_size: self.size

                # Card sensores
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: "92dp"
                    padding: "10dp"
                    spacing: "2dp"
                    canvas.before:
                        Color:
                            rgba: 0.11, 0.11, 0.11, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12]
                    Label:
                        text: "SENSORES DE NÍVEL"
                        color: 0.5, 0.5, 0.5, 1
                        font_size: "9sp"
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: "18dp"
                    BoxLayout:
                        spacing: "6dp"
                        size_hint_y: None
                        height: "24dp"
                        Label:
                            text: "●"
                            color: app.cor_alto
                            font_size: "16sp"
                            size_hint_x: None
                            width: "20dp"
                        Label:
                            text: "▲ Boia Alta"
                            color: app.cor_alto
                            font_size: "12sp"
                            halign: "left"
                            text_size: self.size
                    BoxLayout:
                        spacing: "6dp"
                        size_hint_y: None
                        height: "24dp"
                        Label:
                            text: "●"
                            color: app.cor_baixo
                            font_size: "16sp"
                            size_hint_x: None
                            width: "20dp"
                        Label:
                            text: "▼ Boia Baixa"
                            color: app.cor_baixo
                            font_size: "12sp"
                            halign: "left"
                            text_size: self.size

                # Card log (últimas mensagens)
                BoxLayout:
                    orientation: 'vertical'
                    padding: "8dp"
                    spacing: "2dp"
                    canvas.before:
                        Color:
                            rgba: 0.08, 0.08, 0.08, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12]
                    Label:
                        text: "LOG"
                        color: 0.4, 0.4, 0.4, 1
                        font_size: "9sp"
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: "16dp"
                    Label:
                        id: log1
                        text: app.log_linha1
                        color: 0.5, 0.9, 0.5, 1
                        font_size: "9sp"
                        halign: "left"
                        text_size: self.size
                    Label:
                        id: log2
                        text: app.log_linha2
                        color: 0.5, 0.9, 0.5, 1
                        font_size: "9sp"
                        halign: "left"
                        text_size: self.size
                    Label:
                        id: log3
                        text: app.log_linha3
                        color: 0.5, 0.9, 0.5, 1
                        font_size: "9sp"
                        halign: "left"
                        text_size: self.size

                # Botão Bluetooth
                Button:
                    text: app.texto_conexao
                    size_hint_y: None
                    height: "40dp"
                    background_normal: ''
                    background_color: app.cor_conexao
                    color: 1, 1, 1, 1
                    bold: True
                    font_size: "11sp"
                    on_release: app.alternar_conexao()

        # ── Rodapé: LIGAR / DESLIGAR ─────────────────────────
        BoxLayout:
            size_hint_y: None
            height: "62dp"
            padding: "10dp", "6dp"
            spacing: "10dp"
            canvas.before:
                Color:
                    rgba: 0.05, 0.05, 0.05, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Button:
                text: "⏵  LIGAR"
                background_normal: ''
                background_color: 0, 0.72, 0.32, 1
                color: 1, 1, 1, 1
                bold: True
                font_size: "14sp"
                on_release: app.enviar_comando('L')

            Button:
                text: "⏹  DESLIGAR"
                background_normal: ''
                background_color: 0.78, 0.1, 0.1, 1
                color: 1, 1, 1, 1
                bold: True
                font_size: "14sp"
                on_release: app.enviar_comando('D')
'''

# ============================================================
class H2OProApp(MDApp):

    # ── Propriedades reativas ────────────────────────────────
    status_bomba   = StringProperty("DESCONECTADO")
    cor_bomba      = ColorProperty([0.5, 0.5, 0.5, 1])
    nivel_grafico  = NumericProperty(0)
    cor_agua       = ColorProperty([0, 0.3, 0.6, 0.85])
    pct_nivel      = StringProperty("- %")
    cor_alto       = ColorProperty([0.25, 0.25, 0.25, 1])
    cor_baixo      = ColorProperty([0.25, 0.25, 0.25, 1])
    texto_conexao  = StringProperty("CONECTAR BLUETOOTH")
    cor_conexao    = ColorProperty([0.18, 0.18, 0.18, 1])
    conectado      = BooleanProperty(False)
    nome_estado    = StringProperty("AGUARDANDO CONEXÃO")
    cor_estado     = ColorProperty([0.5, 0.5, 0.5, 1])
    log_linha1     = StringProperty("")
    log_linha2     = StringProperty("")
    log_linha3     = StringProperty("")

    # LEDs
    cor_led_verde    = ColorProperty([0.15, 0.15, 0.15, 1])
    cor_led_amarelo  = ColorProperty([0.15, 0.15, 0.15, 1])
    cor_led_vermelho = ColorProperty([0.15, 0.15, 0.15, 1])

    # ── Internos ─────────────────────────────────────────────
    _log_buffer     = []
    _pisca_tick     = False
    _estado_arduino = "DESCONECTADO"

    # ── Build ─────────────────────────────────────────────────
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.socket_bluetooth = None
        self.input_stream     = None
        self.output_stream    = None
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_interval(self._piscar_leds, 0.5)
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

    # ── Conexão Bluetooth ────────────────────────────────────
    def alternar_conexao(self):
        if not self.conectado:
            self.conectar_bluetooth()
        else:
            self.desconectar_bluetooth()

    def conectar_bluetooth(self):
        if not ON_ANDROID:
            self._modo_teste()
            return
        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            UUID = autoclass('java.util.UUID')
            adaptador = BluetoothAdapter.getDefaultAdapter()
            if not adaptador.isEnabled():
                self._add_log("Ative o Bluetooth!")
                return
            MAC_HC05 = "00:14:03:06:12:84"
            dispositivo = adaptador.getRemoteDevice(MAC_HC05)
            spp_uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
            self.socket_bluetooth = dispositivo.createRfcommSocketToServiceRecord(spp_uuid)
            self.socket_bluetooth.connect()
            self.input_stream  = self.socket_bluetooth.getInputStream()
            self.output_stream = self.socket_bluetooth.getOutputStream()
            self._set_conectado(True)
            threading.Thread(target=self._ler_dados_serial, daemon=True).start()
        except Exception as e:
            self.texto_conexao = "ERRO DE CONEXÃO"
            self.cor_conexao   = [0.8, 0.1, 0.1, 1]
            self._add_log("Erro BT: " + str(e)[:30])

    def desconectar_bluetooth(self):
        self._set_conectado(False)
        if self.socket_bluetooth:
            try:
                self.socket_bluetooth.close()
            except Exception:
                pass
            self.socket_bluetooth = None
        self._add_log("Bluetooth desconectado.")

    def _set_conectado(self, valor):
        self.conectado = valor
        if valor:
            self.texto_conexao = "CONECTADO  ●"
            self.cor_conexao   = [0, 0.55, 0.28, 1]
            self._add_log("Conectado ao HC-05.")
        else:
            self.texto_conexao    = "CONECTAR BLUETOOTH"
            self.cor_conexao      = [0.18, 0.18, 0.18, 1]
            self.status_bomba     = "DESCONECTADO"
            self.cor_bomba        = [0.5, 0.5, 0.5, 1]
            self.nivel_grafico    = 0
            self.pct_nivel        = "- %"
            self.cor_alto         = [0.25, 0.25, 0.25, 1]
            self.cor_baixo        = [0.25, 0.25, 0.25, 1]
            self.cor_agua         = [0, 0.3, 0.6, 0.85]
            self.nome_estado      = "DESCONECTADO"
            self.cor_estado       = [0.5, 0.5, 0.5, 1]
            self.cor_led_verde    = [0.15, 0.15, 0.15, 1]
            self.cor_led_amarelo  = [0.15, 0.15, 0.15, 1]
            self.cor_led_vermelho = [0.15, 0.15, 0.15, 1]
            self._estado_arduino  = "DESCONECTADO"

    # ── Leitura serial (thread) ───────────────────────────────
    def _ler_dados_serial(self):
        buffer = ""
        while self.conectado:
            try:
                if self.input_stream.available() > 0:
                    char_lido = chr(self.input_stream.read())
                    if char_lido == '\n':
                        dados = buffer.strip()
                        if dados:
                            Clock.schedule_once(
                                lambda dt, d=dados: self._processar_pacote(d)
                            )
                        buffer = ""
                    else:
                        buffer += char_lido
            except Exception:
                break

    # ── Processar pacote do Arduino ───────────────────────────
    def _processar_pacote(self, pacote):
        """
        Formato esperado: LIGADA;COM_AGUA;SEM_AGUA
        Campo 0 - bomba:      LIGADA | PARADO
        Campo 1 - boia baixa: COM_AGUA | SEM_AGUA
        Campo 2 - boia alta:  COM_AGUA | SEM_AGUA
        """
        # Log apenas pacotes de estado (não os de debug verbose)
        if ';' not in pacote:
            self._add_log(pacote[:38])
            return

        try:
            partes = pacote.split(';')
            if len(partes) != 3:
                return

            st_bomba, st_baixo, st_alto = partes
            bomba_ligada  = (st_bomba == "LIGADA")
            baixo_com_agua = (st_baixo == "COM_AGUA")
            alto_com_agua  = (st_alto  == "COM_AGUA")

            # ── Inferir estado pelo combinação dos sensores ──
            if alto_com_agua and not baixo_com_agua:
                estado = "FALHA"
            elif not bomba_ligada and not baixo_com_agua and not alto_com_agua:
                estado = "VAZIO"
            elif bomba_ligada and not baixo_com_agua and not alto_com_agua:
                estado = "ACIONANDO"
            elif bomba_ligada and baixo_com_agua and not alto_com_agua:
                estado = "ENCHENDO"
            elif not bomba_ligada and baixo_com_agua and alto_com_agua:
                estado = "CHEIO"
            elif not bomba_ligada and baixo_com_agua and not alto_com_agua:
                estado = "ESVAZIANDO"
            else:
                estado = self._estado_arduino  # mantém se ambíguo

            self._estado_arduino = estado
            self._atualizar_ui(estado, bomba_ligada, baixo_com_agua, alto_com_agua)

        except Exception:
            pass

    def _atualizar_ui(self, estado, bomba, baixo, alto):
        # ── Status da bomba ──
        if bomba:
            self.status_bomba = "EM OPERAÇÃO"
            self.cor_bomba    = [0, 1, 0.55, 1]
        else:
            self.status_bomba = "PARADA"
            self.cor_bomba    = [1, 0.25, 0.25, 1]

        # ── Sensores ──
        self.cor_baixo = [0, 0.8, 1, 1] if baixo else [1, 0.55, 0, 1]
        self.cor_alto  = [0, 0.8, 1, 1] if alto  else [0.25, 0.25, 0.25, 1]

        # ── Nível gráfico + cor da água ──
        if alto and baixo:
            nivel_pct = 90
            self.cor_agua = [0, 0.5, 0.9, 0.9]
        elif baixo:
            nivel_pct = 48
            self.cor_agua = [0, 0.4, 0.75, 0.85]
        else:
            nivel_pct = 5
            self.cor_agua = [0, 0.2, 0.5, 0.7]

        self.nivel_grafico = dp(190) * nivel_pct / 100
        self.pct_nivel     = f"{nivel_pct} %"

        # ── Nome e cor do estado ──
        mapa_estado = {
            "VAZIO":     ("VAZIO",           [0.55, 0.55, 0.55, 1]),
            "ACIONANDO": ("ACIONANDO...",    [1,    0.75, 0,    1]),
            "ENCHENDO":  ("ENCHENDO",        [0,    0.8,  1,    1]),
            "CHEIO":     ("CHEIO  ✔",        [0,    1,    0.45, 1]),
            "ESVAZIANDO":("ESVAZIANDO",      [0.3,  0.7,  1,    1]),
            "FALHA":     ("⚠  FALHA",        [1,    0.2,  0.2,  1]),
        }
        nome, cor = mapa_estado.get(estado, ("AGUARDANDO", [0.5, 0.5, 0.5, 1]))
        self.nome_estado = nome
        self.cor_estado  = cor

        # ── LEDs ──
        # Verde fixo = CHEIO | Verde pisca = ESVAZIANDO
        # Amarelo fixo = ENCHENDO | Amarelo pisca = ACIONANDO
        # Vermelho pisca = FALHA
        self._led_v_fixo    = (estado == "CHEIO")
        self._led_v_pisca   = (estado == "ESVAZIANDO")
        self._led_a_fixo    = (estado == "ENCHENDO")
        self._led_a_pisca   = (estado == "ACIONANDO")
        self._led_r_pisca   = (estado == "FALHA")

    # ── Piscamento de LEDs (clock 0.5s) ──────────────────────
    def _piscar_leds(self, dt):
        self._pisca_tick = not self._pisca_tick
        apagado = [0.12, 0.12, 0.12, 1]

        # Verde
        if getattr(self, '_led_v_fixo', False):
            self.cor_led_verde = [0, 1, 0.35, 1]
        elif getattr(self, '_led_v_pisca', False):
            self.cor_led_verde = [0, 1, 0.35, 1] if self._pisca_tick else apagado
        else:
            self.cor_led_verde = apagado

        # Amarelo
        if getattr(self, '_led_a_fixo', False):
            self.cor_led_amarelo = [1, 0.75, 0, 1]
        elif getattr(self, '_led_a_pisca', False):
            self.cor_led_amarelo = [1, 0.75, 0, 1] if self._pisca_tick else apagado
        else:
            self.cor_led_amarelo = apagado

        # Vermelho
        if getattr(self, '_led_r_pisca', False):
            self.cor_led_vermelho = [1, 0.18, 0.18, 1] if self._pisca_tick else apagado
        else:
            self.cor_led_vermelho = apagado

    # ── Enviar comando ao Arduino ─────────────────────────────
    def enviar_comando(self, comando):
        if not self.conectado:
            self._add_log("Sem conexão Bluetooth.")
            return
        if not ON_ANDROID:
            # Modo teste: simula o envio
            self._add_log(f"CMD enviado: '{comando}'")
            return
        try:
            cmd_bytes = autoclass('java.lang.String')(comando).getBytes()
            self.output_stream.write(cmd_bytes)
            self._add_log(f"CMD enviado: '{comando}'")
        except Exception:
            self._add_log("Erro ao enviar comando.")

    # ── Log de 3 linhas rolante ───────────────────────────────
    def _add_log(self, msg):
        self._log_buffer.append(msg[:40])
        if len(self._log_buffer) > 3:
            self._log_buffer.pop(0)
        linhas = self._log_buffer + [""] * (3 - len(self._log_buffer))
        self.log_linha1 = linhas[0]
        self.log_linha2 = linhas[1]
        self.log_linha3 = linhas[2]

    # ── Modo teste (sem Android) ──────────────────────────────
    def _modo_teste(self):
        self._set_conectado(True)
        self._add_log("Modo teste ativo.")
        # Simula pacote: bomba ligada, boia baixa com água
        Clock.schedule_once(
            lambda dt: self._processar_pacote("LIGADA;COM_AGUA;SEM_AGUA"), 1
        )

    # ── Botão INFO ────────────────────────────────────────────
    def mostrar_info(self):
        self._add_log("H2O Pro v1.1")
        self._add_log("Farad Automação")
        self._add_log(f"Estado: {self._estado_arduino}")


if __name__ == '__main__':
    H2OProApp().run()

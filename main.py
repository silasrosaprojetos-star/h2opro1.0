# ============================================================
#  H2O Pro v1.1 - Supervisório Bluetooth
#  Farad Automação / S.ROSA ENGENHARIA.
#  Compatível com firmware H2O Pro v1.0 (Arduino UNO + HC-06)
#  Protocolo RX: "BOMBA;BOIA_BAIXA;BOIA_ALTA\n"
#  Protocolo TX: 'L' = Ligar | 'D' = Desligar | 'R' = Reset
# ============================================================

import time
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
                    size_hint

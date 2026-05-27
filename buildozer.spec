[app]

# (str) Title of your application
title = H2O Pro

# (str) Package name
package.name = h2opro

# (str) Package domain (needed for android/ios packaging)
package.domain = org.silas

# (str) Source code where the main.py lives
source.dir = .

# (list) Application requirements
# IMPORTANTE: Coloque aqui as bibliotecas que seu código Python usa (kivy é obrigatório)
requirements = python3,kivy

# (str) Supported orientation (landscape, sensor, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# --- Configurações para não dar erro no GitHub Actions ---
# Aceitar as licenças do SDK do Android automaticamente
android.accept_sdk_license = True

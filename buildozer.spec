[app]

# (str) Título do seu aplicativo
title = H2O Pro

# (str) Nome do pacote (não use espaços ou caracteres especiais)
package.name = h2opro

# (str) Domínio do pacote (necessário para empacotamento android/ios)
package.domain = org.silasrosaprojetos

# (str) Diretório onde o código-fonte (main.py) está localizado
# O ponto significa "na pasta atual". (Isso resolve o seu erro do GitHub Actions)
source.dir = .

# (list) Extensões de arquivos que devem ser incluídos no aplicativo
source.include_exts = py,png,jpg,kv,atlas,ttf,html

# (str) Versão do aplicativo
version = 1.0

# (list) Dependências do seu aplicativo (bibliotecas Python necessárias)
# Se você usa KivyMD, adicione aqui ex: python3,kivy,kivymd
requirements = python3,kivy

# (str) Orientação da tela (portrait = em pé, landscape = deitado, all = todas)
orientation = portrait

# (int) Se o aplicativo deve rodar em tela cheia (1 = sim, 0 = não)
fullscreen = 0

#
# --- Configurações Específicas do Android -----------------------------
#

# (list) Permissões que o aplicativo precisa
# INTERNET é padrão se o app precisar carregar algo online
android.permissions = INTERNET

# (int) API alvo do Android (o Buildozer geralmente cuida disso sozinho se comentado)
# android.api = 31

# (int) API mínima suportada (Buildozer cuida disso se comentado)
# android.minapi = 21

# (str) Arquiteturas suportadas do Android (importante para rodar em celulares novos e antigos)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Permite backup do aplicativo no Android
android.allow_backup = True

#
# --- Configurações do Buildozer ---------------------------------------
#

[buildozer]

# (int) Nível de log (0 = erro apenas, 1 = info, 2 = debug com comandos inteiros)
log_level = 2

# (int) Mostrar aviso se executar como root (1 = sim, 0 = não)
warn_on_root = 1

name: Build Android App

on:
  push:
    branches:
      - main
      - master
  pull_request:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Instalar dependências do sistema
        run: |
          sudo apt-get update
          sudo apt-get install -y build-essential libltdl-dev libffi-dev libssl-dev python3-dev zip unzip
          pip install --upgrade pip
          pip install --upgrade buildozer cython virtualenv

      - name: Compilar o APK com Buildozer
        uses: ArtemSBulgakov/buildozer-action@v2
        id: buildozer
        with:
          command: buildozer android debug
          buildozer_version: master

      - name: Fazer upload do APK gerado
        uses: actions/upload-artifact@v4
        with:
          name: meu-aplicativo-apk
          path: bin/*.apk

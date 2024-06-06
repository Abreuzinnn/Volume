#!/bin/bash


# Instala as dependências necessárias
pip install git+https://github.com/jleb/pyaudio.git

# Instala os pacotes Python
pip install -r requirements.txt

# Executa o script Python
python Alerta.py

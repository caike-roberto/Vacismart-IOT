"""
Gateway do VaciSmart (IoT).

O Arduino so escreve a temperatura na serial, ele nao fala HTTP.
Este script le essas leituras e monta o JSON combinado com o time Java.

Dois modos:
  - sem API_URL definida: so imprime o JSON na tela (modo teste)
  - com API_URL definida: faz POST pra API Java com o token do dispositivo

Uso:
  python gateway.py leituras.txt
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
TRANSPORTE_ID = os.getenv("TRANSPORTE_ID", "00000000-0000-4000-8000-000000000001")
DISPOSITIVO_ID = "ARDUINO-DEMO-01"
PAUSA_S = float(os.getenv("PAUSA_S", "1"))

FUSO = timezone(timedelta(hours=-3))  # America/Sao_Paulo


def montar_leitura(temperatura):
    return {
        "transporteId": TRANSPORTE_ID,
        "dispositivoId": DISPOSITIVO_ID,
        "temperaturaC": temperatura,
        "medidaEm": datetime.now(FUSO).isoformat(timespec="seconds"),
    }


def enviar(dados):
    resp = requests.post(
        API_URL,
        json=dados,
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        timeout=10,
    )
    print(f"{dados['temperaturaC']} C -> HTTP {resp.status_code}")


def main():
    arquivo = sys.argv[1] if len(sys.argv) > 1 else "leituras.txt"

    with open(arquivo, encoding="utf-8") as f:
        for linha in f:
            texto = linha.strip()
            if not texto or texto.startswith("#"):
                continue

            if texto == "ERRO_SENSOR":
                print("sensor sem resposta, leitura descartada")
                continue

            try:
                temperatura = float(texto)
            except ValueError:
                print(f"linha ignorada: {texto!r}")
                continue

            dados = montar_leitura(temperatura)

            if API_URL:
                try:
                    enviar(dados)
                except requests.RequestException as erro:
                    print(f"falha ao enviar: {erro}")
            else:
                print(json.dumps(dados, ensure_ascii=False))

            time.sleep(PAUSA_S)


if __name__ == "__main__":
    main()

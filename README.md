# Lab1-criptografia
Este repositorio contiene el desarrollo del **Laboratorio 1** de la asignatura Seguridad en Redes.  
El objetivo principal es implementar técnicas básicas de ocultamiento de información en tráfico ICMP, 
junto con el posterior descifrado mediante ataque de fuerza bruta.

## Contenido

- **Códigos**
  - `cesar.py`: Implementación del cifrado y descifrado César.
  - `pingv4.py`: Generación de paquetes ICMP con inserción de texto cifrado en el payload.
  - `readv4.py`: Script para extraer mensajes de un archivo `.pcap` y descifrarlos mediante ataque de fuerza bruta con prueba de chi-cuadrado.

- **Capturas**
  Carpeta con las imágenes de ejecuciones y resultados en Wireshark.

## Requisitos

- Python 3.x  
- Librerías necesarias:  
  - `scapy` (para construcción y análisis de paquetes)  
  - Librerías estándar de Python (`string`, `math`, etc.)

Instalación de dependencias:
pip install scapy
## ejecucion
Ejecución

-Cifrado César

cesar.py <texto> <desplazamiento>

Envío de ICMP con payload cifrado

sudo python pingv4.py <IP(usado para la tarea 8.8.8.8)> <mensaje>


Descifrado de mensajes (MITM)

python readv4.py <archivo.pcap>

# cesar.py
import sys

def cifrado_cesar(texto, desplazamiento):
    texto = texto.upper()  # Convertir a mayúsculas
    resultado = ""
    for caracter in texto:
        if 'A' <= caracter <= 'Z':  # Solo letras
            codigo = ord(caracter)
            nuevo_codigo = ((codigo - 65 + desplazamiento) % 26) + 65
            resultado += chr(nuevo_codigo)
        else:
            resultado += caracter  # Mantener números y espacios
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py <texto> <desplazamiento>")
        sys.exit(1)

    texto = sys.argv[1]
    desplazamiento = int(sys.argv[2])
    cifrado = cifrado_cesar(texto, desplazamiento)
    print(cifrado)

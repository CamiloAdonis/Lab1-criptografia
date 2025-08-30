# mitm_decoder.py (versión final ordenada con desplazamientos 0-25)
import sys
from scapy.all import rdpcap, ICMP

FREQ_ES = {
    'A':12.53,'B':1.42,'C':4.68,'D':5.86,'E':13.68,'F':0.69,'G':1.01,'H':0.70,
    'I':6.25,'J':0.44,'K':0.01,'L':4.97,'M':3.15,'N':6.71,'O':8.68,'P':2.51,
    'Q':0.88,'R':6.87,'S':7.98,'T':4.63,'U':3.93,'V':0.90,'W':0.01,'X':0.22,
    'Y':0.90,'Z':0.52
}
GREEN, RESET = "\033[92m", "\033[0m"
OFFSET = 0x10

def descifrado_cesar(texto, k):
    out = []
    for ch in texto:
        if 'A' <= ch <= 'Z':
            c = ord(ch) - 65
            out.append(chr(((c - k) % 26) + 65))
        elif ch == ' ':
            out.append(' ')
        else:
            out.append(ch)
    return ''.join(out)

def chi_cuadrado_score(texto):
    counts = {c:0 for c in FREQ_ES}
    total = 0
    for ch in texto:
        if 'A' <= ch <= 'Z':
            counts[ch] += 1
            total += 1
    if total == 0:
        return float('inf')
    score = 0.0
    for c in FREQ_ES:
        exp = FREQ_ES[c] * total / 100.0
        if exp > 0:
            obs = counts[c]
            score += (obs - exp) ** 2 / exp
    return score

def extraer_mensaje_desde_pcap(pcap_path):
    chars = []
    paquetes = rdpcap(pcap_path)
    for p in paquetes:
        if p.haslayer(ICMP) and p[ICMP].type == 8:
            data = bytes(p[ICMP].payload)
            if len(data) > OFFSET:
                b = data[OFFSET]
                ch = chr(b)
                if ('A' <= ch <= 'Z') or ch == ' ' or ch == 'b':
                    chars.append(ch)
    if chars and chars[-1] == 'b':  # eliminar sentinel solo si es minúscula
        chars.pop()
    return ''.join((c.upper() if c != ' ' else ' ') for c in chars)

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 mitm_decoder.py <archivo.pcap>")
        sys.exit(1)

    pcap = sys.argv[1]
    cifrado = extraer_mensaje_desde_pcap(pcap)
    if not cifrado:
        print("❌ No se pudo extraer mensaje del PCAP")
        sys.exit(1)

    print("🔒 Mensaje cifrado extraído:", cifrado)
    print("\n🔓 Posibles descifrados (desplazamientos 0–25):")
    print("=" * 70)

    resultados = []
    for k in range(26):
        texto = descifrado_cesar(cifrado, k)
        score = chi_cuadrado_score(texto)
        resultados.append((score, k, texto))

    # elegir mejor
    mejor_score, mejor_k, mejor_texto = min(resultados, key=lambda x: x[0])

    # imprimir ordenado por desplazamiento (0-25)
    for score, k, texto in sorted(resultados, key=lambda x: x[1]):
        if k == mejor_k:
            print(f"{GREEN}Desplazamiento {k:2d}: {texto}{RESET}")
        else:
            print(f"Desplazamiento {k:2d}: {texto}")

    print("=" * 70)
    print(f"\n🎯 {GREEN}MENSAJE MÁS PROBABLE:{RESET} {mejor_texto}")
    print(f"   Desplazamiento usado: {mejor_k}")

if __name__ == "__main__":
    main()

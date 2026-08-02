import socket
import argparse
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111,
    135, 139, 143, 443, 445, 993, 995,
    1433, 1521, 3306, 3389, 5432,
    5900, 6379, 8080
]

# Sondas simples para servicios que no envían banner espontáneamente
PROBES = {
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    8080: b"HEAD / HTTP/1.0\r\n\r\n",
    443: b"",  # HTTPS requeriría TLS; se deja vacío a propósito
}

VERSION = "001"

BANNER = r"""
   ___            _     _____                                 
  / _ \___  _ __ | |_  /  ___|  ___ __ _ _ __  _ __   ___ _ __ 
 / /_)/ _ \| '__|| __| \ `--. / __/ _` | '_ \| '_ \ / _ \ '__|
/ ___/ (_) | |   | |_   `--. \ (_| (_| | | | | | | |  __/ |   
\/    \___/|_|    \__| /\__/ /\___\__,_|_| |_|_| |_|\___|_|   

"""


def print_banner():
    print(BANNER)
    print(f"    Escaner de puertos TCP con banner grabbing")
    print(f"    " + "-" * 45 + "\n")


print_lock = threading.Lock()
results = []
results_lock = threading.Lock()


def parse_ports(ports_arg):
    """Convierte '1-1000' o '22,80,443' o None en una lista de puertos."""
    if not ports_arg:
        return COMMON_PORTS

    ports = set()
    for part in ports_arg.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def scan_port(host, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))

        if result == 0:
            banner = "Sin banner"
            try:
                probe = PROBES.get(port)
                if probe:
                    sock.send(probe)
                data = sock.recv(1024)
                if data:
                    banner = data.decode(errors="ignore").strip()
            except (socket.timeout, OSError):
                pass

            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Desconocido"

            with results_lock:
                results.append({
                    "port": port,
                    "service": service,
                    "banner": banner
                })

            with print_lock:
                print(f"[+] Puerto {port} abierto")
                print(f"    Servicio : {service}")
                print(f"    Banner   : {banner}\n")

        sock.close()
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Escáner de puertos y banners"
    )
    parser.add_argument(
        "host",
        help="IP o dominio objetivo"
    )
    parser.add_argument(
        "--ports",
        help="Puertos a escanear, ej: '22,80,443' o '1-1000'. Por defecto usa una lista de puertos comunes.",
        default=None
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout de conexión en segundos (default: 1.0)"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=50,
        help="Cantidad de threads concurrentes (default: 50)"
    )
    parser.add_argument(
        "--output",
        help="Ruta de archivo para exportar resultados (JSON o CSV según extensión)",
        default=None
    )

    args = parser.parse_args()

    # Resolver el host antes de arrancar, para dar un error claro
    try:
        resolved_ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"[!] No se pudo resolver el host: {args.host}")
        return

    ports = parse_ports(args.ports)

    print(f"\nEscaneando {args.host} ({resolved_ip}) — {len(ports)} puertos, "
          f"{args.threads} threads, timeout {args.timeout}s\n")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(scan_port, args.host, port, args.timeout)
            for port in ports
        ]
        for _ in as_completed(futures):
            pass

    elapsed = time.time() - start_time
    results.sort(key=lambda r: r["port"])

    print(f"--- Resumen ---")
    print(f"Puertos abiertos : {len(results)}")
    print(f"Tiempo total     : {elapsed:.2f}s\n")

    if args.output:
        if args.output.endswith(".csv"):
            import csv
            with open(args.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["port", "service", "banner"])
                writer.writeheader()
                writer.writerows(results)
        else:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Resultados exportados a {args.output}")


if __name__ == "__main__":
    main()
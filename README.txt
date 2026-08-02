```
  __   __  _                       _                                   
 /  \ /  \/ |  ___   _ __  ___ _ _| |_   ___ __ __ _ _ _  _ _  ___ _ _ 
| () | () | | |___| | '_ \/ _ \ '_|  _| (_-</ _/ _` | ' \| ' \/ -_) '_|
 \__/ \__/|_|       | .__/\___/_|  \__|_/__/\__\__,_|_||_|_||_\___|_|  
                    |_|              |___|                             
```

Escáner de puertos TCP concurrente con detección de banners y servicios, escrito en Python.

## Características

- Escaneo concurrente con threads (velocidad configurable)
- Detección de banners de los servicios expuestos
- Identificación del servicio asociado a cada puerto
- Puertos configurables: lista fija de puertos comunes, lista personalizada o rango
- Export de resultados a JSON o CSV
- Resumen final con cantidad de puertos abiertos y tiempo total de escaneo

## Instalación

No requiere dependencias externas, solo Python 3.

```bash
git clone https://github.com/BenjaCliminio/Port_scanner.git
pip install tqdm
cd Port_scanner
```

## Uso

```bash
python port_scanner.py <host> [opciones]
```

### Opciones

| Flag         | Descripción                                                  | Default                    |
|--------------|---------------------------------------------------------------|-----------------------------|
| `--ports`    | Puertos a escanear (ej: `22,80,443` o `1-1000`)               | Lista de puertos comunes    |
| `--timeout`  | Timeout de conexión en segundos                               | 1.0                          |
| `--threads`  | Cantidad de threads concurrentes                               | 50                           |
| `--output`   | Archivo de salida (`.json` o `.csv`)                           | -                            |

### Ejemplos

Escaneo básico con puertos comunes:
```bash
python port_scanner.py 127.0.0.1
```

Escaneo de un rango de puertos con más threads:
```bash
python port_scanner.py 192.168.1.10 --ports 1-1000 --threads 100
```

Escaneo con timeout ajustado y export a JSON:
```bash
python port_scanner.py 192.168.1.10 --ports 1-1000 --timeout 0.5 --output resultado.json
```

Export a CSV con puertos específicos:
```bash
python port_scanner.py scanme.nmap.org --ports 22,80,443 --output resultado.csv
```

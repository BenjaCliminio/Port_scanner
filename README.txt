# Port Scanner

Escáner de puertos TCP con detección de banners, escrito en Python.

## Características
- Escaneo concurrente con threads
- Detección de banners y servicios
- Puertos configurables (lista o rango)
- Export de resultados a JSON/CSV

## Uso

```bash
python port_scanner.py <host> [opciones]
```

### Opciones
| Flag | Descripción | Default |
|------|-------------|---------|
| `--ports` | Puertos a escanear (ej: `22,80,443` o `1-1000`) | Lista de puertos comunes |
| `--timeout` | Timeout de conexión en segundos | 1.0 |
| `--threads` | Cantidad de threads concurrentes | 50 |
| `--output` | Archivo de salida (`.json` o `.csv`) | - |

### Ejemplo
```bash
python port_scanner.py 192.168.1.10 --ports 1-1000 --threads 100 --output resultado.json
```

#  Descripción
-** Este proyecto es un descargador de música de YouTube que permite a los usuarios obtener canciones de manera rápida y sencilla. A través de una página web intuitiva, los usuarios pueden ingresar enlaces de videos y descargar el audio en el formato deseado. El sistema está diseñado para ofrecer dos métodos de descarga: uno secuencial y otro en paralelo, brindando flexibilidad y eficiencia según las necesidades del usuario.

Para su desarrollo, se utilizaron diversas tecnologías. Django gestiona el servidor y las solicitudes de descarga, mientras que Bootstrap se empleó para crear una interfaz atractiva y fácil de usar. La lógica del programa fue implementada en Python, utilizando herramientas como yt-dlp para descargar y convertir los videos en archivos de audio. Además, se desarrollaron dos versiones del programa:

La rama master, que ejecuta las descargas en paralelo utilizando librerías como threading y multiprocessing, optimizando el tiempo y los recursos.
La rama características, programación secuencial, que realiza las descargas de manera secuencial, procesando un archivo a la vez.
Estas dos versiones permiten al usuario elegir entre eficiencia máxima o un enfoque más sencillo, según sus necesidades.**



# Downloader project

## Desarrolladores
- **Jesus Alejandro Be Hau**
- **Roger Jesus Aguilar Uicab**
- **Miguel Angel Gomez Herguera**

---
## Requerimientos previos
Es necesario instalar python y django

---
## Levantar el proyecto

Clonar el proyecto

```bash
  git clone https://github.com/JABEHAU/DownloaderProject
```

Ir al directorio raiz del proyecto

```bash
  cd DownloaderProject
```

Lanzar el proyecto

```bash
  python manage.py runserver
```

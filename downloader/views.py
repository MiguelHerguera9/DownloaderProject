from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import os
from yt_dlp import YoutubeDL
import threading
import time

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def process_urls(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            urls = data.get('urls', [])

            if not urls or not all(isinstance(url, str) for url in urls):
                return JsonResponse({'success': False, 'error': 'Formato de URLs inválido.'}, status=400)

            user_downloads_folder = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
            if not os.path.exists(user_downloads_folder):
                return JsonResponse({'success': False, 'error': 'No se encontró la carpeta de descargas del usuario.'}, status=400)

            download_files = []
            errors = []
            threads = []

            def download_url(url):
                """Descarga una URL específica utilizando YoutubeDL."""
                try:
                    # Opciones específicas por hilo
                    ydl_opts = {
                        'ffmpeg_location': 'C:\\ffmpeg\\bin',
                        'noplaylist': True,
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(user_downloads_folder, '%(id)s_%(title)s.%(ext)s'),
                        'postprocessors': [
                            {
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }
                        ],
                    }
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        file_path = os.path.join(user_downloads_folder, f"{info['id']}_{info['title']}.mp3")

                        download_time = time.time()
                        os.utime(file_path, (download_time, download_time))

                        download_files.append(file_path)

                except Exception as e:
                    errors.append({'url': url, 'error': str(e)})

            for url in urls:
                thread = threading.Thread(target=download_url, args=(url,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            return JsonResponse({'success': True, 'message': 'Todas las descargas fueron exitosas.', 'files': download_files})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Error al procesar el cuerpo de la solicitud.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

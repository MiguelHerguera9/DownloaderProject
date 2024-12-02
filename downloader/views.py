from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import os
from yt_dlp import YoutubeDL
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
            
            ydl_opts = {
                'ffmpeg_location': 'C:\\ffmpeg\\bin',
                'noplaylist': True,
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(user_downloads_folder, '%(title)s.%(ext)s'),
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],
            }

            download_files = []

            with YoutubeDL(ydl_opts) as ydl:
                for url in urls:
                    info = ydl.extract_info(url, download=True)
                    file_path = os.path.join(user_downloads_folder, f"{info['title']}.mp3")

                    download_time = time.time()
                    os.utime (file_path, (download_time, download_time))

                    download_files.append(f"{info['title']}.mp3")


            return JsonResponse({'success': True, 'message': 'Descarga exitosa, los archivos se guardaron en la carpeta de descargas..', 'files': download_files})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Ha ocurrido un error al descargar los archivos.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse
import hashlib
import boto3
from urllib.parse import urljoin
from .models import File
import requests
from .forms import UploadFileForm


def get_file(request: HttpRequest, file_hash: str):
    files = File.objects.filter(hash=file_hash)
    if not files.exists():
        return HttpResponse('expired')
    link = files.first().link
    file_content = requests.get(link).content

    response = HttpResponse(file_content, content_type='application/octet-stream')
    file_name = link.split("/")[-1]
    print(file_name)
    response['Content-Disposition'] = f'inline; filename="{file_name}"'

    return response


def index(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'index.html', {'form': UploadFileForm()})
    
    form = UploadFileForm(request.POST, request.FILES)
    print(form.is_valid())
    file = request.FILES['file']
    file_name = file.name
    file_content = file.read()
    file_hash = hashlib.md5(file_content).hexdigest()
    file_link = f'http://storage.yandexcloud.net/buckettan/{file_hash}{file_name}'

    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    print(file_content[:20], len(file_content), file_name)

    s3.put_object(Bucket='buckettan', Key=f'{file_hash}{file_name}', Body=file_content, StorageClass='COLD')

    uploaded = File(hash=file_hash, link=file_link)
    uploaded.save()
    
    return render(request, 'link.html', {'link': reverse("myapp:get-file", args=[file_hash])})

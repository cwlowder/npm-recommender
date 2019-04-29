from django.shortcuts import render

# Create your views here.
def simple_upload(request):
    if request.method == 'POST' and request.FILES['package']:
        package = request.FILES['package']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')
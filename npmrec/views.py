from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO handle form
            print(form)
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload_package.html', {'form': form})
import os
from wsgiref.util import FileWrapper

from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage

from .forms import FileForm
from .models import File

AVAILABLE_SPACE = 10
def get_space_available(request_user):
    folder_path = f'uploads/user_{request_user.pk}'
    total_size = 0
    _, filenames = default_storage.listdir(folder_path)
    for f in filenames:
        fp = os.path.join(folder_path, f)
        total_size += default_storage.size(fp)

    return round(total_size / (1024 * 1024),6)

class FileListView(LoginRequiredMixin,ListView):
    context_object_name = 'file_list'
    template_name = 'storage_drive/file/list.html'
    queryset = File.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = File.objects.filter(owner_id = self.request.user.id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'storage_drive'
        context['file_list_count'] = self.queryset.count()
        context['form'] = FileForm()
        queryset = File.objects.filter(owner_id = self.request.user.id).order_by('-updated_at')[:10]
        context['recent_files'] = queryset
        context['available_space'] = AVAILABLE_SPACE
        context['used_space'] = get_space_available(self.request.user)
        context['used_space_percent'] = context['used_space'] *100 / AVAILABLE_SPACE
        return context
    
class FileDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        file = File.objects.filter(pk=pk).first()
        filename = file.file.path
        wrapper = FileWrapper(file.file)
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % file.name
        response['Content-Length'] = os.path.getsize(filename)
        return response
    
@login_required()
def file_create(request):
    if request.method == 'POST':
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            space_used = get_space_available(request.user)
            if space_used > AVAILABLE_SPACE:
                return HttpResponse("Space is used completely.", status=403)
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            return JsonResponse({'success': True})
        return render(request, 'dashboard/tables/form_base.html', {'form': form},status=422)
    else:
        form = FileForm()
    return render(request, 'dashboard/tables/form_base.html', {'form': form},)

@login_required
def file_delete(request):
    file_ids = request.POST.getlist('ids[]',[])
    try:
        files = File.objects.filter(id__in = file_ids, owner = request.user)
        if not files:
            raise PermissionDenied("You do not have permission to delete these files.")
        for file in files:
            file_path = file.file.path
            if os.path.isfile(file_path):
                os.remove(file_path)
            file.delete()
        return JsonResponse({'message': 'Files deleted successfully.','success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

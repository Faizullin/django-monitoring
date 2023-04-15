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
from .models import File, get_space_available, AVAILABLE_SPACE
from dashboard.models import CustomUser
from dashboard.context_processors import default_context



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
        context.update(default_context())

        used_space = get_space_available(self.request.user)

        context.update({
            "form": FileForm(),
            'file_list_count': self.queryset.count(),
            'segment': 'storage_drive',
            'recent_files': File.objects.filter(owner_id = self.request.user.id).order_by('-updated_at')[:10],
            'available_space': AVAILABLE_SPACE,
            'used_space': used_space,
            'used_space_percent': used_space *100 / AVAILABLE_SPACE,
        })
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
            file_size_mb = form.cleaned_data['file'].size / (1024*1024)
            space_used = get_space_available(request.user)
            if space_used + file_size_mb > AVAILABLE_SPACE:
                return HttpResponse("Space is used completely.", status=403)
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            user = CustomUser.objects.get(id = request.user.pk)
            user.used_space = round(space_used + file_size_mb, 4)
            user.save()
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
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
            file.delete()
        return JsonResponse({'message': 'Files deleted successfully.','success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

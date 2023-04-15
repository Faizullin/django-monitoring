from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from dashboard.context_processors import default_context
from dashboard.models import CustomUser
from .forms import *
import django_filters
from django_filters.views import FilterView 
import django_tables2 as tables

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','email',]

class UserTable(tables.Table):
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                    '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:user_edit\' pk=record.pk %}">Edit</a>'
                    '<a class="">'
                    '<form method="post" action="{% url \'dashboard:user_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = CustomUser
        fields = ("id","username", "email", "address", "age","used_space", "date_joined" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }

class UserListView(LoginRequiredMixin, tables.SingleTableMixin, FilterView):
    model = CustomUser
    table_class = UserTable
    template_name = 'dashboard/tables/user/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = UserFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = super().get_context_data()
        context.update(default_context())
        context.update({
            "form": UserForm(),
            'segment': 'user_index'
        })
        return context
    
    def get_queryset(self, *args, **kwargs):
        users = CustomUser.objects.all()
        return users

@login_required()
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = UserForm()
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = UserForm(instance=user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:user_edit', kwargs={'pk': user.pk}) })



@login_required
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('dashboard:user_index')
    raise Http404








# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import JsonResponse, Http404
# from django.shortcuts import render, get_object_or_404, redirect
# from django.utils.html import format_html
# from django.urls import reverse
# import django_tables2 as tables
# import django_filters
# from django_filters.views import FilterView 


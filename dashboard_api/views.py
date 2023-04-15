from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
from rest_framework import status, permissions,generics, filters
from rest_framework.response import Response
import psutil, time
from .serializers import UserSerializer, SystemDataSerializer
from dashboard.models import *
from storage_drive.models import get_space_available, AVAILABLE_SPACE

def getStatData():
    # load_avg = psutil.getloadavg()
    # pids = psutil.pids()
    lastSystemData =  SystemData.objects.last()
    context = {
        'data': {}
    }
    context['data']['user_acts'] = {
        #'timestamp': [ user.date_joined for user in user_acts ],
        'login': CustomUser.objects.filter(last_login__isnull=False).count(),
        'register': CustomUser.objects.count(),
    }
    context['data']['new_users'] = UserSerializer(CustomUser.objects.order_by('-id')[:10], many = True).data
    context['data']["cpu_times"] = psutil.cpu_times()
    context['data']["cpu_freq"] = psutil.cpu_freq()
    context['data']["cpu_stats"] = psutil.cpu_stats()
    context['data']["load_avg"] = random.randint(20,27) #psutil.getloadavg()
    context['data']["disk_io_counters"] = psutil.disk_io_counters()
    net_io_counters = psutil.net_io_counters()
    context['data']["net_io_counters"] = {
        'sent': net_io_counters.bytes_sent,
        'received': net_io_counters.bytes_recv
    }
    context['data']['system_data'] = SystemDataSerializer(lastSystemData).data

    #context['data']['processes'] = ProcessInfo.get_all_processes()
    processes = []
    for proc in psutil.process_iter():
        try:
            if proc.name() != 'systemd':
                pinfo = proc.as_dict(attrs=['pid', 'name','status','cpu_percent','memory_info'])
                processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    context['data']['processes'] = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:10]
    return context

class ApiServerData(APIView):
    # authentication_classes = [JWTAuthentication, ]
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        context = getStatData()
        return Response(data = context)
    

started = False
MAX_SAVE_NUMBER = 20
import random
def save_system_data():
    global MAX_SAVE_NUMBER
    global started
    print("Start save_system_data")  
    while True:
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        cpu_temp = float(random.randint(40,60))
        timestamp = int(time.time())
 
        system_data = SystemData(cpu_percent=cpu_percent, mem_percent=mem_percent, disk_percent=disk_percent, timestamp=timestamp, cpu_temp=cpu_temp)
        system_data.save()
        current_count = SystemData.objects.count()
        
        if current_count > MAX_SAVE_NUMBER:
            first_n_records = SystemData.objects.order_by('id').filter(id__lt = (system_data.pk - MAX_SAVE_NUMBER))
            first_n_records.delete()

         
        time.sleep(7)

def save_user_storage_drive():
    global MAX_SAVE_NUMBER
    global started
    print("Start save_user_storage_drive")  
    while True:
        users = CustomUser.objects.all()
        for user in users:
            used_space_by_user = get_space_available(user)
            user.used_space = round(used_space_by_user,4)
            user.save()
        
        time.sleep(14)

from threading import Thread
def apiStartRecord(request):
    global started
    if started:
        return JsonResponse({"data":"Already started!"})
    elif not started:
        started = True
        t1 = Thread(target=save_system_data, daemon=True)
        t2 = Thread(target=save_user_storage_drive, daemon=True)

        t1.start()
        t2.start()  
        return JsonResponse({"data":"Starting"})
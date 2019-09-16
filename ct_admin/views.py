from django.shortcuts import render

# Create your views here.

def Home(request):
    return render(request, 'ct_admin/ct_admin.html')
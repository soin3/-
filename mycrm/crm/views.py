from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')


def customers_list(request):
    return render(request,"sales/customers.html")

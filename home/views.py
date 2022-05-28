from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index1.html')
def faq(request):
    return render(request,'faq button.html')
def our_team(request):
    return render(request, 'our team.html')
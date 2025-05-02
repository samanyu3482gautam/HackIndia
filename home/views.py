from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def profile(request):
    return render(request,'profile.html')


def feedback_form(request):
  
    
    return render(request,'home/feedback_form.html')
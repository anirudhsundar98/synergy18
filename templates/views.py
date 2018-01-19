from django.shortcuts import render

# Views

def homepage(request):
	return render(request, 'homepage.html')
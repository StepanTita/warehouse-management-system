from django.shortcuts import render
from .forms import NewCargoForm


# Create your views here.
def index(request):
    return render(request, 'controller/index.html')


def new_cargo(request):
    if request.method == "POST":
        pass
    else:
        form = NewCargoForm()
        return render(request, 'new_cargo/new_cargo.html', {'form': form})

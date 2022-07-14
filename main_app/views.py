from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Import the FeedingForm
from .forms import FeedingForm



def home(request):
    return HttpResponse('<a href = "/about"><h1>Hello World /ᐠ｡‸｡ᐟ\ﾉ</h1></a>')

def about(request):
    return render(request,'about.html')

# Add new view
def cats_index(request):
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', {'cats': cats })

def add_feeding(request, cat_id):
  # create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it 
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)

def cats_detail(request, cat_id):
  ## Get the the individual cat
  cat = Cat.objects.get(id=cat_id)
  feeding_form = FeedingForm()
  ## render template, pass it the cat
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form })

class CatCreate(CreateView):
  model = Cat
  fields = '__all__'
  success_url = '/cats/'
  
class CatUpdate(UpdateView):
    model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

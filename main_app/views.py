from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Cat, Toy, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3



from .forms import FeedingForm

# Add these "constants" below the imports
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'mycatcollector'



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
  # Get the toys the cat doesn't have
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  ## render template, pass it the cat
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have })

def assoc_toy(request, cat_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect ('detail', cat_id=cat_id)

def add_photo(request, cat_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, cat_id=cat_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', cat_id=cat_id)
  
   

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

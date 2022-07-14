from datetime import date
from django.db import models
from django.urls import reverse



# Create your models here.

class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('toys_detail', kwargs={'pk': self.id})


class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})
    
    def fed_for_today(self):
        return self.feeding_set.filter(date = date.today()).count() >= len(MEALS)
    
    
    
MEALS = (
('B', 'Breakfast'),
('L', 'Lunch'),
('D', 'Dinner')
)
class Feeding(models.Model):
    date = models.DateField('Feeding date')
    meal = models.CharField('Meal',
        max_length=1,  
        choices=MEALS, # add the 'choices' field option
        default=MEALS[0][0] # set the default value for meal to be 'B'
        ) 
    # Create a cat_id FK
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    
    def __str__(self):
        # get_x_display() is a function in django 
        return f"{self.get_meal_display()} on {self.date}"
  
    # change the default sort   
    class Meta:
        ordering = ['-date', 'meal']
    
    
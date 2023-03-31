from django.db import models

class Cards(models.Model):
    name = models.CharField(max_length=100,help_text="Character Names")
    picture = models.TextField(help_text="Character Images")
    
    def __str__(self):
        return self.name

# python3 manage.py makemigrations {name of app}
# python3 manage.py migrate -> migration 

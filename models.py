from django.db import models

class InsertTemplate(models.Model):
    template_title = models.CharField("template title")
    template_filename = models.CharField("template file name")

    def __str__(self):
        return self.template_title
    
    

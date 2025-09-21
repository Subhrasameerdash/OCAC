from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=40)       # column: name (varchar(40))
    email = models.EmailField(max_length=40)     # column: email (varchar, validated as email)
    subject = models.CharField(max_length=40)
    content = models.TextField(max_length=400)   # column: content (text)

    def _str_(self):
        return f"{self.name} | {self.email} | {self.subject}"
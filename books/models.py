from django.db import models

class Book(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, default="ar")  # زبان کتاب
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=255)
    number = models.PositiveIntegerField()  
    juz = models.PositiveIntegerField(null=True, blank=True) 

    def __str__(self):
        return f"{self.book.title} - {self.title}"


class Verse(models.Model):

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="verses")
    number = models.PositiveIntegerField()  
    text = models.TextField() 
    translation = models.TextField(blank=True) 

    class Meta:
        unique_together = ('chapter', 'number') 

    def __str__(self):
        return f"{self.chapter.title} - {self.number}"

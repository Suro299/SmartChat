from django.db import models

class Film(models.Model):
    title = models.CharField("Title", max_length = 255, unique = True)
    img = models.URLField("Url", max_length = 255)
    year = models.PositiveIntegerField("Year")
    genre = models.CharField("Genre", max_length = 255)
    href = models.URLField("Href", max_length = 255)
    
    class Meta:
        verbose_name = "Sponsor Film"
        verbose_name_plural = "Sponsor Films"
        
        
    def __str__(self) -> str:
        return f"{self.title} | {self.year} | {self.genre}"
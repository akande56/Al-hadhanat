from django.db import models

# Create your models here.


class QA(models.Model):
    """Model definition for QA."""

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.CharField(max_length=100)

    class Meta:
        """Meta definition for QA."""

        verbose_name = "QA"
        verbose_name_plural = "QAs"

    def __str__(self):
        """Unicode representation of QA."""
        return str(self.name)

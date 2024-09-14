from django.db import models
from django.contrib.auth.hashers import make_password


from django.contrib.auth.models import AbstractUser
from django.db import models

class Medewerker(AbstractUser):
    # Voeg extra velden toe die je nodig hebt
    voornaam = models.CharField(max_length=255)
    achternaam = models.CharField(max_length=100)
    gebruikersnaam = models.CharField(max_length=255, unique=True, default='')
    emailadres = models.EmailField(max_length=255, unique=True)
    postcode = models.CharField(max_length=6)
    huisnummer = models.IntegerField()
    geslacht = models.CharField(max_length=10)
    telefoonnummer = models.CharField(max_length=15)
    geboortedatum = models.DateField()
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medewerkers'


class Ervaringsdeskundige(models.Model):
    deskundige_id = models.AutoField(primary_key=True)
    voornaam = models.CharField(max_length=255, blank=True, null=True)
    achternaam = models.CharField(max_length=255, blank=True, null=True)
    wachtwoord = models.CharField(max_length=255, blank=True, null=True)
    geboortedatum = models.DateField(blank=True, null=True)
    telefoonnummer = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    geslacht = models.CharField(max_length=10, blank=True, null=True)
    postcode = models.CharField(max_length=6, blank=True, null=True)
    huisnummer = models.IntegerField(blank=True, null=True)
    soort_beperking = models.TextField(blank=True, null=True)
    hulpmiddelen = models.TextField(blank=True, null=True, default='null')
    bijzonderheden = models.TextField(blank=True, null=True, default='null')
    account_status = models.IntegerField(default=0)
    bericht_status = models.CharField(max_length=255, blank=True, null=True, default='null')
    naam_toezichthouder = models.CharField(max_length=255, blank=True, null=True, default='null')
    email_toezichthouder = models.CharField(max_length=255, blank=True, null=True, default='null')
    telefoonnummer_toezichthouder = models.CharField(max_length=255, blank=True, null=True, default='null')
    benadering_keuze = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    beperking = models.ForeignKey(
        'Beperking', on_delete=models.SET_NULL, blank=True, null=True
    )
    onderzoek = models.ForeignKey(
        'companies.Onderzoek', on_delete=models.SET_NULL, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.wachtwoord = make_password(self.wachtwoord)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'ervaringsdeskundigen'


class Beperking(models.Model):
    beperking_id = models.AutoField(primary_key=True)
    beperking = models.CharField(max_length=255)
    categorie = models.CharField(max_length=255)

    class Meta:
        db_table = 'beperkingen'

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def validate_seven_digits(value):
    if len(str(value)) != 7:
        raise ValidationError("This field needs exactly 7 digits.")
    
class Osauhing(models.Model):
    companyname = models.CharField(max_length=100, validators=[MinValueValidator(3)])
    registrycode = models.PositiveIntegerField(validators=[validate_seven_digits])
    foundingdate = models.DateField()
    totalcapital = models.PositiveIntegerField(validators=[MinValueValidator(2500)])
    shareholders = models.ManyToManyField('Shareholder', related_name='companies', blank=True)

class IndividualShareHolder(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    personal_id_code = models.PositiveIntegerField(unique=True)
    shareholder_share = models.PositiveIntegerField(validators=[MinValueValidator(1)])

class LegalEntityShareHolder(models.Model):
    full_name = models.CharField(max_length=70)
    registry_code = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    shareholder_share = models.PositiveIntegerField(validators=[MinValueValidator(1)])

class Shareholder(models.Model):
    individual = models.ForeignKey(IndividualShareHolder, null=True, blank=True, on_delete=models.CASCADE)
    legal_entity = models.ForeignKey(LegalEntityShareHolder, null=True, blank=True, on_delete=models.CASCADE)




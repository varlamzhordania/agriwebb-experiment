import os
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseModel(models.Model):
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
        blank=True,
        null=True
        )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
        blank=True,
        null=True
        )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} (ID: {self.id}, Active: {self.is_active})"


@deconstructible
class UploadPath:
    def __init__(self, folder, sub_path):
        self.folder = folder
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        # Use os.path.splitext to handle file extensions safely
        _, extension = os.path.splitext(filename)
        extension = extension.lstrip('.')  # Remove the leading dot if present
        return f"{self.folder}/{self.sub_path}/{timestamp}.{extension}"


class Record(models.Model):
    class RecordTypeChoices(models.TextChoices):
        AnimalTreatment = "animalTreatment", _("Animal Treatment")
        Feed = "feed", _("Feed")
        LocationChanged = "locationChanged", _("Location Changed")
        PregnancyScan = "pregnancyScan", _("Pregnancy Scan")
        Score = "score", _("Score")
        Weigh = "weigh", _("Weigh")

    record_id = models.IntegerField(
        verbose_name=_('Record ID'),
        primary_key=False,
        blank=True,
        null=True,
        help_text=_('Record ID on the agriwebb'),
    )
    record_type = models.CharField(
        max_length=20,
        verbose_name=_('Record Type'),
        choices=RecordTypeChoices.choices,
        blank=True,
        null=True,
        help_text=_('Record Type on the agriwebb'),
    )
    observation_date = models.DateTimeField(  # change to charField,it could be unix time
        verbose_name=_('Observation Date'),
        blank=True,
        null=True,
        help_text=_('Observation Date on the agriwebb'),
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name=_('Session ID'),
        blank=True,
        null=True,
        help_text=_('Session ID on the agriwebb'),
    )

    class Meta:
        abstract = True

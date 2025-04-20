from django.db import models
from django.utils.translation import gettext_lazy as _


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

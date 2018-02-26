from django.db import models
from django.forms import ModelForm

''' MODELS '''

class Activity(models.Model):
    name = models.TextField(
        blank=False,
    )
    description = models.TextField(
        blank=True,
        default=None,
    )

    class Meta:
        db_table = 'activity'

class Unit(models.Model):
    name = models.TextField(
        blank=False,
    )
    description = models.TextField(
        blank=True,
        default=None,
    )
    


class Metric(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
    )
    start = models.DateTimeField(
        blank=False,
        default=None,
        help_text="When the metric occurred or began.",
    )
    end = models.DateTimeField(
        blank=True,
        default=None,
        help_text=(
            "When provided, defines a duration of the metric by subtracting "
            "the <code>start</code> field."
        )
    )
    item = models.TextField(
        blank=True,
        help_text=(
            "The item associated with the metric; e.g. when eating, "
            "the user may write what was eaten."
        )
    )
    value = models.FloatField(
        blank=True,
        default=None,
        help_text=(
            "The recorded value for the metric event; e.g. when eating "
            "this could be how many calories were eaten."
        )
    )
    units = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        help_text=(
            "Units associated with the <code>value</code> field."
        )
    )
    alone = models.BooleanField(
        blank=False,
        default=True,
        help_text=(
            "Whether metric event occurred while being alone."
        )
    )
    notes = models.TextField(
        blank=True,
        help_text=(
            "Any extra notes associated with metric event."
        )
    )
    
    class Meta:
        db_table = 'metric'


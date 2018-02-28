from django.db import models

'''
Other models:
- medication
- sex
- bathroom
- exercise
- social time

- questionaires
'''

class Activity(models.Model):
    '''
    Defines the lsit of available metrics to record; is
    used to populate the select dropdown on the form
    that submits a metric.
    '''
    name = models.TextField(
        blank=False,
    )
    description = models.TextField(
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'activity'


class Eat(models.Model):
    '''
    Metric to log eating.

    The required fields for this model are:
        - start
        - alone

    '''
    start = models.DateTimeField(
        blank=False,
        help_text="When the metric event occurred or began.",
    )
    end = models.DateTimeField(
        blank=True,
        null=True,
        help_text=(
            "When provided, defines a duration of the metric event by"
            " subtracting the <code>Start</code> field."
        )
    )
    item = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Description of any item eaten."
        )
    )
    value = models.FloatField(
        blank=True,
        null=True,
        help_text=(
            "The recorded calories for the metric event."
        )
    )
    units = models.CharField(
        max_length=3,
        choices=[('cal','Cal')],
        blank=True,
        null=True,
        help_text=(
            "Units associated with the <code>Value</code> field."
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
        null=True,
        help_text=(
            "Any extra notes associated with metric event."
        )
    )
    
    class Meta:
        db_table = 'metric_eat'

class Drink(models.Model):
    '''
    Metric to log drinking.

    The required fields for this model are:
        - start
        - alone
        - item
        - has_caffeine

    '''
    start = models.DateTimeField(
        blank=False,
        help_text="When the metric occurred or began.",
    )
    item = models.CharField(
        max_length=9,
        choices=[
            ('water','Water'),
            ('tea','Tea'),
            ('coffee','Coffee'),
            ('alcohol','Alcohol'),
            ('soda','Soda')
        ],
        default='water',
        blank=False,
        help_text=(
            "The type of item drunk."
        )
    )
    value = models.FloatField(
        blank=True,
        null=True,
        help_text=(
            "The recorded volume for the metric event."
        )
    )
    units = models.CharField(
        max_length=9,
        choices=[('fl oz','Fluid Ounce')],
        blank=True,
        null=True,
        help_text=(
            "Units associated with the <code>Value</code> field."
        )
    )
    has_caffeine = models.BooleanField(
        blank=False,
        default=True,
        help_text=(
            "Whether the metric event contained caffeine."
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
        null=True,
        help_text=(
            "Any extra notes associated with metric event."
        )
    )

    class Meta:
        db_table = 'metric_drink'



class Sleep(models.Model):
    '''
    Metric to log eating.

    The required fields for this model are:
        - start
        - alone
        - end

    '''
    start = models.DateTimeField(
        blank=False,
        help_text="When the metric occurred or began.",
    )
    end = models.DateTimeField(
        blank=False,
        null=False,
        help_text=(
            "When provided, defines a duration of the metric by subtracting "
            "the <code>start</code> field."
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
        null=True,
        help_text=(
            "Any extra notes associated with metric event."
        )
    )

    class Meta:
        db_table = 'metric_sleep'

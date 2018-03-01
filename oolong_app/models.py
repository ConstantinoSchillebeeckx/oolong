from django.db import models
from django.conf import settings

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
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'activity'

class Metric(models.Model):
    '''
    Serves as the base model for all other metrics.

    The required fields for this model are:
        - start
    '''
    start = models.DateTimeField(
        blank=False,
        db_index=True,
        help_text="When the metric event occurred or began.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        default=None,
        db_index=True,
    )

    class Meta:
        abstract = True


class Eat(Metric):
    '''
    Metric to log eating.

    The required fields for this model are:
        - those of the base `Metric` model
        - alone

    '''
    end = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "When provided, defines a duration of the metric event by"
            " subtracting the <code>Start</code> field."
        )
    )
    item = models.TextField(
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "Description of any item eaten."
        )
    )
    value = models.FloatField(
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "The recorded calories for the metric event."
        )
    )
    units = models.CharField(
        max_length=3,
        choices=[('cal','Cal')],
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "Units associated with the <code>Value</code> field."
        )
    )
    alone = models.BooleanField(
        blank=False,
        default=True,
        db_index=True,
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

class Drink(Metric):
    '''
    Metric to log drinking.

    The required fields for this model are:
        - those of the base `Metric` model
        - alone
        - item
        - has_caffeine

    '''
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
        db_index=True,
        help_text=(
            "The type of item drunk."
        )
    )
    value = models.FloatField(
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "The recorded volume for the metric event."
        )
    )
    units = models.CharField(
        max_length=9,
        choices=[('fl oz','Fluid Ounce')],
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "Units associated with the <code>Value</code> field."
        )
    )
    has_caffeine = models.BooleanField(
        blank=False,
        default=True,
        db_index=True,
        help_text=(
            "Whether the metric event contained caffeine."
        )
    )
    alone = models.BooleanField(
        blank=False,
        default=True,
        db_index=True,
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



class Sleep(Metric):
    '''
    Metric to log eating.

    The required fields for this model are:
        - those of the base `Metric` model
        - alone
        - end

    '''
    end = models.DateTimeField(
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "When provided, defines a duration of the metric by subtracting "
            "the <code>start</code> field."
        )
    )
    alone = models.BooleanField(
        blank=False,
        default=True,
        db_index=True,
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




class Questionnaire(models.Model):
    '''
    Model that serves as a reference to define what questionnaires
    are available; e.g. GAD-7
    '''
    name = models.TextField(
        blank=False,
        null=False,
        unique=True,
        db_index=True,
    )
    description = models.TextField(
        null=True,
        unique=True,
    )
    form_header = models.TextField(
        null=True,
        help_text=(
            "Questionnaire form header help; e.g. 'Over the last 2 weeks, "
            "how often have you been bothered by the following problems?'"
        )
    )

    class Meta:
        db_table = 'questionnaire'



class Question(models.Model):
    '''
    Models that servers as a reference for all the questions available
    across the various questionnaires.
    '''
    question = models.TextField(
        blank=False,
        db_index=True,
        null=False,
        help_text=(
            "The text for the question."
        )
    )
    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.PROTECT,
        help_text=(
            "Which questionnaire the particular question is associated with."
        )
    )

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'question'
        unique_together = ('question','questionnaire')


class AvailableResponse(models.Model):
    '''
    Models that servers as a reference for all the available response types
    for a given questionnaire. A score & label combination cannot be associated
    with more than one questionnaire; it will simply be defined more than once.
    '''
    score = models.IntegerField(
        blank=False,
        db_index=True,
        null=False,
        help_text=(
            "Score for given response; e.g. 4."
        )
    )
    label = models.TextField(
        blank=False,
        db_index=True,
        null=False,
        help_text=(
            "Text label for given response; e.g. 'Several days'."
        )
    )
    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.PROTECT,
        help_text=(
            "Questionnaire for which response applies; e.g. GAD-7."
        )
    )

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'available_response'
        unique_together = [('label','questionnaire'),('score','questionnaire')]
    


class Response(models.Model):
    '''
    Model serves to record a users response to a given question on a given
    questionnaire.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        default=None,
        db_index=True,
    )
    date = models.DateField(
        blank=False,
        auto_now_add=True,
        db_index=True,
        help_text=(
            "Date on which question was answered."
        )
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        help_text=(
            "Question being answered/scored."
        )
    )   
    response = models.ForeignKey(
        AvailableResponse,
        on_delete=models.PROTECT,
        help_text=(
            "Response to given question."
        )
    )   

    class Meta:
        db_table = 'response'
        unique_together = ('user','date','question','response')






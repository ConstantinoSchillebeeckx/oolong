from django.db import models
from django.conf import settings


'''
                                -------------
                                METRIC MODELS
                                -------------
'''
class Activity(models.Model):
    '''
    Defines the list of available metrics to record; is
    used to populate the select dropdown on the form
    that submits a metric.
    '''
    name = models.TextField(
        blank=False,
        db_index=True,
    )
    icon = models.TextField(
        blank=False,
        db_index=True,
        help_text = "Name of font-awesome icon; e.g. `fa-beer`"
    )
    description = models.TextField(
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'activity'


class _Metric(models.Model):
    '''
    Serves as the base model for all other metrics.

    The required fields for this model are:
        - time_stamp
    '''
    time_stamp = models.DateTimeField(
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

class Note(_Metric):
    '''
    Generic note

    The required fields for this model are:
        - those of the base `Metric` model
        - nots
    '''
    notes = models.TextField(
        blank=False,
        null=False,
        help_text=(
            "Any extra notes associated with metric event."
        )
    )

class Medication(_Metric):
    '''
    Metric to log taking medication.

    The required fields for this model are:
        - those of the base `Metric` model
        - dose
        - medication
    '''
    medication = models.TextField(
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "Name of medication taken."
        )
    )
    dose = models.FloatField(
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "Dose of medication taken in mg."
        )
    )

    class Meta:
        db_table = 'metric_medication'
    
    
class Sex(_Metric):
    '''
    Metric to log sexual activity.

    The required fields for this model are:
        - those of the base `Metric` model
        - alone
    '''
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
        db_table = 'metric_sex'
    

class Bathroom(_Metric):
    '''
    Metric to log bathroom usage.

    The required fields for this model are:
        - those of the base `Metric` model
        - process
    '''
    process = models.CharField(
        max_length=1,
        choices=[
            ('1','Number 1'),
            ('2','Number 2'),
        ],
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "You know..."
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
        db_table = 'metric_bathroom'

class Exercise(_Metric):
    '''
    Metric to log exercise.

    The required fields for this model are:
        - those of the base `Metric` model
        - alone
        - type
    '''
    type = models.CharField(
        max_length=10,
        choices=[
            ('gym','Gym'),
            ('run','Run'),
            ('walk','Walk'),
        ],
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "The type of meal eaten."
        )
    )
    value = models.FloatField(
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "The recorded value for the type of exercise."
        )
    )
    units = models.CharField(
        max_length=10,
        choices=[
            ('steps','Steps'),
            ('miles','Miles'),
            ('km','Kilometers'),
        ],
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
        db_table = 'metric_exercise'

class Relax(_Metric):
    '''
    Metric to log relaxing time. This is meant as a type of catch
    all for activities like meditation, hanging out with friends,
    watching TV, etc.

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
            " subtracting the <code>Time stamp</code> field."
        )
    )
    type = models.CharField(
        max_length=15,
        choices=[
            ('read_book','Read book'),
            ('work','Work'),
            ('hobby','Hobby'),
            ('therapist','Therapist'),
            ('phone','Phone'),
            ('friends','Friends'),
            ('walk','Walk'),
            ('video_game','Video game'),
            ('meditation','Meditation'),
            ('walk','Walk'),
            ('internet','Internet'),
            ('other','Other'),
        ],
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "The type of relax/social event."
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
        db_table = 'metric_relax'

class Eat(_Metric):
    '''
    Metric to log eating.

    The required fields for this model are:
        - those of the base `Metric` model
        - alone
        - type
    '''
    end = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        help_text=(
            "When provided, defines a duration of the metric event by"
            " subtracting the <code>Time stamp</code> field."
        )
    )
    type = models.CharField(
        max_length=10,
        choices=[
            ('snack','Snack'),
            ('meal','Meal'),
        ],
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "The type of meal eaten."
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
        max_length=10,
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
    home_cooked = models.BooleanField(
        blank=False,
        default=True,
        db_index=True,
        help_text=(
            "Whether the meal was cooked at home."
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

class Drink(_Metric):
    '''
    Metric to log drinking.

    The required fields for this model are:
        - those of the base `Metric` model
        - alone
        - item
        - has_caffeine

    '''
    type = models.CharField(
        max_length=10,
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
        max_length=10,
        choices=[
            ('fl oz','Fluid Ounce'),
            ('ml','Milliliter'),
        ],
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



class Sleep(_Metric):
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
            "the <code>Time stamp</code> field."
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



'''
                    --------------------
                    QUESTIONNAIRE MODELS
                    --------------------
'''




class Questionnaire(models.Model):
    '''
    Model that serves as a reference to define what questionnaires
    are available; e.g. GAD-7.

    NOTE: it is assumed that the available answers for each question
    on a questionnaire are all the same.
    '''
    name = models.TextField(
        blank=False,
        null=False,
        primary_key=True,
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
    score = models.IntegerField(
        blank=False,
        null=False,
        db_index=True,
        help_text=(
            "Response score to given question."
        )
    )   

    class Meta:
        db_table = 'response'
        unique_together = ('user','date','question')






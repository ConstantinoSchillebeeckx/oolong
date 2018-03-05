import django_tables2 as tables

class _Generic(tables.Table):
    '''
    skeleton for the metric table; all the model specific fields will
    be passed by `extra_columns`
    '''

    id = tables.Column()
    time_stamp = tables.Column()

    class Meta:
        exclude=('user',)
        attrs = {
            'class': 'table',
        }
        template_name = 'django_tables2/bootstrap.html'

import django_tables2 as tables

class ResponseTable(tables.Table):
    '''
    skeleton for the questionnaire table
    '''

    edit = tables.TemplateColumn('<a style="color:#1abc9c;" class="far fa-edit fa-lg" href="?id={{record.id}}"></a>', verbose_name='')
    date = tables.DateTimeColumn(format='Y-m-d H:m:s')
    question = tables.Column()
    response = tables.Column()

    class Meta:
        exclude=('user',)
        attrs = {
            'class': 'table table-striped',
        }
        template_name = 'django_tables2/bootstrap.html'

class _Generic(tables.Table):
    '''
    skeleton for the metric table; all the model specific fields will
    be passed by `extra_columns`
    '''

    edit = tables.TemplateColumn('<a style="color:#1abc9c;" class="far fa-edit fa-lg" href="?activity={{record.activity}}&id={{record.id}}"></a>', verbose_name='')
    delete = tables.TemplateColumn('<a style="color:#c7254e;" class="far fa-trash-alt fa-lg" href="?activity={{record.activity}}&id={{record.id}}&delete"></a>', verbose_name='')
    time_stamp = tables.DateTimeColumn(format='Y-m-d H:i:s')

    class Meta:
        order_by = '-time_stamp'
        exclude=('user',)
        attrs = {
            'class': 'table table-striped',
        }
        template_name = 'django_tables2/bootstrap.html'

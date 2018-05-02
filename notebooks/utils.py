def value_count(x, name=None):
    '''
    Helper function that wraps df.value_counts() into a more
    presentable fashion.
    
    Example:
    ========
    dat = a|b|c
          1|2|3
          4|5|6 
    
    value_counts(dat.a) returns:
        a|count_a
        1|1
        4|1
        
    value_counts(dat.c) returns:
        c|count_c
        3|2
    Args:
    =====
        x (Pandas Series) data to count
        name (str, default='count_NAME') name to give to value count 
        column where NAME is `x.name`
    Yields:
    =======
        a dataframe with value_counts() for each unique value in `x`
    '''
    
    name = name if name else 'count_' + str(x.name)
    
    counts = pd.DataFrame(pd.Series(x.value_counts(),name=name))
    counts.index.name = x.name
    return counts
  
  
def load_css():
    '''
    Loads some handy CSS styles into jupyter including the
    bootstrap styles for <code>, <mark> and .lead
    
    Usage:
      import utils
      utils.load_css()
    Make sure this is called as the last command in a cell.
    '''

    from IPython.core.display import HTML

    css = '''<style>
    code {
        color: #c7254e !important;
        background-color: #f9f2f4 !important;
        font-size: 90% !important;
        padding: 2px 4px !important;
        border-radius: 4px !important;
    }
    .lead {
        font-weight: 300 !impotant;
        line-height: 1.4 !important;
        font-size: 21px !important;
    }
    mark {
        color: rgb(138, 109, 59) !important;
        font-weight: bold !important;
    }
    </style>
    '''

    return HTML(css)

convert = function(inputs) {

/*
This should be set by Django
    var lookup = {
        1:'Strongly disagree',
        2:'Disagree',
        3:'Slightly disagree',
        4:'Neither',
        5:'Slightly agree',
        6:'Agree',
        7:'Strongly agree'
    }
*/

    // lookup object key by value
    getValByKey = function(value) {
        if (value in lookup) {
            return value;
        } else {
            return Object.keys(lookup).filter(function(key) {return lookup[key] === value})[0];
        }
    }

    $(inputs).each(function(d) {

        /*
            Assumes main selector $(this) is a text input. This input 
            will get the 'hidden' type and a parent DIV will be
            generated around it; this parent DIV will be used to generate the
            noUislider. The now hidden input type will get updated
            automatically as the slider moves.
        */

        // generate slider div around input
        $(this).wrap( "<div class='q_slider'></div>" );
        var slider = $(this).parent()[0];
        var slider_id = $(this)[0].id

        // convert input to hidden
        $(this)[0].type = 'hidden';
        $(this)[0].required = false;

        var max = 8;
        var min = 0;

        noUiSlider.create(slider, {
            start: 4,
            tooltips: true,
            padding: 1,
            range: {
                'min': min,
                'max': max
            },
            step: 1,
            format: {
                to: function ( value ) {
                    var label = lookup[Math.floor(value)];
                    return label;
                },
                from: function ( value ) {
                    return value;
                }
            },
            pips: {
                mode: 'range',
                density: 100/(max-min)
            }
        });

        slider.noUiSlider.on('end', function(values, handle) {
            var number = getValByKey(values[0]);
            var input_id = '#' + slider_id
            $(input_id).val(number);
        });
    })
}

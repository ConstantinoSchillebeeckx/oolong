
/* ONLY USED ON METRIC.HTML */

// automatically animate a scroll to the
// selected element
// https://stackoverflow.com/a/1586379/1153897
$.fn.scrollView = function () {
    return this.each(function () {
        $('html, body').animate({
            scrollTop: $(this).offset().top - 80
        }, 500);
    });
}


jQuery('select, input, textarea').focus(function() {
    // since we show().hide() the timestamp div
    // prevent it from auto scrolling on first page load :(
    //if (this.id !== 'id_time_stamp') $(this).scrollView();
})

// on metric page load
jQuery(function () {

    // vars for datetime picker
    var start_input = jQuery('#id_time_stamp');
    var end_input = jQuery('#id_end');
    var picker_format = {
        format: "YYYY-MM-DD H:mm:ss",
        ignoreReadonly: true, // https://github.com/Eonasdan/bootstrap-datetimepicker/issues/1668
        allowInputToggle: true,
        showTodayButton: true,
        showClose: true,
        toolbarPlacement: 'top',
        widgetPositioning: {'vertical':'bottom'}
    }

    // on activity metric page load
    // scroll down a bit to fully load form
    // saves on screen real estate for mobile
    if(window.location.href.indexOf("activity") > -1) {
        jQuery('#anchor').scrollView();
    }


    // build timestamp datetime picker
    // we show/hide start to autopopulate with
    // user's current time - a little dirty ...
    if (start_input.length) {
        var start_picker = start_input.datetimepicker(picker_format)
        start_picker.data("DateTimePicker").show().hide();

        start_picker.on("dp.show", function(e) {
            // show time by default
            $('[data-action=togglePicker]').click();
            $(this).scrollView();
        })

    }

    // build end datetime picker
    end_input.datetimepicker(picker_format);

    // set the end timestamp to the start timestamp if the default
    // end timestamp is before the end timestamp
    end_input.on("dp.show", function (e) {
        var start = start_input.data('DateTimePicker').date()
        var end = end_input.data('DateTimePicker').date()

        // show time by default
        $('[data-action=togglePicker]').click();

        if (end < start) {
            $(this).data('DateTimePicker').date(start);
        }
    });
});


/* ONLY USED ON METRIC.HTML */


convert = function(inputs) {
// this function isn't currently being used
// see https://github.com/ConstantinoSchillebeeckx/oolong/issues/2

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

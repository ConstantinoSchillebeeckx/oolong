
/* ONLY USED ON METRIC.HTML */
var isMobile = false; //initiate as false

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
    if (this.id !== 'id_time_stamp' && !isMobile) $(this).scrollView();
})

// on metric page load
jQuery(function () {

    // device detection
    // https://stackoverflow.com/a/3540295/1153897
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
        || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) isMobile = true;

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
    // scroll down a bit to fully load form.
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
            // show time view instead of date
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

        // show time view instead of date
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

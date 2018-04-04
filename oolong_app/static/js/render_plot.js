function render_drink_plot(plotDat) {
    var chart;
    /*
    Expects a Django view to exist:
    CREATE OR REPLACE VIEW public.plot_drink AS
    select
        user_id,
        type,
        time_stamp::date::text as "date",
        sum( case when metric_drink.units::text = 'ml'::text then metric_drink.volume * 0.033814::double precision else metric_drink.volume end )
    from
        metric_drink
    group by
        user_id,
        type,
        time_stamp::date::text;

    Param:
    ======
    plotDat is a query of the view plot_drink 
    for the user currently logged in.

    It's format is a list of objects with keys:
    - type
    - date
    - sum
    
    */


    // convert data
    var tmp = d3.nest()
                .key(function(d) { return d.type })
                .key(function(d) { return d.date })
                .rollup(function(d) { 
                    return d3.sum(d, function(i) { return i.fl_oz });
                })
                .map(plotDat);

    // multiBarChart expects all series to have the same x's
    // in the same order!
    // so we have to fill in those that are missing
    var all_dates = d3.set(plotDat.map(function(d) { 
                        return d.date;
                    })).values().sort();


    // make all series stackable
    var data = Object.keys(tmp).map(function(type) {
        var vals = tmp[type]; // {YYYY-MM-DD: vol}
        return {
            key: type,
            nonStackable: false,
            values: all_dates.map(function(i) {
                var epoch = new Date(i).valueOf();
                if (i in vals) {
                    return {x: epoch, y: vals[i]}
                } else {
                    return {x: epoch, y: 0}
                }
            })
        };
    })


    nv.addGraph(function() {

        chart = nv.models.multiBarChart()
            .stacked(true)
            .color(d3.scale.category10().range())


        chart.xAxis
            .tickFormat(function(d) {
                return d3.time.format.utc('%Y-%m-%d')(new Date(d))
            })

        chart.yAxis
             .showMaxMin(true)
             .axisLabel("Volume (fl. oz.)")


        d3.select('#chart').append('svg')
          .datum(data)
          .call(chart);


        nv.utils.windowResize(chart.update);

        return chart;
    });
}


function render_mood_plot(plotDat, agg) {
    var chart;

    console.log(plotDat)

    // the type of aggregating function to display
    // either avg, or median
    // must be a column in the view `plot_response`
    if (typeof agg === 'undefined') agg='avg'


    // Django expects a view with the name `plot_response` to exist:
    /*
    SELECT t3.date::text AS date,
        date_part('epoch'::text, t3.date)::numeric::integer AS epoch,
        t3.questionnaire,
        avg(t3.score) AS avg,
        stddev_samp(t3.score) AS std,
        t3.user_id,
        median(t3.score) AS median
       FROM ( SELECT t1.id,
                t1.date::date AS date,
                t1.score,
                t2.questionnaire_id AS questionnaire,
                t1.user_id
               FROM response t1
                 LEFT JOIN question t2 ON t1.question_id = t2.id
              WHERE t2.questionnaire_id <> 'Summary'::text) t3
      GROUP BY t3.user_id, t3.questionnaire, t3.date
      ORDER BY t3.date, t3.questionnaire;
    */

    var lookup = {
        1:'Strongly disagree',
        2:'Disagree',
        3:'Slightly disagree',
        4:'Neutral',
        5:'Slightly agree',
        6:'Agree',
        7:'Strongly agree',
    }

    var data = d3.nest()
                .key(function(d) { return d.questionnaire })
                .rollup(function(d) { 
                    return d.map(function(i) { 
                        return {
                            x:i.epoch*1000, 
                            y:i[agg]
                        } 
                    }) 
                })
                .entries(plotDat)


    nv.addGraph(function() {

        chart = nv.models.lineChart()
            .color(d3.scale.category10().range())
            .options({
                duration: 300,
                useInteractiveGuideline: true,
                margin: {left: 60, right: 50},
            });

        chart.xAxis
            //.axisLabel("Date")
            .tickFormat(function(d,i) {
                return d3.time.format('%Y-%m-%d')(new Date(d))
            })

        // we hack the y-axis a bit so that we can display labels instead
        // of the averaged mood score; however the tooltip also makes
        // use of this formatting, so we pass the exact value if its
        // not an integer found in `lookup`
        var yMin = 0.5, yMax = 7.5;
        chart.yAxis
             .showMaxMin(false)
             .axisLabel(agg + " score")
             .ticks(Object.keys(lookup).length)
/*
For the time being we don't convert y-axis labels.
I'm doing this since I've switch the labels and scoring around
from 1-7 to 1-5.
            .tickFormat(function(d) {
                if (d in lookup) {
                    return lookup[d];
                } else if (d != yMax && d!= yMin) {
                    return d.toFixed(2);
                }
            })
*/

        chart.yDomain([yMin,yMax])


        d3.select('#chart').append('svg')
          .datum(data)
          .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
}



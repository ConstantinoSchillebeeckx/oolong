function render_response_plot(plotDat, agg) {
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
                .rollup(function(d) { return d.map(function(i) { return {x:i.epoch*1000, y:i[agg]} }) })
                .entries(plotDat)


    nv.addGraph(function() {

        chart = nv.models.lineChart()
            .options({
                duration: 300,
                useInteractiveGuideline: true,
                margin: {left: 110, right: 50},
            });

        chart.xAxis
            .axisLabel("Date")
            .tickFormat(function(d,i) {
                return d3.time.format('%Y-%m-%d')(new Date(d))
            })

        // we hack the y-axis a bit so that we can display labels instead
        // of the averaged mood score; however the tooltip also makes
        // use of this formatting, so we pass the exact value if its
        // not an integer found in `lookup`
        var yMin = 0.5, yMax = 7.5;
        chart.yAxis
            .showMaxMin(true)
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



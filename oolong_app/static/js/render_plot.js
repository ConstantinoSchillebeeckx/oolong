function render_response_plot(plotDat, agg) {
    var chart;

    // the type of aggregating function to display
    // either avg, or median
    // must be a column in the view `plot_response`
    if (typeof agg === 'undefined') agg='avg'


    // Django expects a view with the name `plot_response` to exist:
    // select "date", extract('epoch' from "date")::numeric::integer epoch, questionniare, avg(score), stddev_samp(score) as std from (
    // select t1.id, "date"::date, score, questionnaire_id as questionniare
    // FROM public.response t1
    // left join available_response t2 on t1.response_id = t2.id
    // where questionnaire_id != 'Summary'
    // ) t3
    // group by questionniare, "date"
    // order by "date", questionniare

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
                .key(function(d) { return d.questionnaire_id })
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
            .tickFormat(function(d) {
                if (d in lookup) {
                    return lookup[d];
                } else if (d != yMax && d!= yMin) {
                    return d.toFixed(2);
                }
            })

        chart.yDomain([yMin,yMax])


        d3.select('#chart').append('svg')
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
}



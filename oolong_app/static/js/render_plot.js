function render_response_plot(plotDat) {
    var chart;


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
        3:'Neutral',
        4:'Agree',
        5:'Strongly agree',
    }

    var data = d3.nest()
                .key(function(d) { return d.questionnaire_id })
                .rollup(function(d) { return d.map(function(i) { return {x:i.epoch*1000, y:i.avg} }) })
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
            .tickFormat(function(d) {
                return d3.time.format('%Y-%m-%d')(new Date(d))
            })

        chart.yAxis
            .showMaxMin(true)
            .ticks(5)
            .tickFormat(function(d) {
                return lookup[d];
            })

        chart.yDomain([0.5,5.5])


        d3.select('#chart').append('svg')
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
}



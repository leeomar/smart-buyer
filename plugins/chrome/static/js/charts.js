$(function() {
    var url = window.location.href;
    var re_list = {
        '360buy': /360buy\.com\/product/,
        'letao': /letao\.com\/shoe/,
        'okbuy': /okbuy\.com\/product\/detail/,
    };
    var priceArea = $(document.createElement('div'))
    priceArea.css({
        'position': 'absolute',
        'height': '167px',
        'width': '100%',
        'background-color': '#FFFFFF',
        'border-bottom': '2px solid #000000',
        'z-index': '10000',
        'display': 'none'
    });
    var priceChart = $(document.createElement('div'))
    priceChart.css({
        'height': '167px',
        'width': '100%',
    });
    priceChart.attr({
        'id': 'price_chart'
    });
    var priceButton = $(document.createElement('div'))
    priceButton.css({
        'position': 'absolute',
        'height': '30px',
        'width': '80px',
        'background-color': 'yellow',
        'cursor': 'pointer',
    });
    priceButton.html('查看价格曲线');
    function fadeInChart() {
        priceArea.slideDown(300);
        priceButton.html('收起价格曲线');
        priceButton.unbind('click', fadeInChart);
        priceButton.bind('click', fadeOutChart);
    }
    function fadeOutChart() {
        priceArea.slideUp(250);
        priceButton.html('查看价格曲线');
        priceButton.unbind('click', fadeOutChart);
        priceButton.bind('click', fadeInChart);
    }

    priceButton.bind('mouseenter', fadeInChart);
    priceArea.prepend(priceChart);
    $('body').prepend(priceArea);

    if (re_list['360buy'].test(url)){
        priceButton.css({
            'margin-left': '190px',
        })
        $('#summary').prepend(priceButton);
    }
    if (re_list['letao'].test(url)){
        priceButton.css({
            'margin-left': '190px',
        })
        $('#shoesale').prepend(priceButton);
    }
    if (re_list['okbuy'].test(url)){
        priceButton.css({
            'margin-left': '190px',
        })
        $('.pProductTitle').prepend(priceButton);
    }
    var request = {
        'type': 'getprice',
        'data': window.location.href
    };
    chrome.extension.sendRequest(request, function(response) {
        if (200 != response.status)
            return
        window.chart = new Highcharts.Chart({
            chart : {
                renderTo : 'price_chart',
                defaultSeriesType: 'line',
            },
            title: {
                text: '价格走势',
                x: -20
            },
            xAxis: {
                categories: response.timeline
            },
            yAxis: {
                title: {
                    text: '价格 (￥)'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                    return this.series.name + ': ' + this.y ;
                }
            },
            legend: {
                enabled: false
            },
            series: response.series
        });
    });
})

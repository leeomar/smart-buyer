$(function(){
    chrome.extension.onRequest.addListener(
        function(request, sender, callback){
            if ('getprice' == request.type){
                var req = $.getJSON('http://chrome.tuanzz.com/price_trend', {
                    url: request.data
                }, callback);
                req.error(callback);
            } else if ('getxpath' == request.type){
                callback('getxpath');
            }
        });
});

$(function() {
    var alldom = $("body *");
    var leafdom = [];
    //选择器激活后，要给所有叶子结点绑定的事件
    function clickevent(){
        event.preventDefault();
        alert(getxpath($(this)));
        unbindlevent();
        leaveevent.apply($(this));
    }
    function enterevent(){
        $(this).attr('border_temp',
                    $(this).css('border'));
        $(this).css('border', '2px solid blue');
    }
    function leaveevent(){
        $(this).css('border',
                    $(this).attr('border_temp'));
    }
    //筛选所有叶子结点并绑定 click 事件查找 xpath
    (function bindevent(){
        $.each(alldom, function(){
            if (0 == $(this).children().length){
                $(this).bind({
                    'click': clickevent,
                    'mouseenter': enterevent,
                    'mouseleave': leaveevent
                });
                leafdom.push(this);
            };
        });
    })();
    //当查找结束后取消事件绑定
    function unbindlevent(){
        $.each(leafdom, function(){
            $(this).unbind({
                'click': clickevent,
                'mouseenter': enterevent,
                'mouseleave': leaveevent
            });
        })
    }
    //递归查找 xpath
    function getxpath(x){
        var xtag = x[0].tagName.toLowerCase();
        var xid = x.attr('id');
        if (undefined != xid){
            return('//' + xtag + '[contains(@id, "' + xid + '")]');
        };
        if ('body' == xtag){
            return('//html/body');
        }
        var xparent = x.parent();
        // scrapy 的 hxs.select 从 1 开始计数，不是从 0 开始，故结果 +1
        var xindex = xparent.find(xtag).index(x) + 1;
        return(getxpath(xparent) + '/' + xtag + '[' + xindex + ']');
    }
})

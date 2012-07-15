$(function(){
    chrome.tabs.getSelected(null, function(tab){
        try {
            //在当前打开的标签中导入 jquery.min.js 和 xpath.js ，触发 xpath 的价格查找操作
            chrome.tabs.executeScript(tab.id, {file: "static/js/jquery.min.js" }, function(){
                chrome.tabs.executeScript(tab.id, {file: "static/js/xpath.js" }, function(){
                    document.getElementById('msg').innerText = "请在页面中选择价格";
                });
            })
        } catch (err) {
            document.getElementById('msg').innerText = "Error: " + err.message;
        }
    });
})
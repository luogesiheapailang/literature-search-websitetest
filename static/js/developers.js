// 第一次加载该网页时运行的内容，一般用来定义函数
if (first_load_js.developers) {

    function reload_developers(){
        // 完成第一次加载后每次进入该网页都会运行的内容，一般用于加载main标签内部的监听、定时器
        history.pushState({}, '', '/index?page=developers'); // 更改网页url
        document.getElementById("private-title").innerHTML = '文献搜索：开发团队';

    }
    function exit_developers(){
        // 退出该页面执行的函数，一般用于关闭全局监听、定时等
    }

    eval("reload_" + currentPage + "()")
    first_load_js.developers = false; // 写在最后，当加载完该js才认为第一次加载页面成功
}
let first_load_js = {
    "home": true,
    "details": true,
    "history": true,
    "developers": true,
    "document": true,
}

let currentPage = null;
function get_page(PageSign, privateData=null) {
    if (PageSign === 'empty'){
        if (currentPage) {eval("exit_" + currentPage + "()")}
        document.querySelector('main').innerHTML = `<h1 style="color:white; text-align: center; margin-top: 30%">即将开放，敬请期待！</h1>`
        currentPage = null;
    }
    else {
        if (currentPage && first_load_js[currentPage] === false) {
            // 使用exit_xxx()函数来终止运行中监听、定时
            eval("exit_" + currentPage + "()")
        }
        currentPage = PageSign

        // 发送 AJAX 请求
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/index', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({page_sign: PageSign, private_data: privateData}));

        xhr.onload = function () {
            const response = JSON.parse(xhr.responseText);
            // console.log(response)
            if (response.state === 200) {
                document.getElementById("private-css").href = "/static/css/" + PageSign + ".css"
                document.querySelector(".main").innerHTML = response.privateHTML;

                if (first_load_js[PageSign]) {
                    // 另外起一个线程加载js，有关该js的初始化操作都放在对应的js中执行
                    const newScript = document.createElement('script')
                    newScript.src = "/static/js/" + PageSign + ".js"
                    document.body.appendChild(newScript);
                } else {
                    // 加载最后一次get的页面
                    eval("reload_" + currentPage + "()")
                }
            }
        };

        xhr.onerror = function () {
            alert("页面请求失败");
        };
    }
}


// 获取浏览器网址栏的参数
const params = window.location.search.substring(1).split("&");
let searchPara = {};
for (let i = 0; i < params.length; i++) {
    let param = params[i].split("=");
    searchPara[param[0]] = param[1];
}

get_page('home')
if (searchPara.page === 'details' && searchPara.id) {
    get_page('details', searchPara.id)
}
else if (['history','document', 'developers'].includes(searchPara.page)) {
    get_page(searchPara.page)
}


// 显示返回顶部按钮
function showBackToTopBtn() {
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        document.getElementById("back-to-top-btn").style.display = "block";
    } else {
        document.getElementById("back-to-top-btn").style.display = "none";
    }
}
window.addEventListener('scroll', showBackToTopBtn);

// 点击按钮返回顶部
function backToTop() {
    document.body.scrollTop = 0; // 兼容 Safari
    document.documentElement.scrollTop = 0; // 兼容 Chrome, Firefox, IE 和 Opera
}

document.getElementById("back-to-top-btn").addEventListener('click', backToTop);


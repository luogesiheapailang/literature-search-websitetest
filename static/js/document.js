
if (first_load_js.document) {
    const left_width = document.querySelector('.left-column').offsetWidth
    let content = document.querySelector('.content')
    content.style.width = 0.8*left_width + 'px'
    let top_height = content.getBoundingClientRect().height - 20;
    // 开启固定左侧栏
    function fixLeftColumn() {
        if (document.body.scrollTop >= top_height|| document.documentElement.scrollTop >= top_height) {
            content.style.position = "fixed";
            content.style.top = '20px';
        } else {
            content.style.position = "relative";
            content.style.top = '0';
        }
    }

    function reload_document(){history.pushState({}, '', '/index?page=document');
        document.getElementById("private-title").innerHTML = '文献搜索：功能说明';
        window.addEventListener('scroll', fixLeftColumn);
    }
    function exit_document(){
        window.removeEventListener('scroll', fixLeftColumn);
    }

    eval("reload_" + currentPage + "()")
    first_load_js.document = false;
}
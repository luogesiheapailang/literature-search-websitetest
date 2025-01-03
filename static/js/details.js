if (first_load_js.details) {
    function random(max) {
        return Math.floor(Math.random() * max);
    }

    let activeElement = null;
    let initialX, initialY;
    let initialMouseX, initialMouseY;
    let xBias = 0;
    let yBias = 0;
    let first;

    // 拖拽开始时记录初始位置
    function dragStart(e) {
        activeElement = e.target;
        xBias = 0;
        yBias = 0;
        initialX = parseInt(activeElement.style.left.slice(0, -2));
        initialY = parseInt(activeElement.style.top.slice(0, -2));
        first = true
    }

    function dragEnd(e) {
        activeElement = null;
    }

    function drag(e) {
        if (activeElement) {
            if (first){
                initialMouseX = e.pageX;
                initialMouseY = e.pageY;
                first = false;
            }

            // e.preventDefault();
            xBias = e.pageX - initialMouseX;
            yBias = e.pageY - initialMouseY;
            // 将bias除以1.25以抵消index.css中缩放125%的影响
            activeElement.style.left = initialX + xBias/1.25 + 'px';
            activeElement.style.top = initialY + yBias/1.25 + 'px';

        }
    }

    function drawTopic(data) {
        // console.log(typeof data,data)
        const topicContainer = document.getElementById('topic-container');
        topicContainer.innerHTML = '';

        if (data) {
            data = data.replace(/'/g, '"');
            data = JSON.parse(data);
            // 计算data中值的和
            let sum = 0;
            for (const topic in data) {
                sum += data[topic];
            }
            // 计算每个标签的边长（按正方形算）
            const maxWidth = document.getElementById('topic-container').offsetWidth
            const maxHeight = document.getElementById('topic-container').offsetHeight
            const totalArea = 10000; // 容器的总面积
            for (const topic in data) {
                data[topic] = Math.sqrt(totalArea * data[topic] / sum);
            }
            // console.log(data)

            const colorBoard = ['rgba(232,78,78,0.7)', 'rgba(236,122,60,0.65)', 'rgba(243,214,62,0.68)', 'rgba(125,231,112,0.68)',
                'rgba(155,239,246,0.68)', 'rgba(88,154,243,0.71)', 'rgba(127,127,229,0.73)'];

            // 遍历数据并渲染圆形元素
            for (const topic in data) {
                const a = data[topic];
                const circle = document.createElement('div');
                circle.className = 'topic';
                circle.innerText = topic;
                circle.style.backgroundColor = colorBoard[random(7)];
                // 设置圆的d大小
                circle.style.width = a * 2 + 'px';
                circle.style.height = a * 2 + 'px';

                circle.style.left = 0.05*maxWidth + random(maxWidth-100) + 'px';
                circle.style.top = random(maxHeight-100) + 'px';

                circle.style.fontSize = a / 2 + 'px';

                circle.addEventListener("mousedown", dragStart);

                topicContainer.appendChild(circle);
            }
        }
    }

    function reload_details() {
        history.pushState({}, '', `/index?page=details&id=${document.getElementById("id").className}`);
        document.getElementById("private-title").innerHTML = '文献搜索：'+ document.getElementById("TI").innerHTML;

        document.addEventListener("mouseup", dragEnd)
        document.addEventListener("mousemove", drag);
        setTimeout(function() {
            drawTopic(document.getElementById("topic-container").innerHTML)
        },100)
        }

    function exit_details(){
        document.removeEventListener("mousemove", drag);
        document.removeEventListener("mouseup", dragEnd)
    }

    eval("reload_" + currentPage + "()")

    first_load_js.details = false
}

if (first_load_js.history) {
    function get_history() {
        fetch('/history')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            const historyContainer = document.getElementById("history-container");
            for (let i = 0; i <= data.length; i++) {
                const historyItem = data[i];
                const historyElement = document.createElement("div");
                historyElement.classList.add("history-item");
                historyElement.innerHTML = `
                    <h2 onclick="get_page('details', '${historyItem[0]}')">${historyItem[2]}</h2>
                    <p>浏览日期：${historyItem[1]}</p>
                `;
                historyContainer.appendChild(historyElement);
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    }

    function reload_history() {
        history.pushState({}, '', '/index?page=history');
        document.getElementById("private-title").innerHTML = '文献搜索：历史记录';
        get_history()
    }
    function exit_history(){}

    eval("reload_" + currentPage + "()")
    first_load_js.history = false
}

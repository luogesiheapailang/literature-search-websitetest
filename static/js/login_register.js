const signInBtn = document.getElementById("signin");
const signUpBtn = document.getElementById("signup");
const registerForm = document.getElementById("form1");
const loginForm = document.getElementById("form2");
const container = document.querySelector(".container");


window.onload = () => {
    container.classList.remove("right-panel-active");
}

signInBtn.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

// 同步两个表单的email和password信息
let RegisterEmail = document.getElementById("Remail");
let LoginEmail = document.getElementById("Lemail");
RegisterEmail.oninput = () => {
    LoginEmail.value = RegisterEmail.value
}
LoginEmail.oninput = () => {
    RegisterEmail.value = LoginEmail.value
}


let Lpassword = document.getElementById("Lpassword");
let Rpassword = document.getElementById("Rpassword");
let Rcpassword = document.getElementById("Rcpassword");
// 同步左右表单的密码
Lpassword.oninput = () => {
    Rpassword.value = Lpassword.value
}
// 验证两次密码输入是否相同
Rpassword.oninput = function () {
    Lpassword.value = Rpassword.value // 同步至左表单的密码
    if (Rpassword.value !== Rcpassword.value) {
        Rcpassword.style.color = 'red'; // 标红第二个输入框的文字
    } else {
        Rcpassword.style.color = ''
    } // 如果两次输入的密码一致，恢复默认颜色
};
Rcpassword.oninput = function () {
    if (Rpassword.value !== Rcpassword.value) {
        Rcpassword.style.color = 'red';
    } else {
        Rcpassword.style.color = ''
    }
};

// 注册操作
registerForm.addEventListener("submit", function (event) {
    event.preventDefault(); // 阻止表单提交
    if (Rpassword.value !== Rcpassword.value) {
        alert("两次密码不同，请重新输入")
    } else {
        // 构造注册表单
        const submitForm = {
            username: document.getElementById("username").value,
            email: RegisterEmail.value,
            password: Rpassword.value,
        };
        // console.log(submitForm)

        // 发送 AJAX 请求
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/login_register', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(submitForm));

        xhr.onload = function () {
            const response = JSON.parse(xhr.responseText);
            alert(response.message);
            if (response.state === 200) {
                window.location.href = 'index';
            }
        };

        xhr.onerror = function () {
            alert("请求失败");
        };

    }
});

loginForm.addEventListener("submit", function (event) {
    event.preventDefault();
    // 构造登入表单
    const submitForm = {
        email: LoginEmail.value,
        password: Lpassword.value,
    };
    // 发送 AJAX 请求
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/login_register', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(JSON.stringify(submitForm));

    // 接受 Ajax 响应
    xhr.onload = function () {
        const response = JSON.parse(xhr.responseText);
        if (response.state === 200) {
            window.location.href = 'index';
        } else {
            alert(response.message);
        }
    };
    xhr.onerror = function () {
        alert("请求失败");
    };
});

let running = 0;

String.prototype.format = String.prototype.f = function(){
    var args = arguments;
    return this.replace(/\{(\d+)\}/g, function(m,n){
        return args[n] ? args[n] : m;
    });
};

function httpGet(theUrl, from, subj, text, pass, spreadsheet)
{
    // 1. Создаём новый объект XMLHttpRequest
    const xhr = new XMLHttpRequest();

// 2. Конфигурируем его: GET-запрос на URL
    xhr.open('POST', 'http://127.0.0.1:10001', false);
    xhr.setRequestHeader('Content-Type', 'multipart/form-data');

// 3. Отсылаем запрос
    const post_str = "from={0}&subj={1}&text={2}&pass={3}&spreadsheet={4}".f(from, subj, text, pass, spreadsheet);
    xhr.send(post_str);

// 4. Если код ответа сервера не 200, то это ошибка
    if (xhr.status !== 200) {
        // обработать ошибку
        alert( xhr.status + ': ' + xhr.statusText ); // пример вывода: 404: Not Found
    } else {
        // вывести результат
        console.log( xhr.responseText ); // responseText -- текст ответа.
    }
}


// Sends a Get request to localhost:10001
// You should start the server first
function start_mailing(from, subj, text, pass, spreadsheet) {
    httpGet("127.0.0.1:10001", from, subj, text, pass, spreadsheet);
}


// function is being called if the process was stopped or not started
// gets all the data and calls start mailing
// Also checks the fields, but the check is light
function successful_run() {
    running = 1;
    alert("Script just started running! \nIf it doesn't work, please check LOGIN and PASSWORD fields!\nAlso the Python server should be up!");
    let tb_login = document.getElementById("txt_login");
    let tb_pass = document.getElementById("password");
    let tb_spreadsheet = document.getElementById("txt_spreadsheet");
    let tb_text = document.getElementById("txt_text");
    let tb_subj = document.getElementById("subj");

    //
    function fields_are_correct(tb_login, tb_pass, tb_spreadsheet) {
        return tb_login.value !== "" && tb_pass !== "" && tb_spreadsheet !== "";
    }

    if (fields_are_correct(tb_login, tb_pass, tb_spreadsheet)) {
        const text = tb_text.value;
        start_mailing(tb_login.value, tb_subj.value, text, tb_pass.value, tb_spreadsheet.value);
    }
}
    function unsuccessful_run() {
        alert("Already running! Please stop before clicking again!");
    }

    function successful_stop() {
        alert("Script was successfully stopped!");
        running = 0;
    }

    function unsuccessful_stop() {
        alert("You can't stop what's not started!");
    }

    function error_alert() {
        alert("Unexpected error!");
    }

    function stop(){
        if(running === 1){
            successful_stop();
        }
        else if (running === 0){
            unsuccessful_stop();
        }
        else{
            error_alert()
        }
        running = 0;

    }
function run(){
    if (running === 0)
    {
        successful_run();
    }
    else if (running === 1){
        unsuccessful_run()
    }

    else{
        error_alert();
    }
}
document.addEventListener('DOMContentLoaded', function () {

    const btadd = document.getElementById("bt_start");
    btadd.addEventListener('click', run)
});

document.addEventListener('DOMContentLoaded', function () {

    const btstop = document.getElementById("bt_stop");
    btstop.addEventListener('click', stop);
});


// const $ = document.querySelector.bind(document);
// const $$ = document.querySelectorAll.bind(document);
// const time = $(".time");
// var ws = new WebSocket("ws://192.168.10.121:8000/ws");

var host = window.location.host; 
    // console.log(host)
var ws = new WebSocket(`ws://${host}/ws`); 
// var ws = new WebSocket("ws://192.168.10.121:8000/ws");

const id = ["SUB01","SUB02", "SUB03", "SUB04", "SUB05", "SUB06", "SUB07", "SUB08", "SUB09", "SUB10", "SUB11", "SUB12", "SUB13", "SUB14"] ;
function led_on(id_name, class_name = "main-led-active") {
    var element = document.getElementById(id_name);
    element.classList.add(class_name);
}
function led_off(id_name, class_name = "main-led-active") {
    var element = document.getElementById(id_name);
    element.classList.remove(class_name);
}
ws.onmessage = function(event) {
    
    var data = JSON.parse(event.data);
    let temp = data.CPU
    time.innerHTML = temp
    let leds = data.leds
    // console.log(leds)
    for (let i = 0; i < id.length; i++) {
        if(leds[i]){
            led_on(id[i])
        }else{
            led_off(id[i])
        }
    }
    // console.log(data.CPU)
    // document.getElementById("cpu_percent").innerHTML = result.cpu_percent+'%'
    // document.getElementById("cpu_temp").innerHTML = result.cpu_temp
    // document.getElementById("cpu_percent_value").style.setProperty('--radius', result.cpu_percent+'deg');
    
    // var messages = document.getElementById('messages')
    // var message = document.createElement('li')
    // var content = document.createTextNode(result)
    // var cpu =document.getElementById("test").innerHTML = result.cpu
    // console.log(result.cpu.gpu)
    // message.appendChild(content)
    // messages.appendChild(message)
}

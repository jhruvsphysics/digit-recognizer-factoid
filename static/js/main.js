const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let coord = { x: 0, y: 0 };
const display = document.getElementById("displayGuess")

document.addEventListener('mousedown', start);
document.addEventListener('mouseup', stop);
document.querySelector('#erase').onclick = () => {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, 400, 400);
    document.getElementById('instruction').classList.remove("hide")
    display.innerHTML = '<span style="color: #5da6d7">digit</span> recognizer factoid'
}
document.querySelector('#submit').onclick = submitImg

function displayFactoid(guess, msg) {
    msg = msg.replace(/[0-9]/, ()=>'')
    document.getElementById('instruction').classList.toggle("hide")
    display.innerHTML = `<span style="color: #5da6d7; font-size: 55px">${guess}</span>${msg}`
}

function factoid(msg) {
    let [guess, confidence] = msg.split(" ")
    fetch(`http://numbersapi.com/${guess}`)
    .then(res => res.text())
    .then(msg => displayFactoid(guess, msg))
}

function submitImg() {
    // get image URI from canvas object
    // PNG base64
    let image_base64 = canvas.toDataURL('image/jpeg').replace(/^data:image\/jpeg;base64,/, "");

    fetch('/', {
        method: 'POST',
        body: image_base64
    })
    .then(res => res.text())
    .then(msg => factoid(msg))
}
ctx.canvas.width = 400;
ctx.canvas.height = 400;

// function resize() {
//     ctx.canvas.width = window.innerWidth;
//     ctx.canvas.height = window.innerHeight;
// }

// resize();

ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);

function start(event) {
    document.addEventListener('mousemove', draw);
    reposition(event);
}

function reposition(event) {
    coord.x = event.clientX - canvas.offsetLeft;
    coord.y = event.clientY - canvas.offsetTop;
}

function stop() {
    document.removeEventListener('mousemove', draw);
}

function draw(event) {
    ctx.beginPath();
    ctx.lineWidth = 30;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'white';
    ctx.moveTo(coord.x, coord.y);
    reposition(event);
    ctx.lineTo(coord.x, coord.y);
    ctx.stroke();
}
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let coord = { x: 0, y: 0 };

document.addEventListener('mousedown', start);
document.addEventListener('mouseup', stop);
document.querySelector('#erase').onclick = () => {
    ctx.clearRect(0, 0, 500, 500);
}
document.querySelector('#submit').onclick = submitImg

function submitImg() {
    // get image URI from canvas object
    // PNG base64
    console.log("yeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeye")
    console.log(typeof canvas)
    let image_base64 = canvas.toDataURL('image/jpeg').replace(/^data:image\/jpeg;base64,/, "");
    console.log(image_base64)

    fetch('/', {
        method: 'POST',
        body: image_base64
    })
    .then(res => console.log(res))
}

ctx.canvas.width = 400;
ctx.canvas.height = 400;
// function resize() {
//     ctx.canvas.width = window.innerWidth;
//     ctx.canvas.height = window.innerHeight;
// }

// resize();

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
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#ACD3ED';
    ctx.moveTo(coord.x, coord.y);
    reposition(event);
    ctx.lineTo(coord.x, coord.y);
    ctx.stroke();
}
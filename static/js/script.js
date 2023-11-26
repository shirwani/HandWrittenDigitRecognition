function startDrawing(e) {
    isDrawing = true;
    draw(e);
}

function stopDrawing() {
    isDrawing = false;
    ctx.beginPath();
}

function draw(e) {
    if (!isDrawing) return;

    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#000';

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function captureContent() {
    const imageDataUrl = canvas.toDataURL();
    const link = document.createElement('a');
    link.href = imageDataUrl;

    selectedIdx = document.getElementById('digits').selectedIndex
    filename = document.getElementById('digits').options[selectedIdx].value
    console.log(filename)

    link.download = filename + '_' + generateTimestampString() + '.png';
    link.click();

    clearCanvas()
}

function reloadPage() {
    console.log("Reloading...")
    location.reload()
}

function sendContentToApp() {
    const dataUrl = canvas.toDataURL();
    var xhr = new XMLHttpRequest();
    var url = window.location.href + '/result';

    console.log(url)

    // Set up the request
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Set up the callback function for when the request completes
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the response from the Flask server if needed
            // console.log('Response:', xhr.responseText);

            document.getElementById('message').innerHTML = xhr.responseText;
        }
    };

    // Prepare the data to be sent as JSON
    var jsonData = JSON.stringify(dataUrl);
    console.log(jsonData);

    // Send the request with the captured data
    xhr.send(jsonData);
}

function generateTimestampString() {
    var currentDate = new Date();

    var year = currentDate.getFullYear();
    var month = ('0' + (currentDate.getMonth() + 1)).slice(-2); // Months are zero-based
    var day = ('0' + currentDate.getDate()).slice(-2);
    var hours = ('0' + currentDate.getHours()).slice(-2);
    var minutes = ('0' + currentDate.getMinutes()).slice(-2);
    var seconds = ('0' + currentDate.getSeconds()).slice(-2);

    var timestampString = year + month + day + hours + minutes + seconds;

    return timestampString;
}


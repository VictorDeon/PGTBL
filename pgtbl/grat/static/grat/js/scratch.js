let generate = function(idCanvas, idMessage, message) {
    // Find canvas
    let canvas = document.getElementById(idCanvas);

    // Draw a object
    let ctx = canvas.getContext("2d");

    // Draw a new shape on top of existing canvas content
    ctx.globalCompositeOperation = "source-over";

    // Begin a path to draw a circle
    ctx.beginPath();

    // Create a circle
    let centerX = canvas.width / 2;
    let centerY = canvas.height / 2;
    let radius = 60; // width of circle
    let startAngle = 0;
    let endAngle = 2 * Math.PI;
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);

    // Circle color
    ctx.fillStyle = "#ccc";

    // Scratch Here
        ctx.fill();
        ctx.font = "18px Arial";
        ctx.fillStyle = "#fff";
        ctx.fillText("SCRATCH", 30, 75);

    // Messages
    document.getElementById(idMessage).innerHTML = message;
 }

let scratch = function(idCanvas, idMessage) {
    // Find canvas
    let canvas = document.getElementById(idCanvas);

    // Draw a object
    let ctx = canvas.getContext("2d");

    // Declare variables
    let lastX;
    let lastY;
    let mouseX;
    let mouseY;

    // get coordenate of scratch canvas (top and left)
    let isMouseDown = false;

    // When you click a mouse into canvas
    function handleMouseDown(event) {
      let canvasOffset = canvas.getBoundingClientRect();
      let offsetX = canvasOffset.left;
      let offsetY = canvasOffset.top;

      // Mouse position on the X axis inside the canvas
      mouseX = parseInt(event.clientX - offsetX);
      // Mouse position on the Y axis inside the canvas
      mouseY = parseInt(event.clientY - offsetY);
      // Store the lastX and lastY cordenate position
      lastX = mouseX;
      lastY = mouseY;
      isMouseDown = true;
    }

    // When you remove the mouse click from inside the canvas
    function handleMouseUp(event) {
      let canvasOffset = canvas.getBoundingClientRect();
      let offsetX = canvasOffset.left;
      let offsetY = canvasOffset.top;

      // Mouse position on the X axis inside the canvas
      mouseX = parseInt(event.clientX - offsetX);
      // Mouse position on the Y axis inside the canvas
      mouseY = parseInt(event.clientY - offsetY);
      isMouseDown=false;
    }

    // When your mouse leaves the canvas
    function handleMouseOut(event) {
      let canvasOffset = canvas.getBoundingClientRect();
      let offsetX = canvasOffset.left;
      let offsetY = canvasOffset.top;

      // Mouse position on the X axis outside the canvas
      mouseX = parseInt(event.clientX - offsetX);
      // Mouse position on the Y axis outside the canvas
      mouseY = parseInt(event.clientY - offsetY);
      isMouseDown=false;
    }

    function handleMouseMove(event) {
      let canvasOffset = canvas.getBoundingClientRect();
      let offsetX = canvasOffset.left;
      let offsetY = canvasOffset.top;

      mouseX = parseInt(event.clientX - offsetX);
      mouseY = parseInt(event.clientY - offsetY);

      // Remove the scratch padding
      if (isMouseDown) {
        ctx.beginPath();
        ctx.globalCompositeOperation = "destination-out"; // Write over a existing shape
        let radius = 8, startAngle = 0, endAngle = Math.PI*2;
        ctx.arc(lastX, lastY, radius, startAngle, endAngle);
        ctx.fill();
        lastX = mouseX;
        lastY = mouseY;
      }
    }

    canvas.addEventListener("mousedown", function(event){ handleMouseDown(event); });
    canvas.addEventListener("mousemove", function(event){ handleMouseMove(event); });
    canvas.addEventListener("mouseup", function(event){ handleMouseUp(event); });
    canvas.addEventListener("mouseout", function(event){ handleMouseOut(event); });
    document.getElementById(idMessage).removeAttribute("style");
}

// Populate message list
let message_list = []
let messages = document.getElementsByClassName("hidden-messages");
for (let i = 0; i < messages.length; i++) {
    let array = messages[i].textContent.split(',');
    if (array.length > 1) {
        message_list.push("<b>" + array[0] + "</b><br /> (" + array[1] + ")");
    } else {
        message_list.push("<b>" + array[0] + "</b>");
    }
}

generate("canvas1", "scratch-message1", message_list[0]);
scratch("canvas1", "scratch1");

generate("canvas2", "scratch-message2", message_list[1]);
scratch("canvas2", "scratch2");

generate("canvas3", "scratch-message3", message_list[2]);
scratch("canvas3", "scratch3");

generate("canvas4", "scratch-message4", message_list[3]);
scratch("canvas4", "scratch4");
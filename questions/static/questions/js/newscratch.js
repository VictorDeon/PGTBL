$(function(){

  'use strict';

  var isDrawing, lastPoint;
  var container    = document.getElementById('scratch-container'),
      canvas       = document.getElementById('scratch-canvas'),
      canvasWidth  = canvas.width,
      canvasHeight = canvas.height,
      ctx          = canvas.getContext('2d'),
      image        = new Image(),
      brush        = new Image(),
      scratched    = 35;

  image.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAzQAAAE4CAMAAAC68UYXAAAAz1BMVEUPIikPJCsQISoQIigQIikQIioQIisQIykQIyoQIysQJCsQJCwQJi4RIysRJCwRJC0RJC4RJSwRJS0RJS4RJi0RJi4RKDESJS4SJS8SJi4SJi8SJjASJy4SJy8SJzASJzESKC8SKDASKDESKjITJzETKDATKDETKTETKTITKjMTKzYUKTQUKjQUKjUUKzMUKzQUKzUULDQULDUULDYULTcVLDYVLTUVLTYVLTcVLjgVMDoWLjoWLzgWLzkWLzoWLzsWMDkWMDoWMDsWMTsXMTzUYBj+AAADdUlEQVR4Ae3YZ1KUQRiF0WsGzOJnQDE7BtHBoIjZwf2vyRXw41bZBeOcs4enbvebgwqQP0AlC6CSgwqQLxUgiwqQnxWgjAbIogKIBkQDy3wIAH8aIL+BShbAyKUBjlU0IBoQDZBfQM';
  image.onload = function() {
    ctx.drawImage(image, 0, 0);
    $('.winner-box').css({visibility: 'visible'});
  };
  brush.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAzQAAAE4CAMAAAC68UYXAAAAz1BMVEUPIikPJCsQISoQIigQIikQIioQIisQIykQIyoQIysQJCsQJCwQJi4RIysRJCwRJC0RJC4RJSwRJS0RJS4RJi0RJi4RKDESJS4SJS8SJi4SJi8SJjASJy4SJy8SJzASJzESKC8SKDASKDESKjITJzETKDATKDETKTETKTITKjMTKzYUKTQUKjQUKjUUKzMUKzQUKzUULDQULDUULDYULTcVLDYVLTUVLTYVLTcVLjgVMDoWLjoWLzgWLzkWLzoWLzsWMDkWMDoWMDsWMTsXMTzUYBj+AAADdUlEQVR4Ae3YZ1KUQRiF0WsGzOJnQDE7BtHBoIjZwf2vyRXw41bZBeOcs4enbvebgwqQP0AlC6CSgwqQLxUgiwqQnxWgjAbIogKIBkQDy3wIAH8aIL+BShbAyKUBjlU0IBoQDZBfQM';

  canvas.addEventListener('mousedown', handleMouseDown, false);
  canvas.addEventListener('touchstart', handleMouseDown, false);
  canvas.addEventListener('mousemove', handleMouseMove, false);
  canvas.addEventListener('touchmove', handleMouseMove, false);
  canvas.addEventListener('mouseup', handleMouseUp, false);
  canvas.addEventListener('touchend', handleMouseUp, false);

  function distanceBetween(point1, point2) {
    return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
  }

  function angleBetween(point1, point2) {
    return Math.atan2( point2.x - point1.x, point2.y - point1.y );
  }

  function getFilledInPixels(stride) {
    if (!stride || stride < 1) { stride = 1; }

    var pixels   = ctx.getImageData(0, 0, canvasWidth, canvasHeight),
        pdata    = pixels.data,
        l        = pdata.length,
        total    = (l / stride),
        count    = 0;

    for(var i = count = 0; i < l; i += stride) {
      if (parseInt(pdata[i]) === 0) {
        count++;
      }
    }

    return Math.round((count / total) * 100);
  }

  function getMouse(e, canvas) {
    var offsetX = 0, offsetY = 0, mx, my;

    if (canvas.offsetParent !== undefined) {
      do {
        offsetX += canvas.offsetLeft;
        offsetY += canvas.offsetTop;
      } while ((canvas = canvas.offsetParent));
    }

    if (!hasTouch()) {
        mx = e.pageX - offsetX;
        my = e.pageY - offsetY;
    } else {
        var touch = e.touches[0];
        mx = touch.pageX - offsetX;
        my = touch.pageY - offsetY;
    }

    return {x: mx, y: my};
  }

  function handlePercentage(filledInPixels,scratched) {
    filledInPixels = filledInPixels || 0;
    console.log(filledInPixels + '%');
    if (filledInPixels > scratched) {
      $('#scratch-canvas').fadeOut('slow');
    }
  }

  function handleMouseDown(e) {
    isDrawing = true;
    lastPoint = getMouse(e, canvas);
  }

  function handleMouseMove(e) {
    if (!isDrawing) { return; }

    e.preventDefault();

    var currentPoint = getMouse(e, canvas),
        dist = distanceBetween(lastPoint, currentPoint),
        angle = angleBetween(lastPoint, currentPoint),
        x, y;

    for (var i = 0; i < dist; i++) {
      x = lastPoint.x + (Math.sin(angle) * i) - 25;
      y = lastPoint.y + (Math.cos(angle) * i) - 25;
      ctx.globalCompositeOperation = 'destination-out';
      ctx.drawImage(brush, x, y);
    }

    lastPoint = currentPoint;
    handlePercentage(getFilledInPixels(32),scratched);
  }

  function handleMouseUp(e) {
    isDrawing = false;
  }

  function hasTouch() {
    return (('ontouchstart' in window) ||
        (navigator.maxTouchPoints > 0) ||
        (navigator.msMaxTouchPoints > 0));
    }

});

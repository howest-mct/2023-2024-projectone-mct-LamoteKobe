const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

let htmlButtons

const listenToUI = function () {};

const listenToButtons = function(){
  for(const i of htmlButtons){
    i.addEventListener('click', function(){
      socketio.emit('F2B_deviceState', { id: this.getAttribute('data-id'), state: this.getAttribute('data-state')})
    })
  }
}

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });

  socketio.on('B2F_deviceUpdate', function(jsonObj){
    for(const i of htmlButtons){
      if(i.getAttribute('data-id') == jsonObj.id){
        i.setAttribute('data-state', jsonObj.state)
      }
    }
  })

  socketio.on('B2F_sunpos', function(jsonObj){
    document.querySelector('.js-sun').innerHTML = jsonObj.pos
  })
};

const init = function () {
  console.info('DOM geladen');
  htmlButtons = document.querySelectorAll('.js-button');
  listenToButtons();
  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);

const lanIP = `${window.location.hostname}:5000`;
// const socketio = io(lanIP);


let htmlBtnHome, htmlBtnHistory, htmlHistory;
let chartSolar, chartGrid, chartCombined;

const listenToUI = function () {
  htmlBtnHistory.addEventListener('click', function () {
    htmlBtnHome.classList.remove('c-nav__active');
    htmlBtnHistory.classList.add('c-nav__active');
    htmlHistory.classList.remove('c-hidden');
  });
  htmlBtnHome.addEventListener('click', function () {
    htmlBtnHistory.classList.remove('c-nav__active');
    htmlBtnHome.classList.add('c-nav__active');
    htmlHistory.classList.add('c-hidden');
  });
};


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

const getCharts = function () {
  var options = {
    dataLabels: {
      enabled: true,
    },
    chart: {
      type: 'area',
      toolbar: {
        show: false,
      },
    },
    series: [
      {
        name: 'kW',
        data: ['10kWh', '20', '16kWh', 10, 5],
      },
    ],
    xaxis: {
      categories: ['15:00', '16:00', '17:00', '18:00', '19:00'],
      labels: {
        show: false,
      },
    },
    yaxis: {
      show: false,
    },
  };

  var chart = new ApexCharts(chartGrid, options);
  chart.render();
};

const init = function () {
  console.info('DOM geladen');


  htmlHistory = document.querySelector('.js-history');

  htmlBtnHome = document.querySelector('.js-btn-home');
  htmlBtnHistory = document.querySelector('.js-btn-history');

  chartSolar = document.querySelector('.js-chart-solar');
  chartGrid = document.querySelector('.js-chart-grid');
  // chartCombined = document.querySelector('.js-char-combined')


  listenToUI();
  // listenToSocket();
  getCharts();
};

document.addEventListener('DOMContentLoaded', init);

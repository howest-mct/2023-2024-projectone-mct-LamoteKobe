const lanIP = `${window.location.hostname}:5000`;
// const socketio = io(lanIP);


let htmlBtnHome, htmlBtnHistory, htmlHistory, htmlInputPeriod;
let chartSolar, chartGrid, chartCombined;

const listenToUI = function () {
  htmlBtnHistory.addEventListener('click', function () {
    htmlBtnHome.classList.remove('c-nav__active');
    htmlBtnHistory.classList.add('c-nav__active');
    htmlHistory.classList.remove('c-hidden');
    htmlHome.classList.add('c-hidden');

    console.log(lanIP)
    handleData(`http://${lanIP}/api/v1/power/2/`, showGraph)


  });
  htmlBtnHome.addEventListener('click', function () {
    htmlBtnHistory.classList.remove('c-nav__active');
    htmlBtnHome.classList.add('c-nav__active');
    htmlHistory.classList.add('c-hidden');
    htmlHome.classList.remove('c-hidden');
  });
};

const showGraph = function(jsonObj){
  let count = []
  let period = []
  let demo = []
  for(const i of jsonObj.values){
    count.push(Math.round((i.count * jsonObj.constant.constant)*1000)/1000)
    period.push(i.time)
    demo.push(0)
  }
  var options = {
    colors: ['#4A90E2'],
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
        name: 'kWh',
        data: count
      },
    ],
    xaxis: {
      categories: period,
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

  var options = {
    colors:['#4CAF50'],
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
        name: 'kWh',
        data: demo
      },
    ],
    xaxis: {
      categories: period,
      labels: {
        show: false,
      },
    },
    yaxis: {
      show: false,
    },
  };
  var chart = new ApexCharts(chartSolar, options);
  chart.render();
}


const listenToButtons = function(){
  // for(const i of htmlButtons){
  //   i.addEventListener('click', function(){
  //     socketio.emit('F2B_deviceState', { id: this.getAttribute('data-id'), state: this.getAttribute('data-state')})
  //   })
  // }
  htmlInputPeriod.addEventListener('input', function(){
    console.log(this.value)
  })
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

const getCharts = function (options) {
  


};

const init = function () {
  console.info('DOM geladen');


  htmlHistory = document.querySelector('.js-history');
  htmlHome = document.querySelector('.js-home')

  htmlBtnHome = document.querySelector('.js-btn-home');
  htmlBtnHistory = document.querySelector('.js-btn-history');

  htmlInputPeriod = document.querySelector('.js-period');

  chartSolar = document.querySelector('.js-chart-solar');
  chartGrid = document.querySelector('.js-chart-grid');
  // chartCombined = document.querySelector('.js-char-combined')


  listenToUI();
  // listenToSocket();

  listenToButtons();
};

document.addEventListener('DOMContentLoaded', init);

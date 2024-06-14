const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);


let htmlBtnHome, htmlBtnHistory, htmlHistory, htmlInputPeriod;
let htmlChartSolar, htmlChartGrid, htmlChartCombined;
let chartSolar, chartGrid, chartCombined

let htmlAppliances

let eco = []
let solar = []
let grid = []
let period = []

const listenToUI = function () {
  htmlBtnHistory.addEventListener('click', function () {
    htmlBtnHome.classList.remove('c-nav__active');
    htmlBtnHistory.classList.add('c-nav__active');
    htmlHistory.classList.remove('c-hidden');
    htmlHome.classList.add('c-hidden');

    handleData(`http://${lanIP}/api/v1/power/1/`, showGraph)

  });

  htmlBtnHome.addEventListener('click', function () {
    htmlBtnHistory.classList.remove('c-nav__active');
    htmlBtnHome.classList.add('c-nav__active');
    htmlHistory.classList.add('c-hidden');
    htmlHome.classList.remove('c-hidden');
  });

  htmlInputPeriod.addEventListener('input', function(){
    handleData(`http://${lanIP}/api/v1/power/${this.value}/`, updateGraph)
  })

  for(const buttn of htmlAppliances){
    buttn.addEventListener('click', function(){
      socketio.emit("F2B_appliance", {"appliance":this.getAttribute("data-id"), "state":this.getAttribute('data-state')})
    })
  }
};

const showAppliances = function(jsonObj){

  for(const i of jsonObj.data){
    for(const buttn of htmlAppliances){
      if(buttn.getAttribute('data-id') == i.id && i.value){
        buttn.classList.add("c-home__item__active")
        buttn.setAttribute('data-state', 1)
      }
    }
  }
}

const showGraph = function(jsonObj){
  for(const i of jsonObj.eco.values){
    eco.push(Math.round((i.count * jsonObj.eco.constant.constant)))
    period.push(i.time)
  }
  for(const i of jsonObj.grid.values){
    grid.push(Math.round((i.count * jsonObj.grid.constant.constant)))
  }
  for(const i of jsonObj.solar.values){
    solar.push(Math.round((i.count * jsonObj.solar.constant.constant)))
  }
  let combinedOptions = {
    colors:['#4CAF50', '#4A90E2', '#E3D35F'],
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
        name: 'Wh',
        data: solar
      },
      {
        name: 'Wh',
        data: grid
      },
      {
        name: 'Wh',
        data: eco
      },
    ],
    xaxis: {
      categories: period,
      labels: {
        show: false,
      },
    },
    yaxis: {
      min: 0,
      max: Math.max(...grid, ...solar, ...eco) * 1.1,
      show: false,
    },
    legend:{
      show: false
    }
  };
  chartCombined = new ApexCharts(htmlChartCombined, combinedOptions);
  chartCombined.render();
}

const updateGraph = function(jsonObj){
  eco = []
  solar = []
  grid = []
  period = []
  for(const i of jsonObj.eco.values){
    eco.push(Math.round((i.count * jsonObj.eco.constant.constant)))
    period.push(i.time)
  }
  for(const i of jsonObj.grid.values){
    grid.push(Math.round((i.count * jsonObj.grid.constant.constant)))
  }
  for(const i of jsonObj.solar.values){
    solar.push(Math.round((i.count * jsonObj.solar.constant.constant)))
  }
  chartCombined.updateOptions({
    series: [
      {
        name: 'Wh',
        data: solar
      },
      {
        name: 'Wh',
        data: grid
      },
      {
        name: 'Wh',
        data: eco
      },
    ],
    xaxis: {
      categories: period,
      labels: {
        show: false
      }
    },
    yaxis: {
      min: 0,
      max: Math.max(...grid, ...solar, ...eco) * 1.1,
      show: false
    }
  })
}

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });

  socketio.on('B2F_appliance', function(jsonObj){
    for(const buttn of htmlAppliances){
      if(buttn.getAttribute('data-id') == jsonObj.id){
        if (jsonObj.state){
          buttn.classList.add("c-home__item__active")
        }
        else{
          buttn.classList.remove("c-home__item__active")
        }
        buttn.setAttribute('data-state', Number(jsonObj.state))
      }
    }
  })


};

const init = function () {
  console.info('DOM geladen');

  htmlHistory = document.querySelector('.js-history');
  htmlHome = document.querySelector('.js-home')

  htmlBtnHome = document.querySelector('.js-btn-home');
  htmlBtnHistory = document.querySelector('.js-btn-history');

  htmlInputPeriod = document.querySelector('.js-period');

  htmlChartSolar = document.querySelector('.js-chart-solar');
  htmlChartGrid = document.querySelector('.js-chart-grid');
  htmlChartCombined = document.querySelector('.js-chart-combined')

  htmlAppliances = document.querySelectorAll('.js-appliance')

  handleData(`http://${lanIP}/api/v1/appliances/`, showAppliances)


  listenToUI();
  listenToSocket();

};

document.addEventListener('DOMContentLoaded', init);

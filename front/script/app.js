const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);


let htmlBtnHome, htmlBtnHistory, htmlHistory, htmlInputPeriod;
let htmlChartSolar, htmlChartGrid, htmlChartCombined;
let chartSolar, chartGrid, chartCombined

let powerHouse, powerEco, powerGrid, powerSolar

let htmlSettingsInput

let htmlWattage = {}

let htmlAppliances

let isInHistory = false

let eco = []
let solar = []
let house = []
let period = []
let grid = []

const listenToUI = function () {
  htmlBtnHistory.addEventListener('click', function () {
    htmlBtnHome.classList.remove('c-nav__active');
    htmlBtnHistory.classList.add('c-nav__active');
    htmlHistory.classList.remove('c-hidden');
    htmlHome.classList.add('c-hidden');

    handleData(`http://${lanIP}/api/v1/power/${htmlInputPeriod.value}/`, showGraph)
    isInHistory = true

  });

  htmlBtnHome.addEventListener('click', function () {
    htmlBtnHistory.classList.remove('c-nav__active');
    htmlBtnHome.classList.add('c-nav__active');
    htmlHistory.classList.add('c-hidden');
    htmlHome.classList.remove('c-hidden');
    isInHistory = false
    socketio.emit("F2B_get_power")

  });

  htmlBtnSettings.addEventListener('click', function(){
    window.location.href = "settings.html";
  })

  htmlInputPeriod.addEventListener('input', function(){
    handleData(`http://${lanIP}/api/v1/power/${this.value}/`, updateGraph)
  })

  for(const buttn of htmlAppliances){
    buttn.addEventListener('click', function(){
      socketio.emit("F2B_appliance", {"appliance":this.getAttribute("data-id"), "state":this.getAttribute('data-state')})
    })
  }
};

const listenToUI_settings = function(){
  htmlBtnHistory.addEventListener('click', function () {
    window.location.href = "index.html?window=history";
  });

  htmlBtnHome.addEventListener('click', function () {
    window.location.href = "index.html?window=home";
  });

  htmlSettingsInput.addEventListener('input', function(obj){
    socketio.emit("F2B_update_threshold", {"threshold": this.value})
  })
}

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

const showThreshold = function(jsonObj){
  htmlSettingsInput.value = jsonObj.threshold
}

const showGraph = function(jsonObj){
  eco = []
  solar = []
  house = []
  grid = []
  period = []
  for(const i of jsonObj.eco.values){
    eco.push(Math.round((i.count * jsonObj.eco.constant.constant)))
    period.push(i.time)
  }
  for(const i of jsonObj.house.values){
    house.push(Math.round((i.count * jsonObj.house.constant.constant)))
  }
  for(const i of jsonObj.solar.values){
    solar.push(Math.round((i.count * jsonObj.solar.constant.constant)))
  }
  for (const i in house) {
    grid[i] = house[i] - (solar[i] - eco[i])
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
        data: grid,
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
      show: false,
    },
    legend:{
      show: false
    }
  };
  chartCombined = new ApexCharts(htmlChartCombined, combinedOptions);
  chartCombined.render();

  sumSolar = 0
  for (const i of solar) {
    sumSolar += i;
  }
  htmlWattage["solar"].innerHTML = `${sumSolar} Wh`
  sumHouse = 0
  for (const i of house) {
    sumHouse += i;
  }
  htmlWattage["house"].innerHTML = `${sumHouse} Wh`
  sumEco = 0
  for (const i of eco) {
    sumEco += i;
  }
  htmlWattage["eco"].innerHTML = `${sumEco} Wh`
  sumGrid = sumHouse - (sumSolar-sumEco)
  htmlWattage["grid"].innerHTML = `${sumGrid} Wh`
}

const updateGraph = function(jsonObj){
  eco = []
  solar = []
  house = []
  period = []
  grid = []
  for(const i of jsonObj.eco.values){
    eco.push(Math.round((i.count * jsonObj.eco.constant.constant)))
    period.push(i.time)
  }
  for(const i of jsonObj.house.values){
    house.push(Math.round((i.count * jsonObj.house.constant.constant)))
  }
  for(const i of jsonObj.solar.values){
    solar.push(Math.round((i.count * jsonObj.solar.constant.constant)))
  }
  for (const i in house) {
    grid[i] = house[i] - (solar[i] - eco[i])
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
      show: false
    }
  })

  sumSolar = 0
  for (const i of solar) {
    sumSolar += i;
  }
  htmlWattage["solar"].innerHTML = `${sumSolar} Wh`
  sumHouse = 0
  for (const i of house) {
    sumHouse += i;
  }
  htmlWattage["house"].innerHTML = `${sumHouse} Wh`
  sumEco = 0
  for (const i of eco) {
    sumEco += i;
  }
  htmlWattage["eco"].innerHTML = `${sumEco} Wh`
  sumGrid = sumHouse - (sumSolar-sumEco)
  htmlWattage["grid"].innerHTML = `${sumGrid} Wh`
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

  socketio.on('B2F_update_power', function(jsonObj){
    if (!isInHistory){
      htmlWattage[jsonObj.name].innerHTML = `${Math.round(jsonObj.power)} W`
    }

    if(jsonObj.name == "solar" && jsonObj.power == 0){
      powerSolar.classList.remove("c-power__solar")
    }
    else if(jsonObj.name == "solar"){
      powerSolar.classList.add("c-power__solar")
    }

    
    if(jsonObj.name == "eco" && jsonObj.power == 0){
      powerEco.classList.remove("c-power__eco")
    }
    else if(jsonObj.name == "eco"){
      powerEco.classList.add("c-power__eco")
    }


    if(jsonObj.name == "house" && jsonObj.power == 0){
      powerHouse.classList.remove("c-power__house")
    }
    else if(jsonObj.name == "house"){
      powerHouse.classList.add("c-power__house")
    }


    if(jsonObj.name == "grid" && jsonObj.power == 0){
      powerGrid.classList.remove("c-power__grid")
    }
    else if(jsonObj.name == "grid" && jsonObj.power < 0){
      powerGrid.classList.add("c-power__grid-reverse")
    }
    else if(jsonObj.name == "grid"){
      powerGrid.classList.remove("c-power__grid-reverse")
      powerGrid.classList.add("c-power__grid")
    }


  })


};

const init = function () {
  console.info('DOM geladen');

  if (document.querySelector('.js-main')){
    htmlHistory = document.querySelector('.js-history');
    htmlHome = document.querySelector('.js-home')

    htmlBtnHome = document.querySelector('.js-btn-home');
    htmlBtnHistory = document.querySelector('.js-btn-history');

    htmlBtnSettings = document.querySelector('.js-settings-button')

    htmlInputPeriod = document.querySelector('.js-period');

    htmlChartSolar = document.querySelector('.js-chart-solar');
    htmlChartGrid = document.querySelector('.js-chart-grid');
    htmlChartCombined = document.querySelector('.js-chart-combined')

    htmlWattage.eco = document.querySelector('.js-wattage-eco')
    htmlWattage.grid = document.querySelector('.js-wattage-grid')
    htmlWattage.solar = document.querySelector('.js-wattage-solar')
    htmlWattage.house = document.querySelector('.js-wattage-house')

    powerHouse = document.querySelector('.js-power__house')
    powerEco = document.querySelector('.js-power__eco')
    powerGrid = document.querySelector('.js-power__grid')
    powerSolar = document.querySelector('.js-power__solar')

    htmlAppliances = document.querySelectorAll('.js-appliance')

    handleData(`http://${lanIP}/api/v1/appliances/`, showAppliances)
    socketio.emit("F2B_get_power")

    if(new URLSearchParams(window.location.search).get('window') === "history"){
      htmlBtnHome.classList.remove('c-nav__active');
      htmlBtnHistory.classList.add('c-nav__active');
      htmlHistory.classList.remove('c-hidden');
      htmlHome.classList.add('c-hidden');
  
      handleData(`http://${lanIP}/api/v1/power/${htmlInputPeriod.value}/`, showGraph)
      isInHistory = true
    }


    listenToUI();
    listenToSocket();
  }

  if (document.querySelector('.js-settings')){
    htmlBtnHome = document.querySelector('.js-btn-home');
    htmlBtnHistory = document.querySelector('.js-btn-history');
    htmlSettingsInput = document.querySelector('.js-settings-input')
    handleData(`http://${lanIP}/api/v1/threshold/`, showThreshold)
    listenToUI_settings()
  }


};

document.addEventListener('DOMContentLoaded', init);

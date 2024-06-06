const lanIP = `${window.location.hostname}:5000`;
// const socketio = io(lanIP);

const listenToUI = function () {};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
};

const init = function () {
  console.info('DOM geladen');
  // listenToUI();
  // listenToSocket();
  // document.querySelectorAll('.c-nav__item').forEach((item) => {
  //   item.addEventListener('click', function () {
  //     document.querySelector('.c-nav__active').classList.remove('c-nav__active');
  //     this.classList.add('c-nav__active');
  //   });
  // });
  console.log('DOM loaded');

  // Double-check that the element exists
  var chartElement = document.querySelector('#chart');
  if (!chartElement) {
    console.error('Chart element not found');
    return;
  }

  // Options for the chart
  var options = {
    dataLabels: {
      enabled: false,
    },
    chart: {
      type: 'area',
      toolbar: {
        show: false,
      },
    },
    series: [
      {
        name: 'Power',
        data: ['10kWh', '20', '16kWh', 10, 5],
      },
    ],
    xaxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      show: false,
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      show: false,
    },
  };

  // Initialize and render the chart
  var chart = new ApexCharts(chartElement, options);
  chart.render().catch(function (e) {
    console.error('Error rendering chart:', e);
  });
  var chart = new ApexCharts(document.querySelector('#test'), options);
  chart.render().catch(function (e) {
    console.error('Error rendering chart:', e);
  });
};

document.addEventListener('DOMContentLoaded', init);

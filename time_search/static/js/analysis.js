// グラフ作成の手順を定義
const loadCharts = function (xlabels, label, data, dep_stop_name, arr_stop_name) {
  const chartDataSet = {
    type: 'line',
    data: {
      labels: xlabels,
      datasets: [{
        label: label,
        data: data,
        backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--color-aiueo'),
        borderColor: getComputedStyle(document.documentElement).getPropertyValue('--color-sub')
      }]
    },
    options: {}
  };

  const div = document.createElement('div');

  div.classList.add('graph-frame');

  const p = document.createElement('p');
  const text = document.createTextNode(dep_stop_name + '  →  ' + arr_stop_name);
  p.appendChild(text);

  div.appendChild(p);


  const ctx = document.createElement('canvas');
  div.appendChild(ctx)
  new Chart(ctx, chartDataSet);

  document.getElementById('chart-area').appendChild(div);

};

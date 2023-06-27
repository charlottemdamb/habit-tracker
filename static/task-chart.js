'use strict';
const chartForm = document.querySelector("#task-form")

console.log(chartForm)

let weeklyChart
let monthlyChart
let yearlyChart
let allChart

const ctxw = document.getElementById('weekChart');
const ctxm = document.getElementById('monthChart');
const ctxy = document.getElementById('yearChart');
const ctxa = document.getElementById('allTimeChart');

chartForm.addEventListener('submit', taskChartInputs)


function taskChartInputs(evt) {
  evt.preventDefault()

  const formInputs = {
    task: document.querySelector('#task-choice').value
  };
  console.log(formInputs)
  fetch('/task-data', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => { return response.json() })
    .then((responseJSON) => {
      const wDatesList = []
      const wQtyList = []
      let wTitle
      for (let item of responseJSON.week) {
        wQtyList.push(item.qty)
        wDatesList.push(item.date)
        if(item.title)
          wTitle = item.title
      }
      if (weeklyChart !== undefined){
        weeklyChart.destroy()
      }
      weeklyChart = createLineChart(wDatesList, wQtyList, wTitle, ctxw, 'lightgreen', 'lightgreen')
      const mDatesList = []
      const mQtyList = []
      let mTitle
      for (let item of responseJSON.month) {
        mQtyList.push(item.qty)
        mDatesList.push(item.date)
        if(item.title)
          mTitle = item.title
      }
      if (monthlyChart !== undefined){
        monthlyChart.destroy()
      }
      monthlyChart = createLineChart(mDatesList, mQtyList, mTitle, ctxm, 'pink', 'pink')
      const yDatesList = []
      const yQtyList = []
      let yTitle
      for (let item of responseJSON.year) {
        yQtyList.push(item.qty)
        yDatesList.push(item.date)
        if(item.title)
          yTitle = item.title
      }
      if (yearlyChart !== undefined){
        yearlyChart.destroy()
      }
      yearlyChart = createLineChart(yDatesList, yQtyList, yTitle, ctxy, 'lightblue', 'lightblue')

      let aDatesList = []
      let aQtyList = []
      let aTitleList = []
      console.log(responseJSON)
      
      for (let idx in responseJSON.all) {
        let datesList = []
        let qtyList = []
        let titleSet 
        for (let item of responseJSON.all[idx]){
          qtyList.push(item.qty)
          datesList.push(item.date)
          if (item.title){
          titleSet = item.title
          }
        }
        aDatesList.push(datesList)
        aQtyList.push(qtyList)
        aTitleList.push(titleSet)
      }
      if (allChart !== undefined){
        allChart.destroy()
      }
      allChart = createAllChart(aDatesList, aQtyList, aTitleList, ctxa)
    });

}

// const catChartForm = document.querySelector("#cat-form")

// console.log(chartForm)

// let weeklyCatChart
// let monthlyCatChart
// let yearlyCatChart

// const ctxcw = document.getElementById('weekCatChart');
// const ctxcm = document.getElementById('monthCatChart');
// const ctxcy = document.getElementById('yearCatChart');

// catChartForm.addEventListener('submit', catChartInputs)


// function catChartInputs(evt) {
//   evt.preventDefault()

//   const formInputs = {
//     category: document.querySelector('#cat-choice').value
//   };
//   console.log(formInputs)
//   fetch('/cat-data', {
//     method: 'POST',
//     body: JSON.stringify(formInputs),
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   })
//     .then((response) => { return response.json() })
//     .then((responseJSON) => {
//       const wDatesList = []
//       const wQtyList = []
//       const wTaskList = []
//       for (let item of responseJSON.week) {
//         wQtyList.push(item.qty)
//         wDatesList.push(item.date)
//         wTaskList.push(item.title)
//       }
//       if (weeklyCatChart !== undefined){
//         weeklyCatChart.destroy()
//       }
//       weeklyCatChart = createChart(wDatesList, wQtyList, ctxcw, 'green')
//       const mDatesList = []
//       const mQtyList = []
//       const mTaskList = []
//       for (let item of responseJSON.month) {
//         mQtyList.push(item.qty)
//         mDatesList.push(item.date)
//         mTaskList.push(item.title)
//       }
//       if (monthlyChart !== undefined){
//         monthlyChart.destroy()
//       }
//       monthlyCatChart = createChart(mDatesList, mQtyList, ctxcm, 'pink', 'pink')
//       const yDatesList = []
//       const yQtyList = []
//       const yTaskList = []
//       for (let item of responseJSON.year) {
//         yQtyList.push(item.qty)
//         yDatesList.push(item.date)
//         yTaskList.push(item.title)
//       }
//       if (yearlyChart !== undefined){
//         yearlyChart.destroy()
//       }
//       yearlyCatChart = createLineChart(yDatesList, yQtyList, ctxcy, 'blue', 'blue')
//     });

// }


function createAllChart(date, qty, title, ctx) {
  const colors = ['blue','yellow','lightgreen','red','pink','purple','orange'];
  console.log(qty)

  const newChart = new Chart(ctx, {

    type: 'line',
    data: {
      labels: date[0],
      datasets: qty.map((list, idx)=> {
        return {
            label: title[idx],
            data: list,
            borderWidth: 3,
            borderColor: colors[idx%colors.length],
            backgroundColor: colors[idx %colors.length]
          }
      })
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  return newChart
}


function createLineChart(date, qty, title, ctx, color, bcolor) {
  
  const newChart = new Chart(ctx, {

    type: 'line',
    data: {
      labels: date,
      datasets: [{
        label: title,
        data: qty,
        borderWidth: 3,
        borderColor: bcolor,
        backgroundColor: color
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 20
        }
      }
    }
  });
  return newChart
}
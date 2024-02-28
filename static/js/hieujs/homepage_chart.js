// create a chart line for homepage with id canvas is "lineChartMonth"
function createLineChartMonth(dataIncome, dataExpenses) {
  var ctx = document.getElementById("lineChartMonth").getContext("2d");
  var lineChartMonth = new Chart(ctx, {
    type: "line",
    data: {
      labels: [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
      ],
      datasets: [
        {
          label: "Thu Nhập",
          data: dataIncome,
          backgroundColor: "rgba(83, 109, 220, 0.2)",
          borderColor: "rgba(83, 109, 220, 1)",
          pointStyle: "circle",
          borderWidth: 1,
          pointStyle: "circle",
        },
        {
          label: "Chi Tiêu",
          data: dataExpenses,
          backgroundColor: "rgba(82, 205, 255, 0.2)",
          borderColor: "rgba(82, 205, 255, 1)",
          borderWidth: 1,
          pointStyle: "circle",
        },
      ],
    },
    options: {
      aspectRatio: 3,
      scales: {
        yAxes: [
          {
            gridLines: {
              display: true,
              lineWidth: 0.5, // Adjust this value as needed
            },
          },
        ],
        xAxes: [
          {
            gridLines: {
              display: false,
            },
          },
        ],
      },
    },
  });
}
function createLineChartYear(dataIncome, dataExpenses) {
  var ctx = document.getElementById("lineChartYear").getContext("2d");
  var lineChartMonth = new Chart(ctx, {
    type: "line",
    data: {
      labels: [
        "Tháng 1",
        "Tháng 2",
        "Tháng 3",
        "Tháng 4",
        "Tháng 5",
        "Tháng 6",
        "Tháng 7",
        "Tháng 8",
        "Tháng 9",
        "Tháng 10",
        "Tháng 11",
        "Tháng 12",
      ],
      datasets: [
        {
          label: "Thu Nhập",
          data: dataIncome,
          backgroundColor: "rgba(83, 109, 220, 0.2)",
          borderColor: "rgba(83, 109, 220, 1)",
          pointStyle: "circle",
          borderWidth: 1,
          pointStyle: "circle",
        },
        {
          label: "Chi tiêu",
          data: dataExpenses,
          backgroundColor: "rgba(82, 205, 255, 0.2)",
          borderColor: "rgba(82, 205, 255, 1)",
          borderWidth: 1,
          pointStyle: "circle",
        },
      ],
    },
    options: {
      aspectRatio: 3,
      scales: {
        yAxes: [
          {
            gridLines: {
              display: true,
              lineWidth: 0.5, // Adjust this value as needed
            },
          },
        ],
        xAxes: [
          {
            gridLines: {
              display: false,
            },
          },
        ],
      },
    },
  });
}
document.addEventListener("DOMContentLoaded", function () {
  var username = document.getElementById("hp_username").value;
  fetch(`/get_data?p=${username}`)
    .then((response) => response.json())
    .then((data) => {
      createLineChartMonth(
        data.data_income_this_month,
        data.data_expense_this_month
      );
      createLineChartYear(
        data.data_income_this_year,
        data.data_expense_this_year
      );
    });
  // createLineChartMonth();
  // createLineChartYear();
});

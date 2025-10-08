// Variable global para los gráficos
let lineChart, barChart, doughnutChart;

// Cargar y renderizar datos
async function cargarDatos() {
  try {
    const start = document.getElementById("start").value;
    const end = document.getElementById("end").value;
    let url = "/metrics/";
    if (start && end) url += `?start=${start}&end=${end}`;

    const response = await fetch(url);
    const data = await response.json();

    if (data.error) {
      alert("Error: " + data.error);
      return;
    }

    // Actualizar resumen
    document.getElementById("created").textContent = data.created || 0;
    document.getElementById("confirmed").textContent = data.confirmed || 0;
    document.getElementById("cancelled").textContent = data.cancelled || 0;

    const labels = ["Creadas", "Confirmadas", "Canceladas"];
    const valores = [data.created || 0, data.confirmed || 0, data.cancelled || 0];

    // Destruir gráficos previos
    [lineChart, barChart, doughnutChart].forEach((g) => g?.destroy());

    // Colores del modo actual
    const textColor = getComputedStyle(document.body)
      .getPropertyValue("--text-color")
      .trim();

    // Opciones comunes
    const commonOptions = {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: "rgba(128, 128, 128, 0.3)" },
          ticks: { color: textColor },
        },
        x: {
          grid: { color: "rgba(128, 128, 128, 0.3)" },
          ticks: { color: textColor },
        },
      },
      plugins: {
        legend: { labels: { color: textColor } },
      },
    };

    // 📈 Line Chart
    lineChart = new Chart(document.getElementById("lineChart"), {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Tendencia de citas",
            data: valores,
            borderColor: "#2563eb",
            backgroundColor: "rgba(37,99,235,0.2)",
            tension: 0.4,
            fill: true,
            pointRadius: 6,
            pointBackgroundColor: "#2563eb",
          },
        ],
      },
      options: commonOptions,
    });

    // 📊 Bar Chart
    barChart = new Chart(document.getElementById("barChart"), {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Cantidad de citas",
            data: valores,
            backgroundColor: ["#3b82f6", "#22c55e", "#ef4444"],
            borderRadius: 8,
          },
        ],
      },
      options: commonOptions,
    });

    // 🍩 Doughnut Chart
    doughnutChart = new Chart(document.getElementById("doughnutChart"), {
      type: "doughnut",
      data: {
        labels,
        datasets: [
          {
            label: "Distribución",
            data: valores,
            backgroundColor: ["#3b82f6", "#22c55e", "#ef4444"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: textColor },
          },
        },
      },
    });
  } catch (error) {
    console.error("Error al cargar métricas:", error);
    alert("No se pudieron cargar los datos.");
  }
}

// 🌙 Alternar modo oscuro/claro
function toggleDarkMode() {
  const body = document.body;
  const isDarkMode = body.classList.contains("dark-mode");
  const newMode = isDarkMode ? "light-mode" : "dark-mode";
  body.className = newMode;

  document.getElementById("mode-switch").textContent =
    newMode === "dark-mode" ? "🌙" : "☀️";

  localStorage.setItem("theme", newMode);

  // Re-renderizar los gráficos con el nuevo tema
  cargarDatos();
}

// 🚀 Inicialización
function initDashboard() {
  const savedTheme = localStorage.getItem("theme") || "light-mode";
  document.body.className = savedTheme;
  document.getElementById("mode-switch").textContent =
    savedTheme === "dark-mode" ? "🌙" : "☀️";

  document.getElementById("mode-switch").addEventListener("click", toggleDarkMode);
  cargarDatos();
}

document.addEventListener("DOMContentLoaded", initDashboard);

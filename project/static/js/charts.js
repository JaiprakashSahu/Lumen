// project/static/js/charts.js

let donutChartInstance = null;

/**
 * Safely creates or recreates donut chart
 */
function renderDonutChart(data) {
    const canvas = document.getElementById("donutChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    // 🔥 CRITICAL FIX
    if (donutChartInstance) {
        donutChartInstance.destroy();
        donutChartInstance = null;
    }

    donutChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
}


/**
 * Initialize charts only once
 */
function initDashboardCharts() {
    const canvas = document.getElementById("donutChart");
    if (!canvas) return;

    // Example data — replace with your real data
    const initialData = {
        labels: ["Shopping", "Food", "Other"],
        datasets: [{
            data: [100, 0, 0],
            backgroundColor: ["#3B82F6", "#10B981", "#F59E0B"]
        }]
    };

    renderDonutChart(initialData);
}


// Ensure it runs once only
document.addEventListener("DOMContentLoaded", function () {
    initDashboardCharts();

    // Refresh button handler — always goes through renderDonutChart()
    document.getElementById("refreshBtn")?.addEventListener("click", function () {
        const newData = {
            labels: ["Shopping", "Food", "Other"],
            datasets: [{
                data: [120, 30, 50],
                backgroundColor: ["#3B82F6", "#10B981", "#F59E0B"]
            }]
        };

        renderDonutChart(newData);
    });
});
document.addEventListener("DOMContentLoaded", () => {

    let cpuChart, ramChart, diskChart;





    function getLatestPerHostname(list) {
        const latest = {};
    
        list.forEach(item => {
            const host = item.Hostname;
            const time = new Date(item.Timestamp).getTime();
    
            if (!latest[host] || time > latest[host]._time) {
                latest[host] = { ...item, _time: time };
            }
        });
    
        return Object.values(latest).map(({ _time, ...rest }) => rest);
    }

    

    function loadDashboard() {
    fetch("/api/dashboard-summary")
        .then(res => res.json())
        .then(data => {
            renderCPU(getLatestPerHostname(data.cpu));
            renderRAM(getLatestPerHostname(data.ram));
            renderDisk(getLatestPerHostname(data.disk));
            updateFooter(data.lastUpdated);
        })
        .catch(err => console.error("Dashboard load error:", err));
    }


    function renderCPU(list) {
        if (cpuChart) cpuChart.destroy();
        cpuChart = new Chart(document.getElementById("cpuGraph"), {
            type: "bar",
            data: {
                labels: list.map(x => x.Hostname),
                datasets: [{ label: "CPU (%)", data: list.map(x => x.cpu), backgroundColor: "#ff4444" }]
            },
            options: {
                
                x: {
                ticks: {
                    font: { size: 17 },
                    padding: 10
                }
            }
        }
        });
    }

    function renderRAM(list) {
        if (ramChart) ramChart.destroy();
        ramChart = new Chart(document.getElementById("ramGraph"), {
            type: "bar",
            data: {
                labels: list.map(x => x.Hostname),
                datasets: [{ label: "RAM (%)", data: list.map(x => x.ram), backgroundColor: "#ff8800" }]
            },
            options: chartOptions()
        });
    }

    function renderDisk(list) {
        if (diskChart) diskChart.destroy();
        diskChart = new Chart(document.getElementById("diskGraph"), {
            type: "bar",
            data: {
                labels: list.map(x => x.Hostname),
                datasets: [{ label: "Disk (%)", data: list.map(x => x.disk), backgroundColor: "#4da6ff" }]
            },
            options: chartOptions()
        });
    }

    function chartOptions() {
        return {
            responsive: true,
            animation: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, max: 100 } }
        };
    }

    function updateFooter(timestamp) {
        const el = document.getElementById("last-updated");
        if (el && timestamp) {
            el.innerText = "Last Updated On: " + new Date(timestamp).toLocaleString();
        }
    }

    loadDashboard();
    // Auto-refresh every 30 seconds
    setInterval(loadDashboard, 30000);
});

Chart.defaults.animation = false;

document.addEventListener("DOMContentLoaded", () => {

    let lineChartInstance = null;
    let systemsData = [];

    // COLOR LOGIC
    function getColor(value) {
        if (value >= 80) return "#DC0000";
        if (value >= 60) return "#ffb400";
        return "#88b04b";
    }

    // GET LATEST PER HOSTNAME
    function getLatestPerHostname(systems) {
        const latestMap = {};
        systems.forEach(sys => {
            const host = sys.Hostname;
            const time = new Date(sys.Timestamp).getTime();
            if (!latestMap[host] || time > latestMap[host]._time) {
                latestMap[host] = { ...sys, _time: time };
            }
        });
        return Object.values(latestMap).map(({ _time, ...rest }) => rest);
    }

    // LOAD SYSTEMS
    function loadSystems() {
        fetch("/api/utilization/latest")
            .then(res => res.json())
            .then(data => {
                systemsData = getLatestPerHostname(data);
                generateCards(systemsData);
            })
            .catch(err => console.error("Load failed:", err));
    }

    // AUTO-REFRESH EVERY 30 SECONDS
    setInterval(loadSystems, 30000); // 30s
    loadSystems();

    // CREATE DASHBOARD CARDS
    function generateCards(systems) {
        const grid = document.querySelector(".monitoring-grid");
        grid.innerHTML = "";

        // Sort by critical usage
        systems.sort((a, b) => Math.max(b.CPU, b.RAM, b.Disk) - Math.max(a.CPU, a.RAM, a.Disk));

        systems.forEach((sys, index) => {
            const card = document.createElement("div");
            card.className = "system-card";
            card.innerHTML = `
                <div class="card-click-overlay" data-host="${sys.Hostname}"></div>
                <h3>${sys.Hostname}</h3>
                <canvas id="chart${index}"></canvas>
            `;
            grid.appendChild(card);

            const ctx = document.getElementById(`chart${index}`).getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["CPU", "RAM", "DISK"],
                    datasets: [{
                        data: [sys.CPU, sys.RAM, sys.Disk],
                        backgroundColor: [
                            getColor(sys.CPU),
                            getColor(sys.RAM),
                            getColor(sys.Disk)
                        ],
                        barThickness: 55
                    }]
                },
                options: {
                    responsive: true,
                    interaction: { mode: "nearest", intersect: true },
                    plugins: {
                        legend: { display: false },
                        tooltip: { callbacks: { label: ctx => `${ctx.parsed.y}%` } }
                    },
                    scales: { y: { beginAtZero: true, max: 100, ticks: { callback: v => v + "%" } } }
                }
            });
        });
    }

    // OPEN POPUP
    function openPopup(hostname) {
        const hostData = systemsData.find(h => h.Hostname === hostname);
        if (!hostData) return;

        document.getElementById("popup-hostname").innerText = hostname;
        document.getElementById("popup").classList.add("show");
        document.getElementById("overlay").classList.add("show");

        loadHistory(hostname);
        loadPeripherals(hostname);
    }

    // LOAD HISTORY
    function loadHistory(hostname) {
        fetch(`/api/utilization/history/${hostname}`)
            .then(res => res.json())
            .then(history => renderLineChart(history))
            .catch(err => console.error("History error:", err));
    }

    function renderLineChart(history) {
        const ctx = document.getElementById("lineChart").getContext("2d");
        if (lineChartInstance) lineChartInstance.destroy();

        lineChartInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels: history.labels,
                datasets: [
                    { label: "CPU", data: history.cpu, borderColor: "#0913a0", tension: 0.3, fill: false },
                    { label: "RAM", data: history.ram, borderColor: "#e6004c", tension: 0.3, fill: false },
                    { label: "DISK", data: history.disk, borderColor: "#0dc416", tension: 0.3, fill: false }
                ]
            },
            options: {
                responsive: true,
                interaction: { mode: "nearest", intersect: false },
                scales: { y: { beginAtZero: true, max: 100, ticks: { callback: v => v + "%" } } }
            }
        });
    }

    // LOAD PERIPHERALS
    function loadPeripherals(hostname) {
        fetch(`/api/utilization/peripherals/${hostname}`)
            .then(res => res.json())
            .then(items => {
                document.getElementById("peripherals-list").innerHTML =
                    items.map(i => `<li>${i}</li>`).join("");
            })
            .catch(err => console.error("Peripheral error:", err));
    }

    // CLOSE POPUP
    function closePopup() {
        document.getElementById("popup").classList.remove("show");
        document.getElementById("overlay").classList.remove("show");
        if (lineChartInstance) lineChartInstance.destroy();
    }

    // EVENTS
    document.querySelector(".monitoring-grid").addEventListener("click", e => {
        const card = e.target.closest(".system-card");
        if (!card) return;
        const host = card.querySelector(".card-click-overlay").dataset.host;
        openPopup(host);
    });
    

    document.querySelector(".close-popup").addEventListener("click", closePopup);
    document.getElementById("overlay").addEventListener("click", closePopup);

});

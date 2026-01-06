document.addEventListener("DOMContentLoaded", () => {

    function getLatestPerHostname(rows) {
        const latest = {};
        rows.forEach(r => {
            const host = r.hostname;
            const time = new Date(r.timestamp).getTime();
            if (!latest[host] || time > latest[host]._time) {
                latest[host] = { ...r, _time: time };
            }
        });
        return Object.values(latest).map(({ _time, ...rest }) => rest);
    }

    let barChart = null;
    let lineChart = null;

    const barCanvas = document.getElementById("barChart");
    const lineCanvas = document.getElementById("lineChart");

    function getColor(v) {
        if (v >= 80) return "#DC0000";
        if (v >= 60) return "#ffb400";
        return "#88b04b";
    }

    function populateTable(rows) {
        const tbody = document.querySelector("#systemTable tbody");
        tbody.innerHTML = "";
        rows.sort((a, b) => {
            const maxA = Math.max(a.cpu, a.ram, a.disk);
            const maxB = Math.max(b.cpu, b.ram, b.disk);
            return maxB - maxA; // highest → lowest
        });
        
        rows.forEach(r => {
            const tr = document.createElement("tr");
            if (r.cpu >= 80 || r.ram >= 80 || r.disk >= 80) tr.classList.add("high-usage");
            tr.innerHTML = `
                <td><a href="#" class="hostLink">${r.hostname}</a></td>
                <td>${r.cpu}</td>
                <td>${r.ram}</td>
                <td>${r.disk}</td>
            `;
            tbody.appendChild(tr);
        });
    }
    function renderBar(system) {
        if (barChart) barChart.destroy();
    
        barChart = new Chart(barCanvas, {
            type: "bar",
            data: {
                labels: ["CPU", "RAM", "DISK"],
                datasets: [{
                    data: [system.cpu, system.ram, system.disk],
                    backgroundColor: [
                        getColor(system.cpu),
                        getColor(system.ram),
                        getColor(system.disk)
                    ],
                    barThickness: 70,          
                    maxBarThickness: 100,      
                    categoryPercentage: 0.6,   
                    barPercentage: 0.7         
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        ticks: {
                            font: { size: 17 },
                            padding: 10
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: v => v + "%"
                        }
                    }
                }
            }
        });
    }
    


    function renderLine(hostname) {
        fetch(`/api/host-history/${hostname}`)
            .then(r => r.json())
            .then(days => {
                if (lineChart) lineChart.destroy();
                lineChart = new Chart(lineCanvas, {
                    type: "line",
                    data: {
                        labels: days.map(d => d.day),
                        datasets: [
                            { label: "CPU", data: days.map(d => d.cpu), borderColor: "#0913a0", tension: 0.3 },
                            { label: "RAM", data: days.map(d => d.ram), borderColor: "#f54242", tension: 0.3 },
                            { label: "Disk", data: days.map(d => d.disk), borderColor: "#0dc416", tension: 0.3 }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100 } } }
                });
            });
    }

    function render(system) {
        document.getElementById("graphTitle").innerText = system.hostname;
        renderBar(system);
        renderLine(system.hostname);
        document.getElementById("peripheralDetails").innerHTML = `
            <p><b>Monitor:</b> ${system.monitorVendor} | ${system.monitorModel}</p>
            <p><b>Mouse:</b> ${system.mouseVendor} | ${system.mouseModel}</p>
            <p><b>Keyboard:</b> ${system.keyboardVendor} | ${system.keyboardModel}</p>
        `;
    }

    function loadTableData() {
        fetch("/api/table-latest")
            .then(r => r.json())
            .then(rows => {
                const latestRows = getLatestPerHostname(rows);
                populateTable(latestRows);
                const first = latestRows.find(r => r.cpu >= 80 || r.ram >= 80 || r.disk >= 80) || latestRows[0];
                if (first) render(first);
                document.querySelectorAll(".hostLink").forEach(link => {
                    link.onclick = e => {
                        e.preventDefault();
                        const host = link.innerText.trim();
                        render(latestRows.find(r => r.hostname === host));
                    };
                });
            });
    }

    // Initial load
    loadTableData();

    // Auto-refresh every 30 seconds
    setInterval(loadTableData, 30000);

});

// Shared helper functions

export function getLatestPerHostname(rows, timestampKey="timestamp") {
    const latestMap = {};
    rows.forEach(r => {
        const host = r.hostname;
        const time = new Date(r[timestampKey]).getTime();
        if (!latestMap[host] || time > latestMap[host]._time) {
            latestMap[host] = { ...r, _time: time };
        }
    });
    return Object.values(latestMap).map(({ _time, ...rest }) => rest);
}

export function getColor(value) {
    if (value >= 80) return "#DC0000";
    if (value >= 60) return "#ffb400";
    return "#88b04b";
}

export function renderBarChart(ctx, labels, data, colors) {
    return new Chart(ctx, {
        type: "bar",
        data: { labels, datasets: [{ data, backgroundColor: colors }] },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, max: 100 } },
            plugins: { legend: { display: false } }
        }
    });
}

export function renderLineChart(ctx, labels, datasets) {
    return new Chart(ctx, {
        type: "line",
        data: { labels, datasets },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });
}

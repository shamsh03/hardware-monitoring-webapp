// footer.js — Universal Latest Timestamp

function updateFooter(timestamp) {
    const footerEl = document.getElementById("last-updated");
    if (footerEl) {
        footerEl.innerText = timestamp
            ? "Last Updated On: " + new Date(timestamp).toLocaleString()
            : "No data available";
    }
}

function loadFooter() {
    // Choose API that gives latest timestamp efficiently
    // /api/utilization/latest returns latest per host
    fetch("/api/utilization/latest")
        .then(res => res.json())
        .then(rows => {
            if (!rows || rows.length === 0) {
                updateFooter(null);
                return;
            }

            // Get the maximum timestamp from all rows
            const latestTs = rows.reduce((max, row) => {
                const t = new Date(row.Timestamp || row.timestamp).getTime();
                return t > max ? t : max;
            }, 0);

            updateFooter(new Date(latestTs).toISOString());
        })
        .catch(err => {
            console.error("Footer load error:", err);
            updateFooter(null);
        });
}

// Load on DOM ready
document.addEventListener("DOMContentLoaded", loadFooter);

// Optional: Auto-refresh footer every 30 seconds
setInterval(loadFooter, 30000);

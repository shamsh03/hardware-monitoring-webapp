async function initCollectionToggle() {

    const btn = document.getElementById("toggleBtn");
    if (!btn) return;

    async function updateButton() {
        try {
            const res = await fetch("/api/collection/status");
            const data = await res.json();

            btn.textContent = data.collectionEnabled
                ? "🟢 Collection ON"
                : "🔴 Collection OFF";
        } catch (err) {
            console.error("Status fetch failed", err);
        }
    }

    btn.onclick = async () => {
        try {
            const res = await fetch("/api/collection/toggle", { method: "POST" });
            const data = await res.json();

            btn.textContent = data.collectionEnabled
                ? "🟢 Collection ON"
                : "🔴 Collection OFF";
        } catch (err) {
            console.error("Toggle failed", err);
        }
    };

    updateButton();
}

// run AFTER header is inserted
document.addEventListener("DOMContentLoaded", initCollectionToggle);

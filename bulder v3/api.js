const API = {
    async get(path) {
        const r = await fetch(path);
        return r.json();
    },

    async post(path, data) {
        return fetch(path, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });
    },

    async del(path) {
        return fetch(path, { method: "DELETE" });
    }
};
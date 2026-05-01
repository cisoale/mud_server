const API_KEY = "dev123";

const API = {
    async get(url) {
        const r = await fetch(url);
        return r.json();
    },

    async post(url, data) {
        return fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": API_KEY
            },
            body: JSON.stringify(data)
        });
    },

    async del(url) {
        return fetch(url, {
            method: "DELETE",
            headers: {
                "x-api-key": API_KEY
            }
        });
    }
};
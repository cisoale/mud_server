const API = {
    get: async (url) => {
        const r = await fetch(url);
        return await r.json();
    },
    post: async (url, data) => {
        await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
    }
};
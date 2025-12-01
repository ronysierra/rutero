import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'https://literate-fortnight-9j5w9xr55q53wvp-8000.app.github.dev';

const client = axios.create({
    baseURL: BASE_URL,
});

client.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Token ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default client;
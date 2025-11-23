import axios from 'axios';

// 1. Define la URL base de tu API
// IMPORTANTE: Cambia esto por TU URL de Codespaces (la que usaste en Swagger)
// Ejemplo: https://literate-fortnight-xxxx-8000.app.github.dev
const BASE_URL = 'https://literate-fortnight-9j5w9xr55q53wvp-8000.app.github.dev'; 

const client = axios.create({
    baseURL: BASE_URL,
});

// 2. Interceptor: Antes de cada petición, pega el Token si existe
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
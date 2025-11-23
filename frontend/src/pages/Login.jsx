import { useState } from 'react';
import client from '../api/client';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        
        try {
            // 1. Enviar credenciales al backend
            const response = await client.post('/api/token-auth/', {
                username: username,
                password: password
            });

            // 2. Si es exitoso, guardar el token
            const token = response.data.token;
            localStorage.setItem('token', token);
            
            // 3. Redirigir (Por ahora al home, luego haremos el Dashboard)
            alert("¡Login Exitoso! Token guardado.");
            navigate('/dashboard');

        } catch (err) {
            console.error(err);
            setError('Credenciales inválidas o error de conexión');
        }
    };

    return (
        <div className="container d-flex justify-content-center align-items-center vh-100 bg-light">
            <div className="card shadow p-4" style={{ width: '400px' }}>
                <h2 className="text-center text-success mb-4">Rutero Verde y Limpio</h2>
                <h5 className="text-center mb-4">Iniciar Sesión</h5>
                
                {error && <div className="alert alert-danger">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Usuario</label>
                        <input 
                            type="text" 
                            className="form-control"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required 
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Contraseña</label>
                        <input 
                            type="password" 
                            className="form-control"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required 
                        />
                    </div>
                    <button type="submit" className="btn btn-success w-100">
                        Ingresar
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Login;
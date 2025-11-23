import { useEffect, useState } from 'react';
import client from '../api/client';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
    const [rutas, setRutas] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/');
    };

    useEffect(() => {
        const fetchRutas = async () => {
            try {
                const response = await client.get('/api/rutas/');
                setRutas(response.data);
            } catch (error) {
                console.error("Error cargando rutas:", error);
                alert("Error cargando las rutas. Verifica tu conexión.");
            } finally {
                setLoading(false);
            }
        };
        fetchRutas();
    }, []);

    return (
        <div className="bg-light min-vh-100">
            <nav className="navbar navbar-expand-lg navbar-dark bg-success shadow-sm">
                <div className="container">
                    <a className="navbar-brand fw-bold" href="#">Rutero Verde 🌱</a>
                    <button className="btn btn-outline-light btn-sm" onClick={handleLogout}>
                        Cerrar Sesión
                    </button>
                </div>
            </nav>

            <div className="container mt-5">
                <div className="d-flex justify-content-between align-items-center mb-4">
                    <h2>Panel de Rutas</h2>
                    <button className="btn btn-primary" disabled>+ Nueva Ruta</button>
                </div>

                {loading ? (
                    <div className="text-center mt-5">
                        <div className="spinner-border text-success" role="status"></div>
                        <p className="mt-2">Cargando información...</p>
                    </div>
                ) : (
                    <div className="row">
                        {rutas.length === 0 ? (
                            <div className="col-12">
                                <div className="alert alert-info text-center">
                                    No tienes rutas asignadas por el momento.
                                </div>
                            </div>
                        ) : (
                            rutas.map((ruta) => (
                                <div key={ruta.id} className="col-md-4 mb-4">
                                    <div className="card shadow-sm h-100 border-0">
                                        <div className="card-header bg-white border-bottom-0 pt-3">
                                            <h5 className="card-title text-success mb-0">{ruta.nombre}</h5>
                                            <small className="text-muted">{ruta.fecha_programada}</small>
                                        </div>
                                        <div className="card-body">
                                            <p className="card-text">
                                                <strong>Estado:</strong> <span className="badge bg-secondary">{ruta.estado}</span><br/>
                                                <strong>Asesor:</strong> {ruta.asesor_nombre || "Sin asignar"}
                                            </p>
                                            <p className="small text-muted">
                                                {ruta.puntos.length} puntos de visita
                                            </p>
                                        </div>
                                        <div className="card-footer bg-white border-top-0 pb-3">
                                            {/* --- AQUÍ ESTÁ EL CAMBIO --- */}
                                            <button 
                                                className="btn btn-outline-success w-100"
                                                onClick={() => navigate(`/ruta/${ruta.id}`)}
                                            >
                                                Ver Detalles
                                            </button>
                                            {/* --------------------------- */}
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Dashboard;
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
            } finally {
                setLoading(false);
            }
        };
        fetchRutas();
    }, []);

    return (

        <div className="bg-light min-vh-100 w-100 text-start d-block">
             <nav className="navbar navbar-expand-lg navbar-dark bg-success shadow-sm w-100">
                <div className="container-fluid px-4">
                    <a className="navbar-brand fw-bold" href="#">Rutero Verde y Limpio🌱</a>
                    <button className="btn btn-outline-light btn-sm" onClick={handleLogout}>
                        Cerrar Sesión
                    </button>
                </div>
            </nav>

            <div className="container-fluid px-4 py-4 w-100">
                <div className="d-flex justify-content-between align-items-center mb-4 w-100">
                    <h2 className="mb-0">Panel de Rutas</h2>
                    <button className="btn btn-primary" disabled>
                        + Nueva Ruta
                    </button>
                </div>

                {loading ? (
                    <div className="text-center mt-5">
                        <div className="spinner-border text-success" role="status"></div>
                        <p className="mt-2">Cargando...</p>
                    </div>
                ) : (
                    <div className="row g-4 w-100 m-0"> 
                        {rutas.length === 0 ? (
                            <div className="col-12">
                                <div className="alert alert-info text-center shadow-sm">
                                    No tienes rutas asignadas por el momento.
                                </div>
                            </div>
                        ) : (
                            rutas.map((ruta) => (
                                <div key={ruta.id} className="col-12 col-md-6 col-lg-4 col-xl-3">
                                    <div className="card shadow-sm h-100 border-0">
                                        <div className="card-header bg-white border-bottom-0 pt-3">
                                            <div className="d-flex justify-content-between align-items-start mb-2">
                                                <h5 className="card-title text-success mb-0 text-truncate" title={ruta.nombre}>
                                                    {ruta.nombre}
                                                </h5>
                                                <span className={`badge ${ruta.estado === 'ACTIVA' ? 'bg-success' : 'bg-secondary'}`}>
                                                    {ruta.estado}
                                                </span>
                                            </div>
                                            <small className="text-muted">
                                                📅 {ruta.fecha_programada}
                                            </small>
                                        </div>
                                        
                                        <div className="card-body pt-0">
                                            <div className="mt-3">
                                                <div className="d-flex align-items-center mb-2">
                                                    <span className="me-2">👤</span>
                                                    <div>
                                                        <small className="text-muted d-block" style={{fontSize: '0.75rem'}}>Asesor</small>
                                                        <span className="fw-bold">{ruta.asesor_nombre || "Sin asignar"}</span>
                                                    </div>
                                                </div>
                                                
                                                <div className="d-flex align-items-center">
                                                    <span className="me-2">📍</span>
                                                    <div>
                                                        <small className="text-muted d-block" style={{fontSize: '0.75rem'}}>Puntos</small>
                                                        <span className="fw-bold">{ruta.puntos.length} visitas</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="card-footer bg-white border-top-0 pb-3">
                                            <button 
                                                className="btn btn-outline-success w-100 fw-bold"
                                                onClick={() => navigate(`/ruta/${ruta.id}`)}
                                            >
                                                Ver Detalles
                                            </button>
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
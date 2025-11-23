import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../api/client';

function RouteDetails() {
    const { id } = useParams();
    const [ruta, setRuta] = useState(null);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false); // Para mostrar "Subiendo..."
    const navigate = useNavigate();
    
    // Referencia para simular clic en el input de archivo
    const fileInputRef = useRef(null);
    const [selectedPuntoId, setSelectedPuntoId] = useState(null);

    useEffect(() => {
        cargarDetalle();
    }, [id]);

    const cargarDetalle = async () => {
        try {
            const response = await client.get(`/api/rutas/${id}/`);
            setRuta(response.data);
        } catch (error) {
            console.error("Error:", error);
            alert("No se pudo cargar la ruta.");
            navigate('/dashboard');
        } finally {
            setLoading(false);
        }
    };

    // 1. Iniciar proceso: Guardar ID del punto y abrir cámara
    const handleCheckInClick = (puntoId) => {
        setSelectedPuntoId(puntoId);
        // Simula clic en el input oculto
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    // 2. Cuando el usuario selecciona/toma la foto
    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setUploading(true);

        // 3. Obtener ubicación GPS
        if (!navigator.geolocation) {
            alert("Tu navegador no soporta geolocalización.");
            setUploading(false);
            return;
        }

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude, accuracy } = position.coords;
                
                // 4. Enviar todo al Backend
                await enviarVisita(file, latitude, longitude, accuracy);
            },
            (error) => {
                console.error("Error GPS:", error);
                alert("Error obteniendo ubicación. Asegúrate de dar permisos de GPS.");
                setUploading(false);
            },
            { enableHighAccuracy: true } // Pedir la mejor precisión posible
        );
    };

    const enviarVisita = async (foto, lat, lng, acc) => {
        const formData = new FormData();
        // Datos para crear la Visita
        formData.append('punto_visita', selectedPuntoId);
        
        // Necesitamos el ID del asesor (lo sacamos del localStorage o asumimos que el backend lo toma del token)
        // En tu ViewSet de Django pusimos lógica para esto, pero enviémoslo por si acaso si lo tienes a mano
        // Por ahora confiamos en que el backend asigna el usuario del token.
        
        formData.append('latitud_registro', lat);
        formData.append('longitud_registro', lng);
        formData.append('precision_gps', acc);
        formData.append('estado', 'REALIZADA');
        
        // La foto (Django espera 'foto_upload' según nuestro Serializer)
        formData.append('foto_upload', foto);

        try {
            // IMPORTANTE: El Content-Type se pone automático con FormData, no lo fuerces a JSON
            await client.post('/api/visitas/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                }
            });
            
            alert("✅ ¡Visita registrada con éxito!");
            // Recargar datos para actualizar la vista (opcional: mostrar check verde)
            cargarDetalle();

        } catch (error) {
            console.error("Error subiendo visita:", error.response?.data || error);
            alert("❌ Error al registrar la visita. Intenta de nuevo.");
        } finally {
            setUploading(false);
            // Limpiar el input para permitir subir la misma foto si se necesita
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    if (loading) return <div className="text-center mt-5"><div className="spinner-border text-success"></div></div>;
    if (!ruta) return null;

    return (
        <div className="bg-light min-vh-100 pb-5">
            {/* Input oculto para la cámara */}
            <input 
                type="file" 
                accept="image/*" 
                capture="environment" // Abre cámara trasera en móviles
                style={{ display: 'none' }} 
                ref={fileInputRef}
                onChange={handleFileChange}
            />

            {/* Overlay de carga (Pantalla bloqueada mientras sube) */}
            {uploading && (
                <div className="position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-75 d-flex flex-column justify-content-center align-items-center" style={{ zIndex: 1050 }}>
                    <div className="spinner-border text-light mb-3" style={{ width: '3rem', height: '3rem' }}></div>
                    <h4 className="text-white">Registrando visita...</h4>
                    <p className="text-white-50">Subiendo foto y ubicación</p>
                </div>
            )}

            {/* Cabecera */}
            <div className="bg-success text-white p-4 shadow-sm">
                <button onClick={() => navigate('/dashboard')} className="btn btn-sm btn-outline-light mb-2">
                    ← Volver
                </button>
                <h2>{ruta.nombre}</h2>
                <p className="mb-0 opacity-75">Fecha: {ruta.fecha_programada}</p>
            </div>

            <div className="container mt-4">
                <h4 className="mb-3 text-muted">Puntos de Visita</h4>
                
                <div className="row">
                    {ruta.puntos.length === 0 ? (
                        <div className="alert alert-warning">Esta ruta no tiene puntos asignados.</div>
                    ) : (
                        ruta.puntos.map((punto, index) => {
                            // Lógica visual: ¿Ya se visitó este punto?
                            // Tu API devuelve 'puntos', pero para saber si ya se hizo visita,
                            // necesitaríamos que el serializer de 'PuntoVisita' incluya el estado de la visita.
                            // Por ahora, el botón siempre estará activo para pruebas.
                            
                            return (
                                <div key={punto.id} className="col-12 mb-3">
                                    <div className="card border-0 shadow-sm">
                                        <div className="card-body d-flex justify-content-between align-items-center">
                                            <div>
                                                <h5 className="card-title text-primary mb-1">
                                                    <span className="badge bg-light text-dark border me-2">#{index + 1}</span>
                                                    {punto.conjunto.nombre}
                                                </h5>
                                                <p className="card-text small text-muted mb-0">
                                                    📍 {punto.conjunto.direccion}
                                                </p>
                                            </div>
                                            
                                            <button 
                                                className="btn btn-primary"
                                                onClick={() => handleCheckInClick(punto.id)}
                                                disabled={uploading}
                                            >
                                                📸 Check-in
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            );
                        })
                    )}
                </div>
            </div>
        </div>
    );
}

export default RouteDetails;
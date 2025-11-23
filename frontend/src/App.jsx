import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import RouteDetails from './pages/RouteDetails'; // <--- 1. Importar

const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('token');
    return token ? children : <Navigate to="/" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        
        <Route path="/dashboard" element={
            <PrivateRoute>
                <Dashboard />
            </PrivateRoute>
        } />

        {/* 2. Nueva Ruta Dinámica (:id cambiará según la ruta seleccionada) */}
        <Route path="/ruta/:id" element={
            <PrivateRoute>
                <RouteDetails />
            </PrivateRoute>
        } />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
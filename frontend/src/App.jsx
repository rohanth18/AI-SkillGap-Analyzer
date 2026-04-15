import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import UploadResume from './pages/UploadResume';
import AnalysisDetail from './pages/AnalysisDetail';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import RoleManagement from './pages/RoleManagement';
import ManageUsers from './pages/ManageUsers';
import RoleRecommendations from './pages/RoleRecommendations';
import LearningRoadmap from './pages/LearningRoadmap';
import ProjectRecommendations from './pages/ProjectRecommendations';

import AdminInsights from './pages/AdminInsights';
import HomePage from './pages/HomePage';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import { useState, useEffect } from 'react';

function App() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('skillgap_user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
    }, []);

    const handleLogin = (userData) => {
        setUser(userData);
        localStorage.setItem('skillgap_user', JSON.stringify(userData));
    };

    const handleLogout = () => {
        setUser(null);
        localStorage.removeItem('skillgap_user');
    };

    return (
        <div className="app">
            <Navbar user={user} onLogout={handleLogout} />
            <Routes>
                {/* Public Routes */}
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<Login onLogin={handleLogin} />} />
                <Route path="/register" element={<Register />} />
                <Route path="/admin/login" element={<AdminLogin onLogin={handleLogin} />} />

                {/* User Protected Routes */}
                <Route path="/dashboard" element={
                    <ProtectedRoute user={user}>
                        <Dashboard user={user} />
                    </ProtectedRoute>
                } />
                <Route path="/upload" element={
                    <ProtectedRoute user={user}>
                        <UploadResume user={user} />
                    </ProtectedRoute>
                } />
                <Route path="/analysis/:id" element={
                    <ProtectedRoute user={user}>
                        <AnalysisDetail />
                    </ProtectedRoute>
                } />
                <Route path="/role-recommendations/:id" element={
                    <ProtectedRoute user={user}>
                        <RoleRecommendations />
                    </ProtectedRoute>
                } />
                <Route path="/learning-roadmap/:id" element={
                    <ProtectedRoute user={user}>
                        <LearningRoadmap />
                    </ProtectedRoute>
                } />
                <Route path="/projects/:id" element={
                    <ProtectedRoute user={user}>
                        <ProjectRecommendations />
                    </ProtectedRoute>
                } />


                {/* Admin Protected Routes */}
                <Route path="/admin/dashboard" element={
                    <ProtectedRoute user={user} adminOnly>
                        <AdminDashboard />
                    </ProtectedRoute>
                } />
                <Route path="/admin/roles" element={
                    <ProtectedRoute user={user} adminOnly>
                        <RoleManagement />
                    </ProtectedRoute>
                } />
                <Route path="/admin/users" element={
                    <ProtectedRoute user={user} adminOnly>
                        <ManageUsers />
                    </ProtectedRoute>
                } />
                <Route path="/admin/insights" element={
                    <ProtectedRoute user={user} adminOnly>
                        <AdminInsights />
                    </ProtectedRoute>
                } />

                <Route path="*" element={<Navigate to={user ? "/" : "/login"} />} />
            </Routes>
        </div>
    );
}

export default App;

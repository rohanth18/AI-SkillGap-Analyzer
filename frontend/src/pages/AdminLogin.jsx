import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const AdminLogin = ({ onLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('/login', { email, password });
            if (!res.data.user.is_admin) {
                setError('Access denied. Admin rights required.');
                return;
            }
            const userData = { ...res.data.user, token: res.data.token };
            onLogin(userData);
            navigate('/admin/dashboard');
        } catch (err) {
            setError(err.response?.data?.error || 'Login failed');
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'var(--bg-color)' }}>
            <form className="glass-panel" style={{ padding: '2rem', width: '350px', border: '1px solid #f87171' }} onSubmit={handleSubmit}>
                <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: '#f87171' }}>Admin Portal</h2>
                {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
                <input
                    className="input-field"
                    type="email"
                    placeholder="Admin Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    className="input-field"
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button className="btn-primary" style={{ width: '100%', background: '#f87171' }} type="submit">Admin Login</button>
            </form>
        </div>
    );
};

export default AdminLogin;

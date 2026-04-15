import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

const Login = ({ onLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('/login', { email, password });
            const userData = { ...res.data.user, token: res.data.token };
            onLogin(userData);
            navigate(userData.is_admin ? '/admin/dashboard' : '/');
        } catch (err) {
            setError(err.response?.data?.error || 'Login failed');
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'var(--bg-color)' }}>
            <form className="glass-panel" style={{ padding: '2rem', width: '350px' }} onSubmit={handleSubmit}>
                <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Login</h2>
                {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
                <input
                    className="input-field"
                    type="email"
                    placeholder="Email"
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
                <button className="btn-primary" style={{ width: '100%' }} type="submit">Log In</button>
                <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    <Link to="/register" style={{ color: 'var(--primary-color)' }}>Create an account</Link>
                </div>
                <div style={{ marginTop: '0.5rem', textAlign: 'center' }}>
                    <Link to="/admin/login" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Admin Access</Link>
                </div>
            </form>
        </div>
    );
};

export default Login;

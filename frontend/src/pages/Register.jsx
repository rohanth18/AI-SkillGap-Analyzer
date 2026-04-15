import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

const Register = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/register', { name, email, password });
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.error || 'Registration failed');
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'var(--bg-color)' }}>
            <form className="glass-panel" style={{ padding: '2rem', width: '350px' }} onSubmit={handleSubmit}>
                <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Register</h2>
                {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
                <input
                    className="input-field"
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
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
                <button className="btn-primary" style={{ width: '100%' }} type="submit">Register</button>
                <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    <Link to="/login" style={{ color: 'var(--primary-color)' }}>Already have an account?</Link>
                </div>
            </form>
        </div>
    );
};

export default Register;

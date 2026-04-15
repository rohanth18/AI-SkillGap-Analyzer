import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Dashboard = ({ user }) => {
    const [analyses, setAnalyses] = useState([]);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await api.get('/user/analyses');
                setAnalyses(res.data);
            } catch (err) {
                console.error('Error fetching analyses:', err);
            }
        };
        fetchHistory();
    }, []);

    // Chart Data: Progress over time (Confidence Score)
    // Reverse array to show oldest to newest for chart
    const chartData = {
        labels: [...analyses].reverse().map(a => new Date(a.created_at).toLocaleDateString()),
        datasets: [{
            label: 'Confidence Score',
            data: [...analyses].reverse().map(a => a.confidence_score),
            borderColor: '#a855f7',
            backgroundColor: 'rgba(168, 85, 247, 0.5)',
            tension: 0.3
        }]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top', labels: { color: '#f8fafc' } },
        },
        scales: {
            y: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
        }
    };

    return (
        <div className="page-container animate-fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2>Welcome back, {user.name}</h2>
                <Link to="/upload" className="btn-primary" style={{ textDecoration: 'none' }}>+ New Analysis</Link>
            </div>

            {analyses.length === 0 ? (
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem' }}>You haven't analyzed any resumes yet.</p>
                    <Link to="/upload" style={{ color: 'var(--primary-color)' }}>Get started now</Link>
                </div>
            ) : (
                <>
                    <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
                        <h3>Progress Over Time</h3>
                        <div style={{ height: '300px', width: '100%', position: 'relative' }}>
                            <Line data={chartData} options={chartOptions} />
                        </div>
                    </div>

                    <h3>Recent Analyses</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '1rem' }}>
                        {analyses.map(a => (
                            <div key={a.id} className="glass-panel" style={{ padding: '1.5rem' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                                    <span style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{a.job_role}</span>
                                    <span style={{
                                        color: a.confidence_score > 70 ? '#4ade80' : '#facc15',
                                        fontWeight: 'bold'
                                    }}>{a.confidence_score}%</span>
                                </div>
                                <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>
                                    {new Date(a.created_at).toLocaleDateString()}
                                </div>
                                <Link to={`/analysis/${a.id}`} className="btn-secondary" style={{ display: 'inline-block', textDecoration: 'none', fontSize: '0.9rem' }}>
                                    View Details
                                </Link>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

export default Dashboard;

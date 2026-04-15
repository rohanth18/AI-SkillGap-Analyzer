import React, { useEffect, useState } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';

const AdminDashboard = () => {
    const [stats, setStats] = useState({ total_users: 0, total_resumes: 0, average_score: 0 });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await api.get('/admin/stats');
                setStats(res.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchStats();
    }, []);

    return (
        <div className="page-container animate-fade-in">
            <h1 style={{ marginBottom: '2rem' }}>Admin Dashboard</h1>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem', marginBottom: '3rem' }}>
                <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '3rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>{stats.total_users}</div>
                    <div style={{ color: 'var(--text-secondary)' }}>Total Users</div>
                </div>
                <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '3rem', fontWeight: 'bold', color: 'var(--secondary-color)' }}>{stats.total_resumes}</div>
                    <div style={{ color: 'var(--text-secondary)' }}>Total Analyses</div>
                </div>
                <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#4ade80' }}>{stats.average_score}%</div>
                    <div style={{ color: 'var(--text-secondary)' }}>Avg Confidence Score</div>
                </div>
            </div>

            {/* NEW STATS SECTION */}
            <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
                <h3 style={{ marginBottom: '1.5rem' }}>Common Skill Gaps (Top 5)</h3>
                {stats.top_missing_skills && stats.top_missing_skills.length > 0 ? (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {stats.top_missing_skills.map((item, idx) => (
                            <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                <span style={{ width: '150px', fontWeight: 'bold' }}>{item.skill}</span>
                                <div style={{ flex: 1, background: 'rgba(255,255,255,0.1)', height: '24px', borderRadius: '12px', overflow: 'hidden' }}>
                                    <div style={{
                                        width: `${(item.count / (stats.total_resumes || 1)) * 100}%`,
                                        background: '#f87171',
                                        height: '100%',
                                        minWidth: '5px'
                                    }}></div>
                                </div>
                                <span style={{ minWidth: '80px', textAlign: 'right' }}>{item.count} analyses</span>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p style={{ color: 'var(--text-secondary)' }}>No sufficient data yet.</p>
                )}
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
                <Link to="/admin/roles" className="btn-primary" style={{ textDecoration: 'none' }}>Manage Job Roles & Skills</Link>
                <Link to="/admin/users" className="btn-secondary" style={{ textDecoration: 'none' }}>Manage Users</Link>
            </div>
        </div>
    );
};

export default AdminDashboard;

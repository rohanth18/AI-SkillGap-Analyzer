import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import { Bar, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

const AdminInsights = () => {
    const [heatmapData, setHeatmapData] = useState([]);
    const [trendData, setTrendData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchInsights();
    }, []);

    const fetchInsights = async () => {
        try {
            setLoading(true);

            // Fetch both heatmap and trends
            const [heatmapRes, trendsRes] = await Promise.all([
                api.get('/admin/insights/heatmap'),
                api.get('/admin/insights/trends')
            ]);

            setHeatmapData(heatmapRes.data.heatmap_data || []);
            setTrendData(trendsRes.data.trend_data || []);
        } catch (err) {
            console.error('Error fetching insights:', err);
            setError('Failed to load insights data');
        } finally {
            setLoading(false);
        }
    };

    // Heatmap Chart Data
    const heatmapChartData = {
        labels: heatmapData.map(item => item.skill),
        datasets: [{
            label: 'Number of Users Missing This Skill',
            data: heatmapData.map(item => item.count),
            backgroundColor: 'rgba(248, 113, 113, 0.8)',
            borderColor: 'rgba(248, 113, 113, 1)',
            borderWidth: 1
        }]
    };

    const heatmapChartOptions = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Top 20 Most Missing Skills',
                color: '#f8fafc',
                font: { size: 16 }
            }
        },
        scales: {
            x: {
                grid: { color: 'rgba(255,255,255,0.1)' },
                ticks: { color: '#94a3b8' }
            },
            y: {
                grid: { display: false },
                ticks: { color: '#94a3b8' }
            }
        }
    };

    // Trends Chart Data
    const trendsChartData = {
        labels: trendData.map(item => item.domain),
        datasets: [{
            label: 'Skill Gaps',
            data: trendData.map(item => item.gap_count),
            backgroundColor: [
                'rgba(168, 85, 247, 0.8)',
                'rgba(59, 130, 246, 0.8)',
                'rgba(74, 222, 128, 0.8)',
                'rgba(250, 204, 21, 0.8)',
                'rgba(248, 113, 113, 0.8)',
                'rgba(251, 146, 60, 0.8)',
                'rgba(236, 72, 153, 0.8)'
            ],
            borderColor: [
                'rgba(168, 85, 247, 1)',
                'rgba(59, 130, 246, 1)',
                'rgba(74, 222, 128, 1)',
                'rgba(250, 204, 21, 1)',
                'rgba(248, 113, 113, 1)',
                'rgba(251, 146, 60, 1)',
                'rgba(236, 72, 153, 1)'
            ],
            borderWidth: 2
        }]
    };

    const trendsChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: { color: '#f8fafc' }
            },
            title: {
                display: true,
                text: 'Skill Gaps by Domain',
                color: '#f8fafc',
                font: { size: 16 }
            }
        }
    };

    if (loading) {
        return (
            <div className="page-container animate-fade-in">
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>Loading insights...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="page-container animate-fade-in">
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p style={{ color: '#f87171' }}>{error}</p>
                    <Link to="/admin/dashboard" className="btn-primary" style={{ marginTop: '1rem' }}>
                        Back to Dashboard
                    </Link>
                </div>
            </div>
        );
    }

    const totalGaps = heatmapData.reduce((sum, item) => sum + item.count, 0);
    const avgGapsPerSkill = heatmapData.length > 0 ? (totalGaps / heatmapData.length).toFixed(1) : 0;
    const topSkill = heatmapData[0];

    return (
        <div className="page-container animate-fade-in">
            <div style={{ marginBottom: '2rem' }}>
                <Link to="/admin/dashboard" style={{ color: 'var(--primary-color)', textDecoration: 'none' }}>
                    ← Back to Admin Dashboard
                </Link>
            </div>

            <h1 style={{ marginBottom: '1rem' }}>📊 Deep Analytics & Insights</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                Comprehensive skill gap analysis across all users
            </p>

            {/* Summary Stats */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', background: 'linear-gradient(135deg, rgba(248, 113, 113, 0.1), rgba(251, 146, 60, 0.1))' }}>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#f87171' }}>
                        {totalGaps}
                    </div>
                    <div style={{ color: 'var(--text-secondary)' }}>Total Skill Gaps</div>
                </div>

                <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(59, 130, 246, 0.1))' }}>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>
                        {heatmapData.length}
                    </div>
                    <div style={{ color: 'var(--text-secondary)' }}>Unique Skills Tracked</div>
                </div>

                <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', background: 'linear-gradient(135deg, rgba(74, 222, 128, 0.1), rgba(34, 197, 94, 0.1))' }}>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#4ade80' }}>
                        {avgGapsPerSkill}
                    </div>
                    <div style={{ color: 'var(--text-secondary)' }}>Avg Gaps per Skill</div>
                </div>

                {topSkill && (
                    <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', background: 'linear-gradient(135deg, rgba(250, 204, 21, 0.1), rgba(245, 158, 11, 0.1))' }}>
                        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#facc15', marginBottom: '0.5rem' }}>
                            {topSkill.skill}
                        </div>
                        <div style={{ color: 'var(--text-secondary)' }}>Most Missing Skill ({topSkill.count} analyses)</div>
                    </div>
                )}
            </div>

            {/* Heatmap Chart */}
            <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
                <div style={{ height: '600px' }}>
                    {heatmapData.length > 0 ? (
                        <Bar data={heatmapChartData} options={heatmapChartOptions} />
                    ) : (
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)' }}>
                            No skill gap data available
                        </div>
                    )}
                </div>
            </div>

            {/* Domain Trends */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
                {/* Doughnut Chart */}
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <div style={{ height: '400px' }}>
                        {trendData.length > 0 ? (
                            <Doughnut data={trendsChartData} options={trendsChartOptions} />
                        ) : (
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)' }}>
                                No trend data available
                            </div>
                        )}
                    </div>
                </div>

                {/* Domain Breakdown */}
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1.5rem' }}>Domain Breakdown</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {trendData
                            .sort((a, b) => b.gap_count - a.gap_count)
                            .map((trend, index) => {
                                const colors = ['#a855f7', '#3b82f6', '#4ade80', '#facc15', '#f87171', '#fb923c', '#ec4899'];
                                const color = colors[index % colors.length];
                                const percentage = totalGaps > 0 ? ((trend.gap_count / totalGaps) * 100).toFixed(1) : 0;

                                return (
                                    <div key={trend.domain} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                        <div style={{
                                            width: '12px',
                                            height: '12px',
                                            borderRadius: '50%',
                                            background: color,
                                            flexShrink: 0
                                        }}></div>
                                        <div style={{ flex: 1 }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                                                <span style={{ fontWeight: 'bold' }}>{trend.domain}</span>
                                                <span style={{ color: 'var(--text-secondary)' }}>{trend.gap_count} gaps ({percentage}%)</span>
                                            </div>
                                            <div style={{
                                                width: '100%',
                                                height: '6px',
                                                background: 'rgba(255,255,255,0.1)',
                                                borderRadius: '3px',
                                                overflow: 'hidden'
                                            }}>
                                                <div style={{
                                                    width: `${percentage}%`,
                                                    height: '100%',
                                                    background: color,
                                                    transition: 'width 1s ease-out'
                                                }}></div>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                    </div>
                </div>
            </div>

            {/* Insights & Recommendations */}
            <div className="glass-panel" style={{ padding: '2rem', background: 'rgba(59, 130, 246, 0.1)' }}>
                <h3 style={{ marginBottom: '1rem' }}>💡 Key Insights</h3>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.8', margin: 0 }}>
                    {topSkill && (
                        <li>
                            <strong style={{ color: 'var(--text-primary)' }}>{topSkill.skill}</strong> is the most commonly missing skill - consider creating targeted training programs
                        </li>
                    )}
                    {trendData.length > 0 && (
                        <li>
                            <strong style={{ color: 'var(--text-primary)' }}>{trendData.sort((a, b) => b.gap_count - a.gap_count)[0].domain}</strong> domain shows the highest skill gaps - focus recruitment and training efforts here
                        </li>
                    )}
                    <li>Use this data to inform curriculum development and training priorities</li>
                    <li>Consider partnerships with educational institutions for high-demand skills</li>
                    <li>Track trends over time to measure the effectiveness of training programs</li>
                </ul>
            </div>

            {/* Action Items */}
            <div className="glass-panel" style={{ padding: '2rem', marginTop: '2rem', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(59, 130, 246, 0.1))' }}>
                <h3 style={{ marginBottom: '1rem' }}>🎯 Recommended Actions</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
                    <Link to="/admin/roles" className="btn-primary" style={{ textDecoration: 'none', textAlign: 'center' }}>
                        📚 Update Job Roles
                    </Link>
                    <Link to="/admin/users" className="btn-secondary" style={{ textDecoration: 'none', textAlign: 'center' }}>
                        👥 View User Progress
                    </Link>
                    <button onClick={fetchInsights} className="btn-secondary">
                        🔄 Refresh Data
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AdminInsights;

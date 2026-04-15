import React, { useEffect, useState } from 'react';
import { useParams, useSearchParams, Link } from 'react-router-dom';
import api from '../api';

const LearningRoadmap = () => {
    const { id } = useParams(); // analysis_id
    const [searchParams] = useSearchParams();
    const targetRole = searchParams.get('role');

    const [roadmap, setRoadmap] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [expandedWeeks, setExpandedWeeks] = useState(new Set([1, 2, 3])); // First 3 weeks expanded by default

    useEffect(() => {
        fetchRoadmap();
    }, [id]);

    const fetchRoadmap = async () => {
        try {
            setLoading(true);
            // Get complete analysis
            const res = await api.get(`/analysis/${id}/complete`);

            if (res.data.roadmap) {
                setRoadmap(res.data.roadmap);
            } else {
                // Generate roadmap if not exists
                const missing = res.data.missing_skills || [];
                const jobRole = targetRole || res.data.job_role;

                const roadmapRes = await api.post('/generate-roadmap', {
                    missing_skills: missing,
                    job_role: jobRole,
                    analysis_id: id
                });
                setRoadmap(roadmapRes.data);
            }
        } catch (err) {
            console.error('Error fetching roadmap:', err);
            setError('Failed to load learning roadmap');
        } finally {
            setLoading(false);
        }
    };

    const toggleWeek = (weekNum) => {
        const newExpanded = new Set(expandedWeeks);
        if (newExpanded.has(weekNum)) {
            newExpanded.delete(weekNum);
        } else {
            newExpanded.add(weekNum);
        }
        setExpandedWeeks(newExpanded);
    };

    const expandAll = () => {
        if (roadmap && roadmap.roadmap) {
            const allWeeks = new Set(roadmap.roadmap.map(w => w.week));
            setExpandedWeeks(allWeeks);
        }
    };

    const collapseAll = () => {
        setExpandedWeeks(new Set());
    };

    if (loading) {
        return (
            <div className="page-container animate-fade-in">
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>Generating your personalized learning roadmap...</p>
                </div>
            </div>
        );
    }

    if (error || !roadmap) {
        return (
            <div className="page-container animate-fade-in">
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p style={{ color: '#f87171' }}>{error || 'No roadmap available'}</p>
                    <Link to={`/analysis/${id}`} className="btn-primary" style={{ marginTop: '1rem' }}>
                        Back to Analysis
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="page-container animate-fade-in">
            <div style={{ marginBottom: '2rem' }}>
                <Link to={`/analysis/${id}`} style={{ color: 'var(--primary-color)', textDecoration: 'none' }}>
                    ← Back to Analysis
                </Link>
            </div>

            {/* Header */}
            <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(59, 130, 246, 0.2))' }}>
                <h1 style={{ marginBottom: '1rem' }}>📚 Your Personalized Learning Roadmap</h1>
                <h2 style={{ color: 'var(--primary-color)', marginBottom: '1rem' }}>{roadmap.job_role}</h2>

                <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap', marginTop: '1.5rem' }}>
                    <div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>
                            {roadmap.total_weeks}
                        </div>
                        <div style={{ color: 'var(--text-secondary)' }}>Total Weeks</div>
                    </div>
                    <div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#4ade80' }}>
                            {roadmap.skills_covered}
                        </div>
                        <div style={{ color: 'var(--text-secondary)' }}>Skills Covered</div>
                    </div>
                    <div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#facc15' }}>
                            {roadmap.roadmap?.length || 0}
                        </div>
                        <div style={{ color: 'var(--text-secondary)' }}>Learning Modules</div>
                    </div>
                </div>

                <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem' }}>
                    <button onClick={expandAll} className="btn-secondary" style={{ fontSize: '0.9rem' }}>
                        Expand All
                    </button>
                    <button onClick={collapseAll} className="btn-secondary" style={{ fontSize: '0.9rem' }}>
                        Collapse All
                    </button>
                </div>
            </div>

            {/* Timeline */}
            {roadmap.roadmap && roadmap.roadmap.length > 0 ? (
                <div style={{ position: 'relative' }}>
                    {/* Vertical line */}
                    <div style={{
                        position: 'absolute',
                        left: '20px',
                        top: '0',
                        bottom: '0',
                        width: '2px',
                        background: 'linear-gradient(to bottom, var(--primary-color), var(--secondary-color))',
                        opacity: 0.3
                    }}></div>

                    {roadmap.roadmap.map((week, index) => {
                        const isExpanded = expandedWeeks.has(week.week);
                        const isEven = index % 2 === 0;

                        return (
                            <div
                                key={week.week}
                                style={{
                                    marginBottom: '2rem',
                                    marginLeft: '50px',
                                    position: 'relative'
                                }}
                            >
                                {/* Week number circle */}
                                <div style={{
                                    position: 'absolute',
                                    left: '-50px',
                                    top: '10px',
                                    width: '40px',
                                    height: '40px',
                                    borderRadius: '50%',
                                    background: isExpanded ? 'var(--primary-color)' : 'rgba(255,255,255,0.1)',
                                    border: '2px solid var(--primary-color)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontWeight: 'bold',
                                    fontSize: '0.9rem',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease',
                                    zIndex: 1
                                }}
                                    onClick={() => toggleWeek(week.week)}
                                >
                                    {week.week}
                                </div>

                                <div
                                    className="glass-panel"
                                    style={{
                                        padding: '1.5rem',
                                        cursor: 'pointer',
                                        transition: 'all 0.3s ease',
                                        border: isExpanded ? '2px solid var(--primary-color)' : undefined
                                    }}
                                    onClick={() => toggleWeek(week.week)}
                                >
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <div>
                                            <h3 style={{ margin: 0, color: 'var(--primary-color)' }}>
                                                Week {week.week}: {week.title}
                                            </h3>
                                            <div style={{
                                                marginTop: '0.5rem',
                                                color: 'var(--text-secondary)',
                                                fontSize: '0.9rem'
                                            }}>
                                                Focus: <span style={{ color: '#4ade80', fontWeight: 'bold' }}>{week.skill}</span>
                                            </div>
                                        </div>
                                        <div style={{ fontSize: '1.5rem', transition: 'transform 0.3s ease', transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}>
                                            ▼
                                        </div>
                                    </div>

                                    {isExpanded && (
                                        <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                                            {/* Topics */}
                                            <div style={{ marginBottom: '1.5rem' }}>
                                                <h4 style={{ color: 'var(--primary-color)', marginBottom: '0.5rem' }}>📖 Topics to Cover:</h4>
                                                <ul style={{ margin: 0, paddingLeft: '1.5rem', lineHeight: '1.8' }}>
                                                    {week.topics.map((topic, i) => (
                                                        <li key={i} style={{ color: 'var(--text-secondary)' }}>{topic}</li>
                                                    ))}
                                                </ul>
                                            </div>

                                            {/* Resources */}
                                            <div style={{ marginBottom: '1.5rem' }}>
                                                <h4 style={{ color: '#60a5fa', marginBottom: '0.5rem' }}>🔗 Learning Resources:</h4>
                                                <ul style={{ margin: 0, paddingLeft: '1.5rem', lineHeight: '1.8' }}>
                                                    {week.resources.map((resource, i) => (
                                                        <li key={i} style={{ color: 'var(--text-secondary)' }}>{resource}</li>
                                                    ))}
                                                </ul>
                                            </div>

                                            {/* Practice */}
                                            <div style={{
                                                background: 'rgba(74, 222, 128, 0.1)',
                                                padding: '1rem',
                                                borderRadius: '8px',
                                                border: '1px solid rgba(74, 222, 128, 0.3)'
                                            }}>
                                                <h4 style={{ color: '#4ade80', marginBottom: '0.5rem' }}>🎯 Practice Task:</h4>
                                                <p style={{ margin: 0, color: 'var(--text-secondary)' }}>{week.practice}</p>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            ) : (
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>{roadmap.message || 'No roadmap items available'}</p>
                </div>
            )}

            {/* Footer Tips */}
            <div className="glass-panel" style={{ padding: '2rem', marginTop: '2rem', background: 'rgba(59, 130, 246, 0.1)' }}>
                <h3 style={{ marginBottom: '1rem' }}>💡 Tips for Success</h3>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.8', margin: 0 }}>
                    <li>Follow the roadmap week by week for best results</li>
                    <li>Complete the practice tasks to reinforce your learning</li>
                    <li>Don't skip weeks - each builds on the previous one</li>
                    <li>Join online communities for support and networking</li>
                    <li>Build projects alongside learning to apply your knowledge</li>
                </ul>
            </div>
        </div>
    );
};

export default LearningRoadmap;

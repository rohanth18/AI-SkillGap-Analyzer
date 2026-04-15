import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

const RoleRecommendations = () => {
    const { id } = useParams(); // analysis_id
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchRecommendations();
    }, [id]);

    const fetchRecommendations = async () => {
        try {
            setLoading(true);
            // Get complete analysis which includes recommendations
            const res = await api.get(`/analysis/${id}/complete`);

            if (res.data.recommended_roles) {
                setRecommendations(res.data.recommended_roles);
            } else {
                // If not generated yet, generate them
                const skills = res.data.all_skills && res.data.all_skills.length > 0
                    ? res.data.all_skills
                    : Object.keys(res.data.extracted_skills || {});

                const recRes = await api.post('/recommend-roles', {
                    skills: skills,
                    analysis_id: id
                });
                setRecommendations(recRes.data.recommended_roles);
            }
        } catch (err) {
            console.error('Error fetching recommendations:', err);
            setError('Failed to load role recommendations');
        } finally {
            setLoading(false);
        }
    };

    const getConfidenceColor = (confidence) => {
        if (confidence >= 80) return '#4ade80'; // Green
        if (confidence >= 60) return '#facc15'; // Yellow
        return '#f87171'; // Red
    };

    const getConfidenceLabel = (confidence) => {
        if (confidence >= 80) return 'Excellent Match';
        if (confidence >= 60) return 'Good Match';
        return 'Potential Match';
    };

    if (loading) {
        return (
            <div className="page-container animate-fade-in">
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>Loading recommendations...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="page-container animate-fade-in">
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p style={{ color: '#f87171' }}>{error}</p>
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

            <h1 style={{ marginBottom: '1rem' }}>🎯 Recommended Job Roles</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                Based on your skills, our AI recommends these job roles for you
            </p>

            {recommendations.length === 0 ? (
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>No recommendations available</p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '1.5rem' }}>
                    {recommendations.map((rec, index) => (
                        <div
                            key={index}
                            className="glass-panel"
                            style={{
                                padding: '2rem',
                                background: index === 0 ? 'linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(59, 130, 246, 0.1))' : undefined,
                                border: index === 0 ? '2px solid var(--primary-color)' : undefined
                            }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                                <div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                        {index === 0 && <span style={{ fontSize: '1.5rem' }}>🏆</span>}
                                        <h2 style={{ margin: 0, color: 'var(--primary-color)' }}>
                                            {rec.role}
                                        </h2>
                                    </div>
                                    {index === 0 && (
                                        <span style={{
                                            background: 'var(--primary-color)',
                                            color: 'white',
                                            padding: '2px 8px',
                                            borderRadius: '4px',
                                            fontSize: '0.8rem',
                                            fontWeight: 'bold'
                                        }}>
                                            TOP RECOMMENDATION
                                        </span>
                                    )}
                                </div>

                                <div style={{ textAlign: 'right' }}>
                                    <div style={{
                                        fontSize: '2.5rem',
                                        fontWeight: 'bold',
                                        color: getConfidenceColor(rec.confidence)
                                    }}>
                                        {rec.confidence}%
                                    </div>
                                    <div style={{
                                        fontSize: '0.9rem',
                                        color: getConfidenceColor(rec.confidence)
                                    }}>
                                        {getConfidenceLabel(rec.confidence)}
                                    </div>
                                </div>
                            </div>

                            <div style={{
                                width: '100%',
                                height: '8px',
                                background: 'rgba(255,255,255,0.1)',
                                borderRadius: '4px',
                                overflow: 'hidden',
                                marginBottom: '1.5rem'
                            }}>
                                <div style={{
                                    width: `${rec.confidence}%`,
                                    height: '100%',
                                    background: getConfidenceColor(rec.confidence),
                                    transition: 'width 1s ease-out'
                                }}></div>
                            </div>


                        </div>
                    ))}
                </div>
            )}

            <div className="glass-panel" style={{ padding: '2rem', marginTop: '2rem', background: 'rgba(59, 130, 246, 0.1)' }}>
                <h3 style={{ marginBottom: '1rem' }}>💡 What does this mean?</h3>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.8' }}>
                    <li>These recommendations are generated using Machine Learning based on your skill profile</li>
                    <li>Higher confidence scores indicate better alignment with your current skills</li>
                    <li>The top recommendation is our AI's best match for your profile</li>
                </ul>
            </div>
        </div>
    );
};

export default RoleRecommendations;

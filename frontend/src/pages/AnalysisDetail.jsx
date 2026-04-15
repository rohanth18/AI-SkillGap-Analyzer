import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import SkillGapChart from '../components/SkillGapChart';

const AnalysisDetail = () => {
    const { id } = useParams();
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalysis = async () => {
            try {
                const res = await api.get(`/analysis/${id}`);
                setAnalysis(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchAnalysis();
    }, [id]);

    if (loading) return <div className="page-container">Loading...</div>;
    if (!analysis) return <div className="page-container">Analysis not found</div>;

    return (
        <div className="page-container animate-fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Analysis Result: <span style={{ color: 'var(--primary-color)' }}>{analysis.job_role}</span></h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <div className="glass-panel" style={{ padding: '0.5rem 1.5rem', textAlign: 'center' }}>
                        <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>ATS Score</span>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: (analysis.ats_score || 0) > 70 ? '#4ade80' : (analysis.ats_score || 0) > 40 ? '#facc15' : '#f87171' }}>
                            {analysis.ats_score || 'N/A'}{analysis.ats_score ? '%' : ''}
                        </div>
                    </div>
                    <div className="glass-panel" style={{ padding: '0.5rem 1.5rem', textAlign: 'center' }}>
                        <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Match Score</span>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: analysis.confidence_score > 70 ? '#4ade80' : analysis.confidence_score > 40 ? '#facc15' : '#f87171' }}>
                            {analysis.confidence_score}%
                        </div>
                    </div>
                </div>
            </div>

            {/* Advanced Features Action Buttons */}
            <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(59, 130, 246, 0.1))' }}>
                <h3 style={{ marginBottom: '1rem' }}>🚀 Explore Advanced Features</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                    <Link to={`/role-recommendations/${id}`} className="btn-primary" style={{ textDecoration: 'none', textAlign: 'center' }}>
                        🎯 Role Recommendations
                    </Link>
                    <Link to={`/learning-roadmap/${id}`} className="btn-primary" style={{ textDecoration: 'none', textAlign: 'center' }}>
                        📚 Learning Roadmap
                    </Link>
                    <Link to={`/projects/${id}`} className="btn-primary" style={{ textDecoration: 'none', textAlign: 'center' }}>
                        💻 Practice Projects
                    </Link>

                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1rem' }}>Skill Gap Visualization</h3>
                    <div>
                        <SkillGapChart missing={analysis.missing_skills} present={Object.keys(analysis.extracted_skills)} />
                    </div>
                </div>

                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1rem' }}>Missing Skills ({analysis.missing_skills.length})</h3>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                        {analysis.missing_skills.map(s => (
                            <span key={s} style={{
                                background: 'rgba(248, 113, 113, 0.2)',
                                color: '#f87171',
                                padding: '5px 10px',
                                borderRadius: '20px',
                                fontSize: '0.9rem',
                                border: '1px solid rgba(248, 113, 113, 0.3)'
                            }}>
                                {s}
                            </span>
                        ))}
                    </div>

                    <h3 style={{ marginTop: '2rem', marginBottom: '1rem' }}>Matching Skills ({Object.keys(analysis.extracted_skills).length})</h3>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                        {Object.entries(analysis.extracted_skills).map(([skill, data]) => (
                            <span key={skill} title={`Source: ${data.sources.join(', ')}`} style={{
                                background: 'rgba(74, 222, 128, 0.2)',
                                color: '#4ade80',
                                padding: '5px 10px',
                                borderRadius: '20px',
                                fontSize: '0.9rem',
                                border: '1px solid rgba(74, 222, 128, 0.3)',
                                cursor: 'help'
                            }}>
                                {skill} {data.sources.includes('manual') ? '✎' : ''}
                            </span>
                        ))}
                    </div>
                </div>
            </div>

            <div className="glass-panel" style={{ padding: '2rem' }}>
                <h3 style={{ marginBottom: '1.5rem' }}>Recommended Learning Resources</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
                    {analysis.recommendations.map((rec, i) => (
                        <a key={i} href={rec.link} target="_blank" rel="noopener noreferrer"
                            style={{ textDecoration: 'none', color: 'inherit' }}>
                            <div style={{
                                background: 'rgba(15, 23, 42, 0.4)',
                                border: '1px solid #334155',
                                padding: '1rem',
                                borderRadius: '8px',
                                transition: 'all 0.2s'
                            }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.borderColor = 'var(--primary-color)';
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.borderColor = '#334155';
                                    e.currentTarget.style.transform = 'translateY(0)';
                                }}
                            >
                                <div style={{ color: '#ef4444', fontSize: '0.8rem', fontWeight: 'bold' }}>YOUTUBE</div>
                                <div style={{ fontSize: '1.1rem', fontWeight: '600', margin: '0.5rem 0' }}>Learn {rec.skill}</div>
                                <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Click to watch tutorials →</div>
                            </div>
                        </a>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AnalysisDetail;

import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

const ProjectRecommendations = () => {
    const { id } = useParams(); // analysis_id
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        fetchProjects();
    }, [id]);

    const fetchProjects = async () => {
        try {
            setLoading(true);
            // Get complete analysis
            const res = await api.get(`/analysis/${id}/complete`);

            if (res.data.project_recommendations) {
                setProjects(res.data.project_recommendations);
            } else {
                // Generate projects if not exists
                const missing = res.data.missing_skills || [];

                const projectsRes = await api.post('/recommend-projects', {
                    missing_skills: missing,
                    analysis_id: id
                });
                setProjects(projectsRes.data.project_recommendations);
            }
        } catch (err) {
            console.error('Error fetching projects:', err);
            setError('Failed to load project recommendations');
        } finally {
            setLoading(false);
        }
    };

    const getUniqueSkills = () => {
        const skills = new Set(projects.map(p => p.skill));
        return Array.from(skills);
    };

    const filteredProjects = filter === 'all'
        ? projects
        : projects.filter(p => p.skill === filter);

    const getDifficultyColor = (difficulty) => {
        if (difficulty.includes('Beginner')) return '#4ade80';
        if (difficulty.includes('Intermediate')) return '#facc15';
        return '#f87171';
    };

    if (loading) {
        return (
            <div className="page-container animate-fade-in">
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>Loading project recommendations...</p>
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

            <h1 style={{ marginBottom: '1rem' }}>🚀 Practice Projects</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                Hands-on projects to build your skills and portfolio
            </p>

            {/* Stats */}
            <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(59, 130, 246, 0.1))' }}>
                <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
                    <div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>
                            {projects.length}
                        </div>
                        <div style={{ color: 'var(--text-secondary)' }}>Total Projects</div>
                    </div>
                    <div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#4ade80' }}>
                            {getUniqueSkills().length}
                        </div>
                        <div style={{ color: 'var(--text-secondary)' }}>Skills Covered</div>
                    </div>
                </div>
            </div>

            {/* Filter */}
            <div style={{ marginBottom: '2rem' }}>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    <button
                        onClick={() => setFilter('all')}
                        className={filter === 'all' ? 'btn-primary' : 'btn-secondary'}
                        style={{ fontSize: '0.9rem' }}
                    >
                        All ({projects.length})
                    </button>
                    {getUniqueSkills().map(skill => (
                        <button
                            key={skill}
                            onClick={() => setFilter(skill)}
                            className={filter === skill ? 'btn-primary' : 'btn-secondary'}
                            style={{ fontSize: '0.9rem' }}
                        >
                            {skill}
                        </button>
                    ))}
                </div>
            </div>

            {/* Projects Grid */}
            {filteredProjects.length === 0 ? (
                <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>No projects available</p>
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem' }}>
                    {filteredProjects.map((project, index) => (
                        <div
                            key={index}
                            className="glass-panel"
                            style={{
                                padding: '1.5rem',
                                display: 'flex',
                                flexDirection: 'column',
                                transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                                cursor: 'pointer'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.transform = 'translateY(-5px)';
                                e.currentTarget.style.boxShadow = '0 10px 30px rgba(168, 85, 247, 0.3)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.transform = 'translateY(0)';
                                e.currentTarget.style.boxShadow = 'none';
                            }}
                        >
                            {/* Skill Tag */}
                            <div style={{ marginBottom: '1rem' }}>
                                <span style={{
                                    background: 'var(--primary-color)',
                                    color: 'white',
                                    padding: '4px 12px',
                                    borderRadius: '12px',
                                    fontSize: '0.8rem',
                                    fontWeight: 'bold'
                                }}>
                                    {project.skill}
                                </span>
                            </div>

                            {/* Project Title */}
                            <h3 style={{
                                margin: '0 0 1rem 0',
                                color: 'var(--text-primary)',
                                fontSize: '1.1rem',
                                lineHeight: '1.4',
                                flex: 1
                            }}>
                                {project.project}
                            </h3>

                            {/* Difficulty */}
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.5rem',
                                marginBottom: '1rem'
                            }}>
                                <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                    Difficulty:
                                </span>
                                <span style={{
                                    color: getDifficultyColor(project.difficulty),
                                    fontWeight: 'bold',
                                    fontSize: '0.9rem'
                                }}>
                                    {project.difficulty}
                                </span>
                            </div>

                            {/* Action Buttons */}
                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                <button
                                    className="btn-primary"
                                    style={{ flex: 1, fontSize: '0.9rem' }}
                                    onClick={() => window.open(`https://www.youtube.com/results?search_query=${encodeURIComponent(project.project + ' tutorial')}`, '_blank')}
                                >
                                    📺 Tutorial
                                </button>
                                <button
                                    className="btn-secondary"
                                    style={{ flex: 1, fontSize: '0.9rem' }}
                                    onClick={() => window.open(`https://github.com/search?q=${encodeURIComponent(project.skill)}`, '_blank')}
                                >
                                    💻 Examples
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Tips Section */}
            <div className="glass-panel" style={{ padding: '2rem', marginTop: '2rem', background: 'rgba(59, 130, 246, 0.1)' }}>
                <h3 style={{ marginBottom: '1rem' }}>💡 Project Tips</h3>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.8', margin: 0 }}>
                    <li>Start with beginner projects and gradually move to intermediate ones</li>
                    <li>Build each project from scratch to maximize learning</li>
                    <li>Add completed projects to your GitHub portfolio</li>
                    <li>Document your projects with README files</li>
                    <li>Share your projects on LinkedIn to showcase your skills</li>
                    <li>Iterate on projects to add more features and complexity</li>
                </ul>
            </div>

            {/* Call to Action */}
            <div className="glass-panel" style={{
                padding: '2rem',
                marginTop: '2rem',
                background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(59, 130, 246, 0.2))',
                textAlign: 'center'
            }}>
                <h3 style={{ marginBottom: '1rem' }}>🎯 Ready to Start Building?</h3>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                    Pick a project that interests you and start coding today!
                </p>
                <Link
                    to={`/learning-roadmap/${id}`}
                    className="btn-primary"
                    style={{ textDecoration: 'none', display: 'inline-block' }}
                >
                    📚 View Learning Roadmap
                </Link>
            </div>
        </div>
    );
};

export default ProjectRecommendations;

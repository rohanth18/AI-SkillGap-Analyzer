import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

const ResumeRewriter = () => {
    const [originalText, setOriginalText] = useState('');
    const [context, setContext] = useState('experience');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [history, setHistory] = useState([]);

    const handleRewrite = async () => {
        if (!originalText || originalText.trim().length < 10) {
            setError('Please enter at least 10 characters');
            return;
        }

        try {
            setLoading(true);
            setError('');

            const res = await api.post('/rewrite-section', {
                text: originalText,
                context: context
            });

            setResult(res.data);
            setHistory([res.data, ...history.slice(0, 4)]); // Keep last 5
        } catch (err) {
            console.error('Error rewriting:', err);
            setError(err.response?.data?.error || 'Failed to rewrite text');
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        alert('Copied to clipboard!');
    };

    const useExample = (example) => {
        setOriginalText(example);
        setResult(null);
    };

    const examples = [
        "Worked on Python projects and managed data.",
        "Helped with website development and testing.",
        "Was responsible for database management and queries.",
        "Used machine learning for predictions and analysis."
    ];

    return (
        <div className="page-container animate-fade-in">
            <div style={{ marginBottom: '2rem' }}>
                <Link to="/" style={{ color: 'var(--primary-color)', textDecoration: 'none' }}>
                    ← Back to Dashboard
                </Link>
            </div>

            <h1 style={{ marginBottom: '1rem' }}>✨ AI Resume Rewriter</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                Transform your resume text with stronger action verbs and professional language
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
                {/* Input Section */}
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1rem' }}>📝 Original Text</h3>

                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
                            Context:
                        </label>
                        <select
                            value={context}
                            onChange={(e) => setContext(e.target.value)}
                            className="input-field"
                            style={{ width: '100%' }}
                        >
                            <option value="experience">Work Experience</option>
                            <option value="summary">Professional Summary</option>
                            <option value="skills">Skills Description</option>
                        </select>
                    </div>

                    <textarea
                        value={originalText}
                        onChange={(e) => setOriginalText(e.target.value)}
                        placeholder="Enter your resume text here..."
                        className="input-field"
                        style={{
                            width: '100%',
                            minHeight: '200px',
                            resize: 'vertical',
                            fontFamily: 'inherit'
                        }}
                    />

                    <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
                        <small style={{ color: 'var(--text-secondary)' }}>
                            {originalText.length} characters
                        </small>
                    </div>

                    {error && (
                        <div style={{
                            padding: '1rem',
                            background: 'rgba(248, 113, 113, 0.1)',
                            border: '1px solid #f87171',
                            borderRadius: '8px',
                            marginBottom: '1rem',
                            color: '#f87171'
                        }}>
                            {error}
                        </div>
                    )}

                    <button
                        onClick={handleRewrite}
                        disabled={loading || !originalText}
                        className="btn-primary"
                        style={{ width: '100%', marginBottom: '1rem' }}
                    >
                        {loading ? '✨ Rewriting...' : '✨ Rewrite with AI'}
                    </button>

                    <button
                        onClick={() => { setOriginalText(''); setResult(null); setError(''); }}
                        className="btn-secondary"
                        style={{ width: '100%' }}
                    >
                        Clear
                    </button>
                </div>

                {/* Output Section */}
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1rem' }}>✨ Improved Text</h3>

                    {result ? (
                        <>
                            <div style={{
                                background: 'rgba(74, 222, 128, 0.1)',
                                border: '1px solid rgba(74, 222, 128, 0.3)',
                                borderRadius: '8px',
                                padding: '1.5rem',
                                marginBottom: '1rem',
                                minHeight: '200px'
                            }}>
                                <p style={{ margin: 0, lineHeight: '1.6', color: 'var(--text-primary)' }}>
                                    {result.rewritten}
                                </p>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                    <span style={{ color: 'var(--text-secondary)' }}>Improvement Score:</span>
                                    <span style={{
                                        fontSize: '1.5rem',
                                        fontWeight: 'bold',
                                        color: result.score_improvement > 50 ? '#4ade80' : '#facc15'
                                    }}>
                                        +{result.score_improvement}%
                                    </span>
                                </div>
                                <div style={{
                                    width: '100%',
                                    height: '8px',
                                    background: 'rgba(255,255,255,0.1)',
                                    borderRadius: '4px',
                                    overflow: 'hidden'
                                }}>
                                    <div style={{
                                        width: `${result.score_improvement}%`,
                                        height: '100%',
                                        background: result.score_improvement > 50 ? '#4ade80' : '#facc15',
                                        transition: 'width 1s ease-out'
                                    }}></div>
                                </div>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <h4 style={{ color: 'var(--primary-color)', marginBottom: '0.5rem' }}>Improvements Made:</h4>
                                <ul style={{ margin: 0, paddingLeft: '1.5rem', lineHeight: '1.8' }}>
                                    {result.improvements.map((imp, i) => (
                                        <li key={i} style={{ color: 'var(--text-secondary)' }}>{imp}</li>
                                    ))}
                                </ul>
                            </div>

                            <button
                                onClick={() => copyToClipboard(result.rewritten)}
                                className="btn-primary"
                                style={{ width: '100%' }}
                            >
                                📋 Copy to Clipboard
                            </button>
                        </>
                    ) : (
                        <div style={{
                            minHeight: '200px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'var(--text-secondary)',
                            textAlign: 'center'
                        }}>
                            {loading ? 'Rewriting your text...' : 'Your improved text will appear here'}
                        </div>
                    )}
                </div>
            </div>

            {/* Examples */}
            <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
                <h3 style={{ marginBottom: '1rem' }}>💡 Try These Examples</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
                    {examples.map((example, i) => (
                        <div
                            key={i}
                            onClick={() => useExample(example)}
                            style={{
                                padding: '1rem',
                                background: 'rgba(255,255,255,0.05)',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                border: '1px solid rgba(255,255,255,0.1)',
                                transition: 'all 0.2s ease'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.background = 'rgba(168, 85, 247, 0.1)';
                                e.currentTarget.style.borderColor = 'var(--primary-color)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                                e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)';
                            }}
                        >
                            <small style={{ color: 'var(--text-secondary)' }}>{example}</small>
                        </div>
                    ))}
                </div>
            </div>

            {/* History */}
            {history.length > 0 && (
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1rem' }}>📜 Recent Rewrites</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {history.map((item, i) => (
                            <div
                                key={i}
                                style={{
                                    padding: '1rem',
                                    background: 'rgba(255,255,255,0.05)',
                                    borderRadius: '8px',
                                    border: '1px solid rgba(255,255,255,0.1)'
                                }}
                            >
                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                    <div>
                                        <small style={{ color: 'var(--text-secondary)' }}>Original:</small>
                                        <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem' }}>{item.original}</p>
                                    </div>
                                    <div>
                                        <small style={{ color: '#4ade80' }}>Improved (+{item.score_improvement}%):</small>
                                        <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem', color: '#4ade80' }}>{item.rewritten}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Tips */}
            <div className="glass-panel" style={{ padding: '2rem', background: 'rgba(59, 130, 246, 0.1)' }}>
                <h3 style={{ marginBottom: '1rem' }}>💡 Writing Tips</h3>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.8', margin: 0 }}>
                    <li>Start bullet points with strong action verbs (Developed, Implemented, Led)</li>
                    <li>Include quantifiable metrics whenever possible (improved by 40%, managed 10+ projects)</li>
                    <li>Be specific about technologies and tools used</li>
                    <li>Focus on achievements and impact, not just responsibilities</li>
                    <li>Use professional language while keeping it concise</li>
                </ul>
            </div>
        </div>
    );
};

export default ResumeRewriter;

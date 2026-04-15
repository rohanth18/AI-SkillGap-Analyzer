import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const UploadResume = ({ user }) => {
    const [file, setFile] = useState(null);
    const [roles, setRoles] = useState([]);
    const [selectedRole, setSelectedRole] = useState('');
    const [manualSkills, setManualSkills] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchRoles = async () => {
            try {
                const res = await api.get('/roles');
                setRoles(res.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchRoles();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file || !selectedRole) return;

        setLoading(true);
        try {
            // 1. Upload File
            const formData = new FormData();
            formData.append('file', file);
            formData.append('user_id', user.id);

            const uploadRes = await api.post('/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const resumeId = uploadRes.data.resume_id;

            // 2. Analyze
            const manualSkillsList = manualSkills.split(',').map(s => s.trim()).filter(Boolean);

            const analyzeRes = await api.post('/analyze', {
                user_id: user.id,
                resume_id: resumeId,
                role_id: selectedRole,
                manual_skills: manualSkillsList
            });

            navigate(`/analysis/${analyzeRes.data.analysis_id}`);

        } catch (err) {
            console.error(err);
            alert('Analysis failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container animate-fade-in">
            <div className="glass-panel" style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
                <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>New Skill Analysis</h2>

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Job Role</label>
                        <select
                            className="input-field"
                            value={selectedRole}
                            onChange={(e) => setSelectedRole(e.target.value)}
                            required
                        >
                            <option value="">Select a target role...</option>
                            {roles.map(r => (
                                <option key={r.id} value={r.id}>{r.name}</option>
                            ))}
                        </select>
                    </div>

                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Resume (PDF/Text)</label>
                        <input
                            className="input-field"
                            type="file"
                            accept=".pdf,.txt"
                            onChange={(e) => setFile(e.target.files[0])}
                            required
                        />
                    </div>

                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Manual Skills (Optional, comma separated)</label>
                        <input
                            className="input-field"
                            type="text"
                            placeholder="e.g. React, Python, Project Management"
                            value={manualSkills}
                            onChange={(e) => setManualSkills(e.target.value)}
                        />
                    </div>



                    <button disabled={loading} className="btn-primary" style={{ width: '100%', opacity: loading ? 0.7 : 1 }} type="submit">
                        {loading ? 'Analyzing...' : 'Start Analysis'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default UploadResume;

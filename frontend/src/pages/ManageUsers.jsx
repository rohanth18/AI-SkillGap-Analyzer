import React, { useEffect, useState } from 'react';
import api from '../api';

const ManageUsers = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const res = await api.get('/admin/users');
                setUsers(res.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchUsers();
    }, []);

    const handleDeleteUser = async (id) => {
        if (!window.confirm("Are you sure you want to delete this user? All their data (resumes, analyses, etc.) will be permanently removed.")) {
            return;
        }

        try {
            await api.delete(`/admin/users/${id}`);
            // Remove from state
            setUsers(users.filter(u => u.id !== id));
        } catch (err) {
            alert(err.response?.data?.error || "Failed to delete user");
            console.error(err);
        }
    };

    return (
        <div className="page-container animate-fade-in">
            <h1 style={{ marginBottom: '2rem' }}>Manage Users</h1>

            <div className="glass-panel" style={{ padding: '2rem', overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', color: 'var(--text-primary)' }}>
                    <thead>
                        <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>ID</th>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Name</th>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Email</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>Role</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>App Activity</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>Analyses</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(u => (
                            <tr key={u.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <td style={{ padding: '1rem' }}>{u.id}</td>
                                <td style={{ padding: '1rem' }}>{u.name}</td>
                                <td style={{ padding: '1rem' }}>{u.email}</td>
                                <td style={{ padding: '1rem', textAlign: 'center' }}>
                                    {u.is_admin ?
                                        <span style={{ color: '#f87171', border: '1px solid #f87171', padding: '2px 8px', borderRadius: '4px' }}>Admin</span>
                                        :
                                        <span style={{ color: '#94a3b8', border: '1px solid #94a3b8', padding: '2px 8px', borderRadius: '4px' }}>User</span>}
                                </td>
                                <td style={{ padding: '1rem', textAlign: 'center' }}>
                                    {u.resume_count > 0 ?
                                        <span style={{ color: '#4ade80' }}>Active ({u.resume_count} uploads)</span>
                                        :
                                        <span style={{ color: '#64748b' }}>Inactive</span>}
                                </td>
                                <td style={{ padding: '1rem', textAlign: 'center' }}>
                                    {u.analysis_count}
                                </td>
                                <td style={{ padding: '1rem', textAlign: 'center' }}>
                                    <button
                                        onClick={() => handleDeleteUser(u.id)}
                                        className="btn-secondary"
                                        style={{
                                            padding: '4px 12px',
                                            fontSize: '0.8rem',
                                            background: 'rgba(248, 113, 113, 0.1)',
                                            color: '#f87171',
                                            borderColor: 'rgba(248, 113, 113, 0.3)'
                                        }}
                                        onMouseEnter={(e) => e.target.style.background = 'rgba(248, 113, 113, 0.2)'}
                                        onMouseLeave={(e) => e.target.style.background = 'rgba(248, 113, 113, 0.1)'}
                                    >
                                        Remove
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ManageUsers;

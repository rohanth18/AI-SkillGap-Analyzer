import React, { useEffect, useState } from 'react';
import api from '../api';

const RoleManagement = () => {
    const [roles, setRoles] = useState([]);
    // Separate create form state
    const [newRole, setNewRole] = useState({ name: '', description: '', skills: '' });
    // Separate edit form state
    const [editingRole, setEditingRole] = useState(null); // ID of role being edited
    const [editForm, setEditForm] = useState({ name: '', description: '', skills: '' });
    const [loading, setLoading] = useState(false);

    const fetchRoles = async () => {
        try {
            const res = await api.get('/roles');
            setRoles(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchRoles();
    }, []);

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure?')) return;
        try {
            await api.delete(`/admin/roles/${id}`);
            fetchRoles();
        } catch (err) {
            console.error(err);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const skillsList = newRole.skills.split(',').map(s => s.trim()).filter(Boolean);
            await api.post('/admin/roles', { ...newRole, skills: skillsList });
            setNewRole({ name: '', description: '', skills: '' });
            fetchRoles();
        } catch (err) {
            console.error(err);
            alert('Error adding role: ' + (err.response?.data?.error || err.message));
        } finally {
            setLoading(false);
        }
    };

    const startEdit = (role) => {
        setEditingRole(role.id);
        setEditForm({
            name: role.name,
            description: role.description,
            skills: role.skills.join(', ')
        });
    };

    const cancelEdit = () => {
        setEditingRole(null);
        setEditForm({ name: '', description: '', skills: '' });
    };

    const handleUpdate = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            // New EndPoint -> /admin/roles/:id (PUT)
            await api.put(`/admin/roles/${editingRole}`, {
                ...editForm,
                skills: editForm.skills.split(',').map(s => s.trim()).filter(Boolean)
            });
            setEditingRole(null);
            fetchRoles();
        } catch (err) {
            alert('Update failed: ' + (err.response?.data?.error || err.message));
        } finally {
            setLoading(false);
        }
    };

    const handleSeed = async () => {
        setLoading(true);
        try {
            const res = await api.post('/seed');
            alert(res.data.message);
            fetchRoles();
        } catch (err) {
            alert('Seed failed');
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="page-container animate-fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Manage Job Roles</h1>
                <button onClick={handleSeed} className="btn-secondary">Seed from CSV</button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>

                {/* CREATE PANEL */}
                <div className="glass-panel" style={{ padding: '2rem', height: 'fit-content' }}>
                    <h3 style={{ marginBottom: '1.5rem' }}>Add New Role</h3>
                    <form onSubmit={handleCreate}>
                        <input
                            className="input-field"
                            type="text"
                            placeholder="Role Name"
                            value={newRole.name}
                            onChange={e => setNewRole({ ...newRole, name: e.target.value })}
                            required
                        />
                        <textarea
                            className="input-field"
                            placeholder="Description"
                            value={newRole.description}
                            onChange={e => setNewRole({ ...newRole, description: e.target.value })}
                            rows="3"
                        />
                        <textarea
                            className="input-field"
                            placeholder="Skills (comma separated)"
                            value={newRole.skills}
                            onChange={e => setNewRole({ ...newRole, skills: e.target.value })}
                            rows="4"
                            required
                        />
                        <button disabled={loading} className="btn-primary" style={{ width: '100%' }} type="submit">
                            {loading ? 'Saving...' : 'Add Role'}
                        </button>
                    </form>
                </div>

                {/* LIST PANEL */}
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1.5rem' }}>Existing Roles ({roles.length})</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {roles.map(r => (
                            <div key={r.id} style={{
                                border: '1px solid rgba(255,255,255,0.1)',
                                padding: '1rem',
                                borderRadius: '8px',
                                background: 'rgba(0,0,0,0.2)'
                            }}>
                                {editingRole === r.id ? (
                                    /* EDIT MODE */
                                    <form onSubmit={handleUpdate} style={{ display: 'grid', gap: '0.5rem' }}>
                                        <input
                                            className="input-field"
                                            value={editForm.name}
                                            onChange={e => setEditForm({ ...editForm, name: e.target.value })}
                                        />
                                        <textarea
                                            className="input-field"
                                            value={editForm.description}
                                            onChange={e => setEditForm({ ...editForm, description: e.target.value })}
                                            rows="2"
                                        />
                                        <textarea
                                            className="input-field"
                                            value={editForm.skills}
                                            onChange={e => setEditForm({ ...editForm, skills: e.target.value })}
                                            rows="3"
                                        />
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            <button className="btn-primary" type="submit">Save</button>
                                            <button className="btn-secondary" type="button" onClick={cancelEdit}>Cancel</button>
                                        </div>
                                    </form>
                                ) : (
                                    /* VIEW MODE */
                                    <>
                                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                            <span style={{ fontWeight: 'bold', fontSize: '1.1rem', color: 'var(--primary-color)' }}>{r.name}</span>
                                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                                <button onClick={() => startEdit(r)} style={{ background: 'transparent', border: '1px solid var(--primary-color)', color: 'var(--primary-color)', cursor: 'pointer', padding: '2px 8px', borderRadius: '4px' }}>Edit</button>
                                                <button onClick={() => handleDelete(r.id)} style={{ background: 'transparent', border: 'none', color: '#f87171', cursor: 'pointer' }}>Delete</button>
                                            </div>
                                        </div>
                                        <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', margin: '0.5rem 0' }}>{r.description}</div>
                                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem' }}>
                                            {r.skills.slice(0, 15).map((s, i) => (
                                                <span key={i} style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '10px', fontSize: '0.8rem' }}>{s}</span>
                                            ))}
                                            {r.skills.length > 15 && <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>+{r.skills.length - 15} more</span>}
                                        </div>
                                    </>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RoleManagement;

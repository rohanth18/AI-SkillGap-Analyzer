import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = ({ user, onLogout }) => {
    const navigate = useNavigate();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const handleLogout = () => {
        onLogout();
        setMobileMenuOpen(false);
        navigate('/');
    };

    const toggleMobileMenu = () => {
        setMobileMenuOpen(!mobileMenuOpen);
    };

    return (
        <nav className="navbar">
            <Link to="/" className="nav-logo">
                SkillGap AI
            </Link>

            {/* Hamburger Menu Button */}
            <button className="mobile-menu-btn" onClick={toggleMobileMenu}>
                <span className={mobileMenuOpen ? 'hamburger open' : 'hamburger'}>
                    <span></span>
                    <span></span>
                    <span></span>
                </span>
            </button>

            <div className={`nav-links ${mobileMenuOpen ? 'mobile-open' : ''}`}>
                {user ? (
                    // Logged-in user menu
                    <>
                        <Link to="/" onClick={() => setMobileMenuOpen(false)}>Home</Link>
                        {user.is_admin ? (
                            <>
                                <Link to="/admin/dashboard" onClick={() => setMobileMenuOpen(false)}>Dashboard</Link>
                                <Link to="/admin/roles" onClick={() => setMobileMenuOpen(false)}>Roles</Link>
                                <Link to="/admin/users" onClick={() => setMobileMenuOpen(false)}>Users</Link>
                                <Link to="/admin/insights" onClick={() => setMobileMenuOpen(false)}>Insights</Link>
                            </>
                        ) : (
                            <>
                                <Link to="/dashboard" onClick={() => setMobileMenuOpen(false)}>My Analyses</Link>
                                <Link to="/upload" onClick={() => setMobileMenuOpen(false)}>New Analysis</Link>

                            </>
                        )}
                        <a href="#" onClick={handleLogout} style={{ color: '#f87171' }}>Logout</a>
                    </>
                ) : (
                    // Public menu (not logged in)
                    <>
                        <Link to="/" onClick={() => setMobileMenuOpen(false)}>Home</Link>
                        <Link to="/login" onClick={() => setMobileMenuOpen(false)}>Features</Link>
                        <Link to="/login" className="nav-btn-login" onClick={() => setMobileMenuOpen(false)}>
                            Login
                        </Link>
                        <Link to="/register" className="nav-btn-register" onClick={() => setMobileMenuOpen(false)}>
                            Get Started
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;


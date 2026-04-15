import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';
import './HomePage.css';

const HomePage = () => {
    const navigate = useNavigate();
    const [typedText, setTypedText] = useState('');
    const [statsVisible, setStatsVisible] = useState(false);
    const [stats, setStats] = useState({ users: 0, analyses: 0, roles: 0 });
    const [user, setUser] = useState(null);

    // Check if user is logged in
    useEffect(() => {
        const storedUser = localStorage.getItem('skillgap_user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
    }, []);

    // Fetch real stats from backend
    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await api.get('/admin/stats');
                setStats({
                    users: response.data.total_users || 0,
                    analyses: response.data.total_analyses || 0,
                    roles: response.data.total_roles || 0
                });
            } catch (error) {
                console.log('Could not fetch stats, using defaults');
            }
        };
        fetchStats();
    }, []);

    const fullText = "Analyzing your skills... predicting your career path...";

    // Typing animation effect
    useEffect(() => {
        let index = 0;
        const timer = setInterval(() => {
            if (index <= fullText.length) {
                setTypedText(fullText.slice(0, index));
                index++;
            } else {
                clearInterval(timer);
            }
        }, 50);

        return () => clearInterval(timer);
    }, []);

    // Intersection observer for stats animation
    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting) {
                    setStatsVisible(true);
                }
            },
            { threshold: 0.5 }
        );

        const statsElement = document.getElementById('stats-section');
        if (statsElement) {
            observer.observe(statsElement);
        }

        return () => observer.disconnect();
    }, []);

    const features = [
        {
            icon: '🤖',
            title: 'AI Resume Skill Extraction',
            description: 'Advanced NLP and machine learning to extract skills from your resume with 95% accuracy'
        },
        {
            icon: '🎯',
            title: 'Job Role Recommendations',
            description: 'ML-powered predictions suggest the top 3 job roles that match your skill profile'
        },
        {
            icon: '📚',
            title: 'Personalized Career Roadmap',
            description: 'Week-by-week learning plans tailored to your missing skills and career goals'
        },
        {
            icon: '📊',
            title: 'Admin Analytics Dashboard',
            description: 'Deep insights into skill gaps, trends, and workforce analytics'
        }
    ];

    const steps = [
        { number: '01', title: 'Upload Resume', description: 'Upload your resume in PDF format', icon: '📄' },
        { number: '02', title: 'AI Extracts Skills', description: 'Our AI analyzes and extracts your skills', icon: '🔍' },
        { number: '03', title: 'View Skill Gaps', description: 'See your confidence score and missing skills', icon: '📈' },
        { number: '04', title: 'Receive Learning Path', description: 'Get personalized roadmap and projects', icon: '🚀' }
    ];

    const testimonials = [
        {
            name: 'Sarah Johnson',
            role: 'Software Developer',
            text: 'This platform helped me identify my skill gaps and land my dream job at a top tech company!',
            rating: 5
        },
        {
            name: 'Michael Chen',
            role: 'Data Scientist',
            text: 'The personalized learning roadmap was exactly what I needed. Highly recommended!',
            rating: 5
        },
        {
            name: 'Emily Rodriguez',
            role: 'DevOps Engineer',
            text: 'Amazing AI-powered insights! The job role recommendations were spot-on.',
            rating: 5
        }
    ];

    const AnimatedCounter = ({ end, suffix = '' }) => {
        const [count, setCount] = useState(0);

        useEffect(() => {
            if (statsVisible) {
                let start = 0;
                const duration = 2000;
                const increment = end / (duration / 16);

                const timer = setInterval(() => {
                    start += increment;
                    if (start >= end) {
                        setCount(end);
                        clearInterval(timer);
                    } else {
                        setCount(Math.floor(start));
                    }
                }, 16);

                return () => clearInterval(timer);
            }
        }, [statsVisible, end]);

        return <span>{count}{suffix}</span>;
    };

    return (
        <div className="homepage">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-background">
                    <div className="gradient-orb orb-1"></div>
                    <div className="gradient-orb orb-2"></div>
                    <div className="gradient-orb orb-3"></div>
                </div>

                <div className="hero-content">
                    <div className="hero-text">
                        <h1 className="hero-title">
                            AI-Based Skill Gap Analyzer and
                            <span className="gradient-text"> Personalized Learning Recommendation System</span>
                        </h1>
                        <p className="hero-subtitle">
                            Upload your resume, detect your skills, uncover your gaps, and get a personalized roadmap to succeed.
                        </p>
                        <div className="ai-typing">
                            <span className="typing-cursor">💡</span> {typedText}
                            <span className="cursor-blink">|</span>
                        </div>
                        <div className="hero-buttons">
                            {user ? (
                                <>
                                    <Link to="/upload" className="btn-hero-primary">
                                        Analyze Your Resume
                                        <span className="btn-arrow">→</span>
                                    </Link>
                                    <Link to="/dashboard" className="btn-hero-secondary">
                                        View Dashboard
                                    </Link>
                                </>
                            ) : (
                                <>
                                    <Link to="/register" className="btn-hero-primary">
                                        Get Started Free
                                        <span className="btn-arrow">→</span>
                                    </Link>
                                    <Link to="/login" className="btn-hero-secondary">
                                        Login to Analyze
                                    </Link>
                                </>
                            )}
                        </div>
                    </div>

                    <div className="hero-illustration">
                        <div className="illustration-card">
                            <div className="illustration-content">
                                <div className="code-lines">
                                    <div className="code-line"></div>
                                    <div className="code-line short"></div>
                                    <div className="code-line"></div>
                                    <div className="code-line medium"></div>
                                    <div className="code-line"></div>
                                </div>
                                <div className="ai-brain">🧠</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="stats-section" id="stats-section">
                <div className="stats-container">
                    <div className="stat-item">
                        <div className="stat-number">
                            <AnimatedCounter end={stats.users} suffix="+" />
                        </div>
                        <div className="stat-label">Users Registered</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number">
                            <AnimatedCounter end={stats.analyses} suffix="+" />
                        </div>
                        <div className="stat-label">Analyses Completed</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number">
                            <AnimatedCounter end={stats.roles} suffix="+" />
                        </div>
                        <div className="stat-label">Job Roles Supported</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number">
                            <AnimatedCounter end={95} suffix="%" />
                        </div>
                        <div className="stat-label">AI Accuracy</div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="section-header">
                    <h2 className="section-title">Powerful Features</h2>
                    <p className="section-subtitle">Everything you need to advance your career</p>
                </div>

                <div className="features-grid">
                    {features.map((feature, index) => (
                        <div key={index} className="feature-card" style={{ animationDelay: `${index * 0.1}s` }}>
                            <div className="feature-icon">{feature.icon}</div>
                            <h3 className="feature-title">{feature.title}</h3>
                            <p className="feature-description">{feature.description}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* How It Works Section */}
            <section className="how-it-works-section">
                <div className="section-header">
                    <h2 className="section-title">How It Works</h2>
                    <p className="section-subtitle">Get started in 4 simple steps</p>
                </div>

                <div className="steps-container">
                    {steps.map((step, index) => (
                        <div key={index} className="step-item">
                            <div className="step-number">{step.number}</div>
                            <div className="step-icon">{step.icon}</div>
                            <h3 className="step-title">{step.title}</h3>
                            <p className="step-description">{step.description}</p>
                            {index < steps.length - 1 && <div className="step-connector"></div>}
                        </div>
                    ))}
                </div>
            </section>

            {/* Demo Section */}
            <section className="demo-section">
                <div className="demo-content">
                    <div className="demo-text">
                        <h2 className="demo-title">See It In Action</h2>
                        <p className="demo-description">
                            Experience the power of AI-driven career insights. Our platform has helped thousands of professionals identify their strengths and achieve their career goals.
                        </p>
                        <Link to={user ? "/upload" : "/login"} className="btn-demo">
                            {user ? "Start Analysis" : "Try Live Demo"}
                            <span className="btn-arrow">→</span>
                        </Link>
                    </div>
                    <div className="demo-screenshot">
                        <div className="screenshot-placeholder">
                            <div className="screenshot-header">
                                <div className="screenshot-dots">
                                    <span></span><span></span><span></span>
                                </div>
                            </div>
                            <div className="screenshot-content">
                                <div className="chart-placeholder">
                                    <div className="chart-bar" style={{ height: '60%' }}></div>
                                    <div className="chart-bar" style={{ height: '80%' }}></div>
                                    <div className="chart-bar" style={{ height: '45%' }}></div>
                                    <div className="chart-bar" style={{ height: '90%' }}></div>
                                    <div className="chart-bar" style={{ height: '70%' }}></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="testimonials-section">
                <div className="section-header">
                    <h2 className="section-title">What Our Users Say</h2>
                    <p className="section-subtitle">Join thousands of satisfied professionals</p>
                </div>

                <div className="testimonials-grid">
                    {testimonials.map((testimonial, index) => (
                        <div key={index} className="testimonial-card">
                            <div className="testimonial-rating">
                                {'⭐'.repeat(testimonial.rating)}
                            </div>
                            <p className="testimonial-text">"{testimonial.text}"</p>
                            <div className="testimonial-author">
                                <div className="author-avatar">{testimonial.name[0]}</div>
                                <div className="author-info">
                                    <div className="author-name">{testimonial.name}</div>
                                    <div className="author-role">{testimonial.role}</div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <div className="cta-content">
                    <h2 className="cta-title">Ready to Transform Your Career?</h2>
                    <p className="cta-subtitle">Join thousands of professionals who have discovered their true potential</p>
                    <Link to="/register" className="btn-cta">
                        Get Started Now - It's Free
                        <span className="btn-arrow">→</span>
                    </Link>
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <div className="footer-content">
                    <div className="footer-section">
                        <h3 className="footer-logo">SkillGap AI</h3>
                        <p className="footer-tagline">Empowering careers through AI-driven insights</p>
                    </div>

                    <div className="footer-section">
                        <h4 className="footer-heading">Product</h4>
                        <ul className="footer-links">
                            <li><Link to="/login">Features</Link></li>
                            <li><Link to="/register">Pricing</Link></li>
                            <li><Link to="/login">Demo</Link></li>
                        </ul>
                    </div>

                    <div className="footer-section">
                        <h4 className="footer-heading">Company</h4>
                        <ul className="footer-links">
                            <li><a href="#about">About</a></li>
                            <li><a href="mailto:contact@skillgap.ai">Contact</a></li>
                            <li><a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a></li>
                        </ul>
                    </div>

                    <div className="footer-section">
                        <h4 className="footer-heading">Legal</h4>
                        <ul className="footer-links">
                            <li><a href="#privacy">Privacy Policy</a></li>
                            <li><a href="#terms">Terms of Service</a></li>
                        </ul>
                    </div>
                </div>

                <div className="footer-bottom">
                    <p>&copy; 2026 SkillGap AI. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default HomePage;

import React, { useState } from 'react';
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
} from 'chart.js';
import { Radar, Bar, Doughnut, PolarArea } from 'react-chartjs-2';

ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement
);

const SkillGapChart = ({ missing, present }) => {
    const [chartType, setChartType] = useState('radar'); // radar, bar, doughnut, polar, progress

    const allSkills = [...present, ...missing];
    const displaySkills = allSkills.slice(0, 15);

    // Radar Chart Data
    const radarData = {
        labels: displaySkills,
        datasets: [
            {
                label: 'Your Skills',
                data: displaySkills.map(s => present.includes(s) ? 100 : 0),
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: '#6366f1',
                borderWidth: 2,
            },
            {
                label: 'Required Level',
                data: displaySkills.map(() => 100),
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderColor: '#94a3b8',
                borderWidth: 1,
                borderDash: [5, 5],
            },
        ],
    };

    // Bar Chart Data (Horizontal)
    const barData = {
        labels: displaySkills,
        datasets: [
            {
                label: 'Your Skills',
                data: displaySkills.map(s => present.includes(s) ? 100 : 0),
                backgroundColor: displaySkills.map(s =>
                    present.includes(s) ? 'rgba(74, 222, 128, 0.8)' : 'rgba(248, 113, 113, 0.8)'
                ),
                borderColor: displaySkills.map(s =>
                    present.includes(s) ? '#4ade80' : '#f87171'
                ),
                borderWidth: 1,
            },
        ],
    };

    // Doughnut Chart Data (Skills Distribution)
    const doughnutData = {
        labels: ['Skills You Have', 'Skills Missing'],
        datasets: [
            {
                data: [present.length, missing.length],
                backgroundColor: [
                    'rgba(74, 222, 128, 0.8)',
                    'rgba(248, 113, 113, 0.8)',
                ],
                borderColor: [
                    '#4ade80',
                    '#f87171',
                ],
                borderWidth: 2,
            },
        ],
    };

    // Polar Area Chart Data
    const polarData = {
        labels: displaySkills,
        datasets: [
            {
                label: 'Skill Proficiency',
                data: displaySkills.map(s => present.includes(s) ? 100 : 0),
                backgroundColor: displaySkills.map((s, i) => {
                    const hue = (i * 360) / displaySkills.length;
                    return present.includes(s)
                        ? `hsla(${hue}, 70%, 60%, 0.6)`
                        : 'rgba(248, 113, 113, 0.3)';
                }),
                borderColor: displaySkills.map((s, i) => {
                    const hue = (i * 360) / displaySkills.length;
                    return present.includes(s)
                        ? `hsla(${hue}, 70%, 60%, 1)`
                        : '#f87171';
                }),
                borderWidth: 2,
            },
        ],
    };

    const radarOptions = {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            r: {
                angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                pointLabels: {
                    color: '#94a3b8',
                    font: { size: 10 }
                },
                ticks: {
                    display: false,
                    max: 100,
                    min: 0,
                    stepSize: 20
                }
            }
        },
        plugins: {
            legend: {
                labels: { color: '#f8fafc', font: { size: 11 } }
            }
        }
    };

    const barOptions = {
        indexAxis: 'y',
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.parsed.x === 100 ? 'You have this skill' : 'Skill missing';
                    }
                }
            }
        },
        scales: {
            x: {
                max: 100,
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#94a3b8' }
            },
            y: {
                grid: { display: false },
                ticks: { color: '#94a3b8' }
            }
        }
    };

    const doughnutOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#f8fafc', padding: 20, font: { size: 14 } }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((context.parsed / total) * 100).toFixed(1);
                        return `${context.label}: ${context.parsed} (${percentage}%)`;
                    }
                }
            }
        }
    };

    const polarOptions = {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            r: {
                ticks: {
                    display: false,
                    max: 100
                },
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                pointLabels: {
                    color: '#94a3b8',
                    font: { size: 11 }
                }
            }
        }
    };

    const renderChart = () => {
        switch (chartType) {
            case 'radar':
                return <Radar data={radarData} options={radarOptions} />;
            case 'bar':
                return <Bar data={barData} options={barOptions} />;
            case 'doughnut':
                return <Doughnut data={doughnutData} options={doughnutOptions} />;
            case 'polar':
                return <PolarArea data={polarData} options={polarOptions} />;
            case 'progress':
                return (
                    <div style={{ overflowY: 'auto', maxHeight: '300px', paddingRight: '10px' }}>
                        {displaySkills.map((skill, index) => {
                            const hasSkill = present.includes(skill);
                            const progress = hasSkill ? 100 : 0;
                            return (
                                <div key={index} style={{ marginBottom: '15px' }}>
                                    <div style={{
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        marginBottom: '5px',
                                        fontSize: '0.9rem'
                                    }}>
                                        <span style={{ color: hasSkill ? '#4ade80' : '#f87171' }}>
                                            {skill}
                                        </span>
                                        <span style={{
                                            color: hasSkill ? '#4ade80' : '#f87171',
                                            fontWeight: 'bold'
                                        }}>
                                            {hasSkill ? '✓' : '✗'}
                                        </span>
                                    </div>
                                    <div style={{
                                        width: '100%',
                                        height: '8px',
                                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                                        borderRadius: '4px',
                                        overflow: 'hidden'
                                    }}>
                                        <div style={{
                                            width: `${progress}%`,
                                            height: '100%',
                                            backgroundColor: hasSkill ? '#4ade80' : '#f87171',
                                            transition: 'width 0.3s ease',
                                            borderRadius: '4px'
                                        }} />
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                );
            default:
                return <Radar data={radarData} options={radarOptions} />;
        }
    };

    return (
        <div>
            {/* Chart Type Selector */}
            <div style={{
                display: 'flex',
                gap: '8px',
                marginBottom: '15px',
                flexWrap: 'wrap'
            }}>
                {[
                    { type: 'radar', icon: '📊', label: 'Radar' },
                    { type: 'bar', icon: '📈', label: 'Bar' },
                    { type: 'doughnut', icon: '🍩', label: 'Doughnut' },
                    { type: 'polar', icon: '🎯', label: 'Polar' },
                    { type: 'progress', icon: '📉', label: 'Progress' },
                ].map(({ type, icon, label }) => (
                    <button
                        key={type}
                        onClick={() => setChartType(type)}
                        style={{
                            padding: '6px 12px',
                            borderRadius: '6px',
                            border: chartType === type ? '2px solid var(--primary-color)' : '1px solid #334155',
                            background: chartType === type ? 'rgba(168, 85, 247, 0.2)' : 'rgba(15, 23, 42, 0.4)',
                            color: chartType === type ? 'var(--primary-color)' : '#94a3b8',
                            cursor: 'pointer',
                            fontSize: '0.85rem',
                            transition: 'all 0.2s',
                            fontWeight: chartType === type ? 'bold' : 'normal'
                        }}
                        onMouseEnter={(e) => {
                            if (chartType !== type) {
                                e.currentTarget.style.borderColor = 'var(--primary-color)';
                                e.currentTarget.style.color = '#f8fafc';
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (chartType !== type) {
                                e.currentTarget.style.borderColor = '#334155';
                                e.currentTarget.style.color = '#94a3b8';
                            }
                        }}
                    >
                        {icon} {label}
                    </button>
                ))}
            </div>

            {/* Chart Display */}
            <div style={{
                height: chartType === 'progress' ? 'auto' : '300px',
                maxHeight: '400px',
                position: 'relative',
                width: '100%'
            }}>
                {renderChart()}
            </div>

            {/* Stats Summary */}
            <div style={{
                marginTop: '15px',
                padding: '10px',
                background: 'rgba(15, 23, 42, 0.4)',
                borderRadius: '6px',
                display: 'flex',
                justifyContent: 'space-around',
                fontSize: '0.9rem'
            }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ color: '#4ade80', fontWeight: 'bold', fontSize: '1.2rem' }}>
                        {present.length}
                    </div>
                    <div style={{ color: '#94a3b8' }}>Skills You Have</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ color: '#f87171', fontWeight: 'bold', fontSize: '1.2rem' }}>
                        {missing.length}
                    </div>
                    <div style={{ color: '#94a3b8' }}>Skills Missing</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ color: 'var(--primary-color)', fontWeight: 'bold', fontSize: '1.2rem' }}>
                        {((present.length / (present.length + missing.length)) * 100).toFixed(0)}%
                    </div>
                    <div style={{ color: '#94a3b8' }}>Match Rate</div>
                </div>
            </div>
        </div>
    );
};

export default SkillGapChart;

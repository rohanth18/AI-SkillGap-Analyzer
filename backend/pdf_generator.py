"""
Professional PDF Report Generator
Creates beautiful, comprehensive PDF reports for skill gap analysis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from datetime import datetime
import os

def create_header_style():
    """Create custom header styles"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='HighlightBox',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1e293b'),
        backColor=colors.HexColor('#e0e7ff'),
        borderPadding=10,
        borderWidth=1,
        borderColor=colors.HexColor('#6366f1'),
        spaceAfter=12
    ))
    
    return styles

def create_skill_gap_chart(matched_count, missing_count):
    """Create a bar chart for skill gap visualization"""
    drawing = Drawing(400, 200)
    
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 125
    chart.width = 300
    chart.data = [[matched_count, missing_count]]
    chart.categoryAxis.categoryNames = ['Matched Skills', 'Missing Skills']
    
    chart.bars[0].fillColor = colors.HexColor('#4ade80')
    chart.bars[1].fillColor = colors.HexColor('#f87171')
    
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = max(matched_count + missing_count, 10)
    chart.valueAxis.valueStep = 5
    
    drawing.add(chart)
    return drawing

def create_confidence_pie_chart(confidence_score):
    """Create a pie chart for confidence score"""
    drawing = Drawing(300, 200)
    
    pie = Pie()
    pie.x = 75
    pie.y = 50
    pie.width = 150
    pie.height = 150
    
    pie.data = [confidence_score, 100 - confidence_score]
    pie.labels = [f'{confidence_score}%', '']
    pie.slices[0].fillColor = colors.HexColor('#4ade80')
    pie.slices[1].fillColor = colors.HexColor('#e2e8f0')
    
    drawing.add(pie)
    return drawing

def generate_pdf_report(analysis_data, user_name, output_path):
    """
    Generate comprehensive PDF report
    
    Args:
        analysis_data: dict with all analysis information
        user_name: str
        output_path: str (path to save PDF)
    
    Returns:
        str: path to generated PDF
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    story = []
    styles = create_header_style()
    
    # ===== COVER PAGE =====
    story.append(Spacer(1, 2*inch))
    
    # Title
    title = Paragraph("Skill Gap Analysis Report", styles['CustomTitle'])
    story.append(title)
    story.append(Spacer(1, 0.3*inch))
    
    # User info
    user_info = Paragraph(f"<b>Candidate:</b> {user_name}", styles['Normal'])
    story.append(user_info)
    story.append(Spacer(1, 0.1*inch))
    
    job_role = Paragraph(f"<b>Target Role:</b> {analysis_data.get('job_role', 'N/A')}", styles['Normal'])
    story.append(job_role)
    story.append(Spacer(1, 0.1*inch))
    
    date_generated = Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal'])
    story.append(date_generated)
    story.append(Spacer(1, 0.5*inch))
    
    # Confidence Score Highlight
    confidence = analysis_data.get('confidence_score', 0)
    score_color = '#4ade80' if confidence >= 70 else '#facc15' if confidence >= 50 else '#f87171'
    
    score_text = f"""
    <para align=center>
        <font size=48 color='{score_color}'><b>{confidence}%</b></font><br/>
        <font size=14>Overall Confidence Score</font>
    </para>
    """
    story.append(Paragraph(score_text, styles['Normal']))
    
    story.append(PageBreak())
    
    # ===== EXECUTIVE SUMMARY =====
    story.append(Paragraph("Executive Summary", styles['CustomHeading']))
    story.append(Spacer(1, 0.2*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Confidence Score', f"{confidence}%"],
        ['Skills Matched', str(len(analysis_data.get('matched_skills', [])))],
        ['Skills Missing', str(len(analysis_data.get('missing_skills', [])))],
        ['Resume Quality', f"{analysis_data.get('resume_quality_score', 0)}%"],
        ['Red Flags', str(len(analysis_data.get('red_flags', [])))]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # ===== SKILL GAP VISUALIZATION =====
    story.append(Paragraph("Skill Gap Analysis", styles['CustomHeading']))
    story.append(Spacer(1, 0.2*inch))
    
    matched_count = len(analysis_data.get('matched_skills', []))
    missing_count = len(analysis_data.get('missing_skills', []))
    
    chart = create_skill_gap_chart(matched_count, missing_count)
    story.append(chart)
    story.append(Spacer(1, 0.3*inch))
    
    # ===== MATCHED SKILLS =====
    if analysis_data.get('matched_skills'):
        story.append(Paragraph("✓ Matched Skills", styles['CustomSubHeading']))
        
        matched_skills = analysis_data['matched_skills']
        if isinstance(matched_skills, list):
            skills_text = ", ".join(matched_skills[:20])  # Limit to 20
        else:
            skills_text = ", ".join(list(matched_skills.keys())[:20])
        
        story.append(Paragraph(skills_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # ===== MISSING SKILLS =====
    if analysis_data.get('missing_skills'):
        story.append(Paragraph("✗ Missing Skills", styles['CustomSubHeading']))
        
        missing_skills = analysis_data['missing_skills']
        skills_text = ", ".join(missing_skills[:20])
        
        story.append(Paragraph(skills_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # ===== RESUME QUALITY ANALYSIS =====
    story.append(Paragraph("Resume Quality Analysis", styles['CustomHeading']))
    story.append(Spacer(1, 0.2*inch))
    
    quality_score = analysis_data.get('resume_quality_score', 0)
    quality_breakdown = analysis_data.get('quality_breakdown', {})
    
    quality_text = f"<b>Overall Quality Score: {quality_score}%</b>"
    story.append(Paragraph(quality_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    if quality_breakdown:
        quality_data = [['Component', 'Score']]
        for key, value in quality_breakdown.items():
            quality_data.append([key.replace('_', ' ').title(), f"{value}"])
        
        quality_table = Table(quality_data, colWidths=[3*inch, 2*inch])
        quality_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
        ]))
        
        story.append(quality_table)
        story.append(Spacer(1, 0.3*inch))
    
    # ===== RED FLAGS =====
    red_flags = analysis_data.get('red_flags', [])
    if red_flags:
        story.append(Paragraph("⚠ Red Flags Detected", styles['CustomSubHeading']))
        story.append(Spacer(1, 0.1*inch))
        
        for flag in red_flags[:10]:  # Limit to 10
            severity = flag.get('severity', 'low').upper()
            description = flag.get('description', '')
            
            flag_text = f"<b>[{severity}]</b> {description}"
            story.append(Paragraph(flag_text, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # ===== RECOMMENDED ROLES =====
    if analysis_data.get('recommended_roles'):
        story.append(Paragraph("Recommended Job Roles", styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        for i, role in enumerate(analysis_data['recommended_roles'][:3], 1):
            role_name = role.get('role', 'Unknown')
            role_score = role.get('confidence', 0)
            
            role_text = f"<b>{i}. {role_name}</b> - {role_score}% match"
            story.append(Paragraph(role_text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
    
    # ===== LEARNING ROADMAP =====
    if analysis_data.get('roadmap'):
        story.append(Paragraph("Personalized Learning Roadmap", styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        roadmap = analysis_data['roadmap']
        total_weeks = roadmap.get('total_weeks', 0)
        
        roadmap_intro = f"<b>Duration:</b> {total_weeks} weeks"
        story.append(Paragraph(roadmap_intro, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        for week in roadmap.get('roadmap', [])[:8]:  # First 8 weeks
            week_num = week.get('week', 0)
            title = week.get('title', '')
            skill = week.get('skill', '')
            
            week_text = f"<b>Week {week_num}:</b> {title} ({skill})"
            story.append(Paragraph(week_text, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        story.append(Spacer(1, 0.3*inch))
    
    # ===== RECOMMENDED COURSES =====
    if analysis_data.get('youtube_recommendations'):
        story.append(Paragraph("Recommended Learning Resources", styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        for rec in analysis_data['youtube_recommendations'][:5]:
            skill = rec.get('skill', '')
            link = rec.get('link', '')
            
            rec_text = f"• <b>{skill}</b>: {link}"
            story.append(Paragraph(rec_text, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        story.append(Spacer(1, 0.3*inch))
    
    # ===== FOOTER =====
    story.append(Spacer(1, 1*inch))
    footer_text = """
    <para align=center>
        <font size=10 color='#64748b'>
            Generated by SkillGap AI - Your Career Development Partner<br/>
            © 2025 SkillGap AI. All rights reserved.
        </font>
    </para>
    """
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    return output_path

if __name__ == "__main__":
    # Test PDF generation
    test_data = {
        'job_role': 'Full Stack Developer',
        'confidence_score': 75.5,
        'matched_skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL'],
        'missing_skills': ['Docker', 'Kubernetes', 'AWS', 'TypeScript'],
        'resume_quality_score': 82.3,
        'quality_breakdown': {
            'action_verbs': 85,
            'readability': 78,
            'technical_coverage': 80,
            'achievements_score': 90
        },
        'red_flags': [
            {'severity': 'medium', 'description': 'No certifications mentioned'},
            {'severity': 'low', 'description': 'Resume could be more concise'}
        ],
        'recommended_roles': [
            {'role': 'Full Stack Developer', 'confidence': 85},
            {'role': 'Frontend Developer', 'confidence': 78},
            {'role': 'Backend Developer', 'confidence': 72}
        ],
        'roadmap': {
            'total_weeks': 12,
            'roadmap': [
                {'week': 1, 'title': 'Docker Fundamentals', 'skill': 'Docker'},
                {'week': 2, 'title': 'Container Orchestration', 'skill': 'Kubernetes'}
            ]
        },
        'youtube_recommendations': [
            {'skill': 'Docker', 'link': 'https://youtube.com/watch?v=example1'},
            {'skill': 'Kubernetes', 'link': 'https://youtube.com/watch?v=example2'}
        ]
    }
    
    print("Generating test PDF report...")
    output = "test_report.pdf"
    generate_pdf_report(test_data, "John Doe", output)
    print(f"PDF generated: {output}")

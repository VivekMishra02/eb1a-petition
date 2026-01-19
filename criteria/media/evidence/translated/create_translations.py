#!/usr/bin/env python3
"""
Generate USCIS-compliant certified translation PDFs
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

def create_dainik_bhaskar_pdf():
    """Create PDF for Dainik Bhaskar translation"""
    filename = "/Users/vivekmishra/Downloads/eb1_template/criteria/media/evidence/translated/Dainik_Bhaskar_Certified_Translation.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor='black',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Title
    Story.append(Paragraph("CERTIFIED TRANSLATION", title_style))
    Story.append(Spacer(1, 0.2*inch))
    
    # Document info
    Story.append(Paragraph("ENGLISH TRANSLATION OF HINDI NEWSPAPER ARTICLE", heading_style))
    Story.append(Spacer(1, 0.1*inch))
    
    Story.append(Paragraph("<b>Source:</b> Dainik Bhaskar (Business Plus Section)", body_style))
    Story.append(Paragraph("<b>Original Language:</b> Hindi", body_style))
    Story.append(Paragraph("<b>Date of Publication:</b> December 14, 2024", body_style))
    Story.append(Paragraph("<b>Article Title:</b> \"Lecture Held for Computer Science Students\"", body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Translation header
    Story.append(Paragraph("TRANSLATED TEXT", heading_style))
    Story.append(Spacer(1, 0.1*inch))
    
    # Article content
    Story.append(Paragraph("<b>Business Plus</b>", body_style))
    Story.append(Paragraph("<b>Lecture Held for Computer Science Students</b>", body_style))
    Story.append(Spacer(1, 0.1*inch))
    
    content = """<b>JAIPUR</b> | A lecture was organized under the 'Bridging Industry and Academia' Hybrid Lecture Series for Computer Science students on behalf of the Innovation Council of Anand International College of Engineering. Vivek Mishra, Associate Software Engineer, JPMorgan Chase &amp; Co., Wilmington, US, as the keynote speaker in the session 'Career Advice and Future Technologies for Computer Science Aspirants' shared valuable information related to Computer Science among the students and instilled in them a deep understanding of Computer Science shaping the area and discussed future technologies. On this occasion, College Vice Chairperson Monika Mittal Agrawal, Principal Prof. (Dr.) Vijay Kumar Sharma, Vice Principal Prof. (Dr.) Praveen Agrawal were present."""
    
    Story.append(Paragraph(content, body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Certification
    Story.append(Paragraph("TRANSLATOR'S CERTIFICATION STATEMENT", heading_style))
    Story.append(Spacer(1, 0.1*inch))
    
    cert_text = """I, Subhash K Chand, certify that I am competent and fluent in both the Hindi and English languages and possess the necessary qualifications to translate documents from Hindi to English. I further certify that the above English translation is a complete, accurate, and faithful translation of the original Hindi newspaper article published in Dainik Bhaskar (Business Plus Section) on December 14, 2024."""
    
    Story.append(Paragraph(cert_text, body_style))
    Story.append(Spacer(1, 0.1*inch))
    
    cert_text2 = """I have personally reviewed both the original Hindi article and this English translation to ensure accuracy and completeness. I have the ability to read, write, and comprehend both Hindi and English languages at a professional level."""
    
    Story.append(Paragraph(cert_text2, body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Signature block
    Story.append(Paragraph("Signature: _______________________________", body_style))
    Story.append(Spacer(1, 0.1*inch))
    Story.append(Paragraph("<b>Name:</b> Subhash K Chand", body_style))
    Story.append(Paragraph("<b>Professional Title:</b> Translator (Hindi-English)", body_style))
    Story.append(Paragraph("<b>Contact Information:</b> [To be completed]", body_style))
    Story.append(Paragraph("<b>Date of Certification:</b> January 19, 2026", body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Footer note
    footer = """This certification is provided in accordance with U.S. Citizenship and Immigration Services (USCIS) requirements for certified translations of foreign language documents. The translator affirms competence in both source and target languages and attests to the accuracy and completeness of this translation."""
    Story.append(Paragraph(footer, body_style))
    
    doc.build(Story)
    print(f"Created: {filename}")

def create_patrika_pdf():
    """Create PDF for Patrika translation"""
    filename = "/Users/vivekmishra/Downloads/eb1_template/criteria/media/evidence/translated/Patrika_Certified_Translation.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor='black',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Title
    Story.append(Paragraph("CERTIFIED TRANSLATION", title_style))
    Story.append(Spacer(1, 0.2*inch))
    
    # Document info
    Story.append(Paragraph("ENGLISH TRANSLATION OF HINDI NEWSPAPER ARTICLE", heading_style))
    Story.append(Spacer(1, 0.1*inch))
    
    Story.append(Paragraph("<b>Source:</b> Patrika", body_style))
    Story.append(Paragraph("<b>Original Language:</b> Hindi", body_style))
    Story.append(Paragraph("<b>Date of Publication:</b> December 2024", body_style))
    Story.append(Paragraph("<b>Article Title:</b> \"Special Lecture on Career Opportunities in Computer Science at Anand International College\"", body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Translation header
    Story.append(Paragraph("TRANSLATED TEXT", heading_style))
    Story.append(Spacer(1, 0.1*inch))
    
    # Article content  
    Story.append(Paragraph("<b>Special Lecture on Career Opportunities in Computer Science at Anand International College</b>", body_style))
    Story.append(Spacer(1, 0.1*inch))
    
    content = """<b>JAIPUR @ PATRIKA PLUS:</b> Under the Innovation Council of Anand International College of Engineering, a special lecture was organized for Computer Science students on the topic of 'Bridging Industry and Academia' Hybrid Lecture Series. As the chief speaker, Vivek Mishra, an Associate Software Engineer from JPMorgan Chase &amp; Co., a US-based company, shared extensive information with students about future-oriented techniques and the significance of Computer Science. He discussed Computer Science significance and its various applications in detail. Students asked several valuable questions during the session. College Vice Chairperson Monika Mittal Agrawal, Principal Prof. (Dr.) Vijay Kumar Sharma, and Vice Principal Prof. (Dr.) Praveen Agrawal were present on this occasion."""
    
    Story.append(Paragraph(content, body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Certification
    Story.append(Paragraph("TRANSLATOR'S CERTIFICATION STATEMENT", heading_style))
    Story.append(Spacer(1, 0.1*inch))
    
    cert_text = """I, Subhash K Chand, certify that I am competent and fluent in both the Hindi and English languages and possess the necessary qualifications to translate documents from Hindi to English. I further certify that the above English translation is a complete, accurate, and faithful translation of the original Hindi newspaper article published in Patrika newspaper."""
    
    Story.append(Paragraph(cert_text, body_style))
    Story.append(Spacer(1, 0.1*inch))
    
    cert_text2 = """I have personally reviewed both the original Hindi article and this English translation to ensure accuracy and completeness. I have the ability to read, write, and comprehend both Hindi and English languages at a professional level."""
    
    Story.append(Paragraph(cert_text2, body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Signature block
    Story.append(Paragraph("Signature: _______________________________", body_style))
    Story.append(Spacer(1, 0.1*inch))
    Story.append(Paragraph("<b>Name:</b> Subhash K Chand", body_style))
    Story.append(Paragraph("<b>Professional Title:</b> Translator (Hindi-English)", body_style))
    Story.append(Paragraph("<b>Contact Information:</b> [To be completed]", body_style))
    Story.append(Paragraph("<b>Date of Certification:</b> January 19, 2026", body_style))
    Story.append(Spacer(1, 0.3*inch))
    
    # Footer note
    footer = """This certification is provided in accordance with U.S. Citizenship and Immigration Services (USCIS) requirements for certified translations of foreign language documents. The translator affirms competence in both source and target languages and attests to the accuracy and completeness of this translation."""
    Story.append(Paragraph(footer, body_style))
    
    doc.build(Story)
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_dainik_bhaskar_pdf()
    create_patrika_pdf()
    print("\\nBoth certified translation PDFs created successfully!")

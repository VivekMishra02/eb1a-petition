#!/usr/bin/env python3
"""
Detailed analysis to understand the actual structure of main.pdf
"""

import pypdf
import re

def detailed_analysis(pdf_path="main.pdf"):
    """
    Read through PDF to understand the actual structure
    """
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    print("DETAILED PDF STRUCTURE ANALYSIS")
    print("="*70)
    
    # Analyze first 100 pages to understand structure
    print("\n📄 First 100 pages content analysis:\n")
    
    for page_num in range(min(100, total_pages)):
        try:
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Look for key markers
            page_info = f"Page {page_num + 1:3d}: "
            
            # Check for section headings
            if 'Evidence of original' in text and 'contributions of major significance' in text:
                print(page_info + "★ CRITERION: Original Contributions")
            elif 'Evidence of authorship of scholarly articles' in text:
                print(page_info + "★ CRITERION: Scholarly Articles")
            elif 'Evidence of participation as a judge' in text:
                print(page_info + "★ CRITERION: Judging")
            elif 'Evidence of performance in a leading or critical role' in text:
                print(page_info + "★ CRITERION: Critical Role")
            elif 'Evidence of membership in associations' in text:
                print(page_info + "★ CRITERION: Membership")
            elif 'Evidence of published material about' in text:
                print(page_info + "★ CRITERION: Published Material")
            
            # Check for cover/summary sections
            elif 'I-140, Immigrant Petition' in text or 'Petition for Alien Worker' in text:
                print(page_info + "📄 Cover/Petition Document")
            elif 'Summary of' in text and 'Qualifications' in text:
                print(page_info + "📄 Summary Section")
            elif 'List of Exhibits' in text:
                print(page_info + "📋 LIST OF EXHIBITS")
            
            # Check for exhibit headers (in the comment sections)
            elif 'EXHIBITS FOR ORIGINAL' in text:
                print(page_info + "🔖 === ORIGINAL CONTRIBUTIONS EXHIBITS SECTION ===")
            elif 'EXHIBITS FOR JUDGING' in text:
                print(page_info + "🔖 === JUDGING EXHIBITS SECTION ===")
            elif 'EXHIBITS FOR SCHOLARLY' in text:
                print(page_info + "🔖 === SCHOLARLY ARTICLES EXHIBITS SECTION ===")
            elif 'EXHIBITS FOR CRITICAL' in text:
                print(page_info + "🔖 === CRITICAL ROLE EXHIBITS SECTION ===")
            elif 'EXHIBITS FOR MEMBERSHIP' in text:
                print(page_info + "🔖 === MEMBERSHIP EXHIBITS SECTION ===")
            elif 'EXHIBITS FOR PUBLISHED MATERIAL' in text or 'EXHIBITS FOR MEDIA' in text:
                print(page_info + "🔖 === PUBLISHED MATERIAL EXHIBITS SECTION ===")
            
            # Check for specific exhibits
            exhibit_match = re.search(r'Exhibit ((?:OR|JR|SR|CR|M|PM|LOR|RV)-[\w.]+)', text)
            if exhibit_match:
                exhibit_id = exhibit_match.group(1)
                # Get the title (usually after the exhibit ID)
                title_match = re.search(rf'Exhibit {re.escape(exhibit_id)}[:\s]+(.*?)(?:\n|$)', text)
                if title_match:
                    title = title_match.group(1).strip()[:60]
                    print(page_info + f"  📎 Exhibit {exhibit_id}: {title}")
                else:
                    print(page_info + f"  📎 Exhibit {exhibit_id}")
        
        except Exception as e:
            continue
    
    print("\n" + "="*70)

if __name__ == "__main__":
    detailed_analysis()

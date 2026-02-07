#!/usr/bin/env python3
"""
Analyze main.pdf to find exact exhibit locations by reading PDF text
"""

import pypdf
import re

def analyze_pdf_structure(pdf_path="main.pdf"):
    """
    Read through PDF and identify where each exhibit section starts
    """
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    print(f"Analyzing {pdf_path} ({total_pages} pages)...")
    print("="*70)
    
    # Track important markers
    markers = {
        'list_of_exhibits': None,
        'original_start': None,
        'judging_start': None,
        'scholarly_start': None,
        'critical_start': None,
        'membership_start': None,
        'media_start': None,
    }
    
    # Track all exhibits found
    exhibits_found = []
    
    print("\n🔍 Scanning for section markers and exhibits...\n")
    
    for page_num in range(total_pages):
        try:
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Look for key section markers
            if 'List of Exhibits' in text and markers['list_of_exhibits'] is None:
                markers['list_of_exhibits'] = page_num
                print(f"📋 Page {page_num + 1}: Found 'List of Exhibits'")
            
            # Look for exhibit section headers
            if re.search(r'EXHIBITS FOR ORIGINAL CONTRIBUTION', text, re.IGNORECASE):
                markers['original_start'] = page_num
                print(f"📌 Page {page_num + 1}: ORIGINAL CONTRIBUTIONS EXHIBITS START")
            
            if re.search(r'EXHIBITS FOR JUDGING', text, re.IGNORECASE):
                markers['judging_start'] = page_num
                print(f"📌 Page {page_num + 1}: JUDGING EXHIBITS START")
            
            if re.search(r'EXHIBITS FOR SCHOLARLY ARTICLES', text, re.IGNORECASE):
                markers['scholarly_start'] = page_num
                print(f"📌 Page {page_num + 1}: SCHOLARLY ARTICLES EXHIBITS START")
            
            if re.search(r'EXHIBITS FOR CRITICAL ROLE', text, re.IGNORECASE):
                markers['critical_start'] = page_num
                print(f"📌 Page {page_num + 1}: CRITICAL ROLE EXHIBITS START")
            
            if re.search(r'EXHIBITS FOR PUBLISHED MATERIAL', text, re.IGNORECASE):
                markers['media_start'] = page_num
                print(f"📌 Page {page_num + 1}: PUBLISHED MATERIAL EXHIBITS START")
            
            # Membership doesn't have a clear header, look for M-1 exhibit
            if re.search(r'Exhibit M-1', text) and markers['membership_start'] is None:
                markers['membership_start'] = page_num
                print(f"📌 Page {page_num + 1}: MEMBERSHIP EXHIBITS START (Exhibit M-1)")
            
            # Track individual exhibits
            exhibit_matches = re.findall(r'Exhibit ((?:OR|JR|SR|CR|M|PM|LOR|RV)-[\w.]+)', text)
            for exhibit in exhibit_matches:
                exhibits_found.append({
                    'id': exhibit,
                    'page': page_num + 1
                })
        
        except Exception as e:
            continue
    
    print("\n" + "="*70)
    print("📊 ANALYSIS RESULTS")
    print("="*70)
    
    print("\n🎯 Key Section Locations:")
    for key, page in markers.items():
        if page is not None:
            print(f"  {key:20s}: Page {page + 1}")
        else:
            print(f"  {key:20s}: NOT FOUND")
    
    print(f"\n📄 Total Exhibits Found: {len(exhibits_found)}")
    
    # Group exhibits by type
    exhibit_types = {}
    for ex in exhibits_found:
        ex_type = ex['id'].split('-')[0]
        if ex_type not in exhibit_types:
            exhibit_types[ex_type] = []
        exhibit_types[ex_type].append(ex)
    
    print("\n📋 Exhibits by Type:")
    for ex_type in sorted(exhibit_types.keys()):
        exs = exhibit_types[ex_type]
        first_page = min(ex['page'] for ex in exs)
        last_page = max(ex['page'] for ex in exs)
        print(f"  {ex_type:4s}: {len(exs):2d} exhibits (Pages {first_page}-{last_page})")
    
    return markers, exhibits_found

if __name__ == "__main__":
    markers, exhibits = analyze_pdf_structure()
    
    print("\n" + "="*70)
    print("✓ Analysis complete - use these page numbers for accurate splitting")
    print("="*70)

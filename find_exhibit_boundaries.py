#!/usr/bin/env python3
"""
Find exact boundaries of each exhibit section in main.pdf
"""

import pypdf
import re

def find_exhibit_boundaries(pdf_path="main.pdf"):
    """
    Scan PDF from page 60 onwards to find where each exhibit type starts/ends
    """
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    print("FINDING EXACT EXHIBIT BOUNDARIES")
    print("="*70)
    
    # Track first and last occurrence of each exhibit type
    exhibit_ranges = {}
    
    print("\n🔍 Scanning pages 60-557 for exhibits...\n")
    
    for page_num in range(59, total_pages):  # Start from page 60 (index 59)
        try:
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Find all exhibits on this page
            exhibits = re.findall(r'Exhibit ((?:OR|JR|SR|CR|M|PM|LOR|RV)-[\w.]+)', text)
            
            for exhibit in set(exhibits):  # unique exhibits on this page
                prefix = exhibit.split('-')[0]
                
                if prefix not in exhibit_ranges:
                    exhibit_ranges[prefix] = {'first': page_num + 1, 'last': page_num + 1, 'exhibits': []}
                else:
                    exhibit_ranges[prefix]['last'] = page_num + 1
                
                if exhibit not in exhibit_ranges[prefix]['exhibits']:
                    exhibit_ranges[prefix]['exhibits'].append(exhibit)
                    print(f"Page {page_num + 1:3d}: Found Exhibit {exhibit}")
        
        except Exception as e:
            continue
    
    print("\n" + "="*70)
    print("📊 EXHIBIT SECTION BOUNDARIES")
    print("="*70)
    
    # Sort by first page
    sorted_sections = sorted(exhibit_ranges.items(), key=lambda x: x[1]['first'])
    
    for prefix, info in sorted_sections:
        page_range = f"Pages {info['first']}-{info['last']}"
        num_pages = info['last'] - info['first'] + 1
        num_exhibits = len(info['exhibits'])
        
        criterion_name = {
            'OR': 'Original Contributions',
            'JR': 'Judging',
            'SR': 'Scholarly Articles',
            'CR': 'Critical Role',
            'M': 'Membership',
            'PM': 'Published Material',
            'LOR': 'Letters of Recommendation',
            'RV': 'Reference/LOR'
        }.get(prefix, prefix)
        
        print(f"\n{prefix:4s} - {criterion_name}")
        print(f"       {page_range} ({num_pages} pages, {num_exhibits} exhibits)")
        print(f"       Exhibits: {', '.join(sorted(info['exhibits']))}")
    
    return exhibit_ranges

if __name__ == "__main__":
    boundaries = find_exhibit_boundaries()
    
    print("\n" + "="*70)
    print("RECOMMENDED SPLIT POINTS:")
    print("="*70)
    
    # Determine logical split points
    print("\n1. Cover + All Narratives: Pages 1-59")
    print("   (Includes cover, summary, all 6 criteria narratives, list of exhibits)")
    
    if 'OR' in boundaries:
        print(f"\n2. Original Contributions Evidence: Pages {boundaries['OR']['first']}-{boundaries['OR']['last']}")
    
    if 'JR' in boundaries:
        print(f"\n3. Judging Evidence: Pages {boundaries['JR']['first']}-{boundaries['JR']['last']}")
    
    if 'SR' in boundaries:
        print(f"\n4. Scholarly Articles Evidence: Pages {boundaries['SR']['first']}-{boundaries['SR']['last']}")
    
    if 'CR' in boundaries:
        print(f"\n5. Critical Role Evidence: Pages {boundaries['CR']['first']}-{boundaries['CR']['last']}")
    
    if 'M' in boundaries:
        print(f"\n6. Membership Evidence: Pages {boundaries['M']['first']}-{boundaries['M']['last']}")
    
    if 'PM' in boundaries:
        print(f"\n7. Published Material Evidence: Pages {boundaries['PM']['first']}-557")
    
    print("\n" + "="*70)

#!/usr/bin/env python3
"""
Verify that each split file contains the correct exhibits
"""

import pypdf
import re
import os

def verify_split_files():
    """
    Check each split file to verify it contains the correct exhibits
    """
    
    output_dir = "online/I140"
    
    files_to_check = {
        "01_Cover_and_Narratives.pdf": {
            "expected_content": ["List of Exhibits", "Original Contributions", "Scholarly Articles"],
            "expected_exhibits": []
        },
        "02_Original_Contributions.pdf": {
            "expected_content": ["Exhibit OR-"],
            "expected_exhibits": ["OR-1", "OR-2", "OR-3", "OR-4", "OR-5", "OR-6", "OR-7", "OR-8", "OR-9"]
        },
        "03_Judging.pdf": {
            "expected_content": ["Exhibit JR-"],
            "expected_exhibits": ["JR-1", "JR-2", "JR-10", "JR-20", "JR-29"]
        },
        "04_Scholarly_Articles_Part1.pdf": {
            "expected_content": ["Exhibit SR-"],
            "expected_exhibits": ["SR-1", "SR-2", "SR-3", "SR-4"]
        },
        "04_Scholarly_Articles_Part2.pdf": {
            "expected_content": ["Exhibit SR-"],
            "expected_exhibits": ["SR-5", "SR-6", "SR-7", "SR-8", "SR-9"]
        },
        "05_Critical_Role.pdf": {
            "expected_content": ["Exhibit CR-"],
            "expected_exhibits": ["CR-1", "CR-2", "CR-10", "CR-13"]
        },
        "06_Published_Material.pdf": {
            "expected_content": ["Exhibit PM-"],
            "expected_exhibits": ["PM-1", "PM-2", "PM-10", "PM-12"]
        },
    }
    
    print("="*70)
    print("VERIFICATION: Checking split file contents")
    print("="*70)
    
    all_good = True
    
    for filename, checks in files_to_check.items():
        filepath = os.path.join(output_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"\n❌ {filename}: FILE NOT FOUND")
            all_good = False
            continue
        
        reader = pypdf.PdfReader(filepath)
        num_pages = len(reader.pages)
        
        print(f"\n✓ {filename} ({num_pages} pages)")
        
        # Scan all pages
        all_text = ""
        exhibits_found = []
        
        for page_num in range(num_pages):
            try:
                text = reader.pages[page_num].extract_text()
                all_text += text
                
                # Find exhibits
                found = re.findall(r'Exhibit ((?:OR|JR|SR|CR|M|PM)-[\w.]+)', text)
                exhibits_found.extend(found)
            except:
                continue
        
        exhibits_found = list(set(exhibits_found))
        
        # Check expected content
        content_ok = True
        for expected in checks["expected_content"]:
            if expected not in all_text:
                print(f"  ❌ Missing expected content: '{expected}'")
                content_ok = False
                all_good = False
        
        # Check expected exhibits
        if checks["expected_exhibits"]:
            missing = []
            for exhibit in checks["expected_exhibits"]:
                if not any(exhibit in ex for ex in exhibits_found):
                    missing.append(exhibit)
            
            if missing:
                print(f"  ❌ Missing exhibits: {', '.join(missing)}")
                all_good = False
                content_ok = False
            else:
                print(f"  ✓ Contains expected exhibits: {', '.join(sorted(exhibits_found))}")
        
        if content_ok and checks["expected_content"]:
            print(f"  ✓ Content verification passed")
    
    print("\n" + "="*70)
    if all_good:
        print("✓ ALL FILES VERIFIED SUCCESSFULLY")
    else:
        print("❌ SOME FILES HAVE ISSUES - SEE ABOVE")
    print("="*70)
    
    return all_good

if __name__ == "__main__":
    verify_split_files()

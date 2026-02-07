#!/usr/bin/env python3
"""
Split Media Coverage PDF into smaller parts for USCIS upload
"""

import pypdf
import os

def split_media_pdf():
    """Split the media coverage PDF into parts under 12MB"""
    
    input_pdf = "online/07_Media_Coverage_Evidence.pdf"
    
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found")
        return
    
    reader = pypdf.PdfReader(input_pdf)
    total_pages = len(reader.pages)
    
    print(f"Total pages in media coverage: {total_pages}")
    
    # Create Part 1 with updated translations
    part1_pages = []
    # TechBullion: pages 0-3 (4 pages)
    # IEEE Transmitter: pages 4-8 (5 pages)
    # IEEE TV: pages 9-11 (3 pages)
    # DainikBhaskar Translation: page 12 (1 page) - UPDATED
    # RajasthanPatrika Translation: page 13 (1 page) - UPDATED
    # FirstIndia: pages 14-27 (14 pages)
    # Total: 28 pages
    
    writer1 = pypdf.PdfWriter()
    for i in range(0, 28):
        if i < total_pages:
            writer1.add_page(reader.pages[i])
    
    output1 = "online/07_Media_Coverage_Part1.pdf"
    with open(output1, 'wb') as f:
        writer1.write(f)
    
    size1_mb = os.path.getsize(output1) / 1024 / 1024
    print(f"Created Part 1: 28 pages, {size1_mb:.2f}MB")
    print(f"  - Includes UPDATED translations for Dainik Bhaskar and Rajasthan Patrika")
    
    # Create Part 2 with remaining articles
    if total_pages > 28:
        writer2 = pypdf.PdfWriter()
        for i in range(28, total_pages):
            writer2.add_page(reader.pages[i])
        
        output2 = "online/07_Media_Coverage_Part2.pdf"
        with open(output2, 'wb') as f:
            writer2.write(f)
        
        size2_mb = os.path.getsize(output2) / 1024 / 1024
        pages2 = total_pages - 28
        print(f"Created Part 2: {pages2} pages, {size2_mb:.2f}MB")
    
    print(f"\n✓ Media coverage successfully split into manageable parts")

if __name__ == "__main__":
    split_media_pdf()

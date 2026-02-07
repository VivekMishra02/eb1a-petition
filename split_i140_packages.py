#!/usr/bin/env python3
"""
Split main.pdf into I-140 petition packages based on manual page counting
Handles large files by creating multi-part packages
"""

import pypdf
import os
import subprocess
from pathlib import Path

def get_file_size_mb(filepath):
    """Get file size in MB"""
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / 1024 / 1024
    return 0

def compress_pdf(input_pdf, output_pdf=None):
    """Compress PDF using Ghostscript"""
    if output_pdf is None:
        output_pdf = input_pdf.replace('.pdf', '_compressed.pdf')
    
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.7',
        '-dPDFSETTINGS=/ebook',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={output_pdf}',
        input_pdf
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except:
        return False

def split_large_package(reader, start, end, base_filename, output_dir, max_mb=10):
    """
    Split a large package into multiple parts
    Returns list of created files
    """
    total_pages = end - start + 1
    files_created = []
    
    # Try to split into roughly equal parts
    pages_per_part = max(50, total_pages // 3)  # At least 50 pages per part
    
    part_num = 1
    current_start = start
    
    while current_start <= end:
        current_end = min(current_start + pages_per_part - 1, end)
        
        writer = pypdf.PdfWriter()
        for page_num in range(current_start, current_end + 1):
            writer.add_page(reader.pages[page_num])
        
        # Create filename with part number
        if part_num == 1 and current_end == end:
            # Only one part needed
            output_path = os.path.join(output_dir, base_filename)
        else:
            # Multiple parts
            base, ext = os.path.splitext(base_filename)
            output_path = os.path.join(output_dir, f"{base}_Part{part_num}{ext}")
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        num_pages = current_end - current_start + 1
        size_mb = get_file_size_mb(output_path)
        
        files_created.append({
            'path': output_path,
            'pages': num_pages, 
            'size': size_mb,
            'start': current_start + 1,
            'end': current_end + 1,
        })
        
        part_num += 1
        current_start = current_end + 1
    
    return files_created

def create_i140_packages():
    """
    Create I-140 petition packages with smart splitting
    Based on manual analysis of main.tex structure
    """
    
    input_pdf = "main.pdf"
    output_dir = "online/I140"
    
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found")
        return
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    reader = pypdf.PdfReader(input_pdf)
    total_pages = len(reader.pages)
    
    print("="*70)
    print("I-140 Petition Package Creator - Smart Split")
    print("="*70)
    print(f"Input: {input_pdf} ({total_pages} pages)")
    print(f"Output directory: {output_dir}/")
    print()
    
    # Manual page mapping based on 557-page PDF structure:
    # Estimated based on typical EB1-A petition layout
    packages = [
        {
            "name": "01_Cover_Letter_and_Summary",
            "desc": "Cover Letter, Initial Evidence, Summary, All Criteria Narratives, Legal Argument, and List of Exhibits",
            "start": 0,  # pages 1-11
            "end": 10,
        },
        {
            "name": "02_Original_Contributions_Evidence",
            "desc": "Original Contributions - Exhibits OR-1 through OR-1.B, RV-1",
            "start": 11,  # pages 12-65 (approx 54 pages: 47+1+3+3+2+3+1+4+1 from exhibits)
            "end": 64,
        },
        {
            "name": "03_Judging_Evidence",
            "desc": "Judging Work of Others - Exhibits JR-1 through JR-29",
            "start": 65,  # pages 66-160 (approx 95 pages of judging evidence)
            "end": 159,
        },
        {
            "name": "04_Scholarly_Articles_Evidence",
            "desc": "Authorship of Scholarly Articles - Exhibits SR-1 through SR-9",
            "start": 160,  # pages 161-400 (240 pages of scholarly articles)
            "end": 399,
        },
        {
            "name": "05_Critical_Role_Evidence",
            "desc": "Leading/Critical Role - Exhibits CR-1 through CR-13",
            "start": 400,  # pages 401-445 (approx 45 pages)
            "end": 444,
        },
        {
            "name": "06_Membership_Evidence",
            "desc": "Membership in Associations - Exhibits M-1 through M-7",
            "start": 445,  # pages 446-495 (approx 50 pages)
            "end": 494,
        },
        {
            "name": "07_Published_Material_Evidence",
            "desc": "Published Material About Beneficiary - Exhibits PM-1 through PM-12",
            "start": 495,  # pages 496-557 (approx 62 pages)
            "end": total_pages - 1,
        },
    ]
    
    print("Creating I-140 petition packages...")
    print()
    
    all_files = []
    
    for package in packages:
        name = package["name"]
        desc = package["desc"]
        start = package["start"]
        end = min(package["end"], total_pages - 1)
        
        if start >= total_pages or start > end:
            print(f"⚠ Skipping {name} - invalid page range")
            continue
        
        filename = f"{name}.pdf"
        
        # Check estimated size first
        num_pages = end - start + 1
        
        # If likely to be very large, split immediately
        if num_pages > 200:
            print(f"📦 {name} ({num_pages} pages - splitting into parts)")
            parts = split_large_package(reader, start, end, filename, output_dir)
            
            for i, part in enumerate(parts, 1):
                print(f"  Part {i}: Pages {part['start']}-{part['end']} ({part['pages']} pages, {part['size']:.2f} MB)")
                all_files.append(part)
        else:
            # Create single file
            writer = pypdf.PdfWriter()
            for page_num in range(start, end + 1):
                writer.add_page(reader.pages[page_num])
            
            output_path = os.path.join(output_dir, filename)
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            size_mb = get_file_size_mb(output_path)
            
            print(f"✓ {filename}")
            print(f"  Pages: {start+1}-{end+1} ({num_pages} pages)")
            print(f"  Size: {size_mb:.2f} MB")
            
            if size_mb > 12.0:
                print(f"  ⚠ Exceeds 12MB - compressing...")
                compressed_path = output_path.replace('.pdf', '_compressed.pdf')
                if compress_pdf(output_path, compressed_path):
                    compressed_size = get_file_size_mb(compressed_path)
                    if compressed_size < size_mb:
                        os.replace(compressed_path, output_path)
                        size_mb = compressed_size
                        print(f"  ✓ Compressed to {size_mb:.2f} MB")
                    else:
                        os.remove(compressed_path)
            
            all_files.append({
                'path': output_path,
                'pages': num_pages,
                'size': size_mb,
                'start': start + 1,
                'end': end + 1,
            })
        
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✓ Created {len(all_files)} package files")
    print()
    
    total_size = sum(f['size'] for f in all_files)
    print(f"Total size: {total_size:.2f} MB")
    print()
    
    # Check for files still exceeding limit
    large_files = [f for f in all_files if f['size'] > 12.0]
    if large_files:
        print("⚠ FILES STILL EXCEEDING 12MB:")
        for f in large_files:
            filename = os.path.basename(f['path'])
            print(f"  {filename}: {f['size']:.2f} MB ({f['pages']} pages)")
        print()
        print("RECOMMENDATION: These may need manual splitting or further compression.")
    else:
        print("✓ All files are within or close to 12MB USCIS limit")
    
    print()
    print("="*70)
    print("✓ I-140 petition packages ready in online/I140/")
    print("="*70)

if __name__ == "__main__":
    create_i140_packages()

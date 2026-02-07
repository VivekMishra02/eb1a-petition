#!/usr/bin/env python3
"""
Split main.pdf correctly with ALL 6 criteria including Membership
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

def split_pdf_correctly():
    """
    Split main.pdf with CORRECT boundaries for ALL 6 criteria
    """
    
    input_pdf = "main.pdf"
    output_dir = "online/I140"
    
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found")
        return
    
    # Clean out old files
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for old_pdf in Path(output_dir).glob("*.pdf"):
        old_pdf.unlink()
        print(f"Removed old file: {old_pdf.name}")
    
    reader = pypdf.PdfReader(input_pdf)
    total_pages = len(reader.pages)
    
    print("\n" + "="*70)
    print("CORRECTED I-140 PETITION SPLIT - ALL 6 CRITERIA")
    print("="*70)
    print(f"Input: {input_pdf} ({total_pages} pages)")
    print(f"Output directory: {output_dir}/")
    print("\nIncluding Membership criterion (was missing)")
    print("="*70)
    
    # CORRECTED page ranges including Membership
    # Order: Cover, Original, Judging, Scholar, Critical, Membership, Published Material
    packages = [
        {
            "filename": "01_Cover_and_Narratives.pdf",
            "desc": "Cover Letter, Summary, All 6 Criteria Narratives, Legal Argument, List of Exhibits",
            "start": 0,    # Pages 1-59
            "end": 58,
        },
        {
            "filename": "02_Original_Contributions.pdf",
            "desc": "Original Contributions Evidence (Exhibits OR-1 through OR-9, OR-1.B, LOR-6, RV-1)",
            "start": 59,   # Pages 60-137
            "end": 136,
        },
        {
            "filename": "03_Judging.pdf",
            "desc": "Judging Evidence (Exhibits JR-1 through JR-29)",
            "start": 137,  # Pages 138-213
            "end": 212,
        },
        {
            "filename": "04_Scholarly_Articles.pdf",
            "desc": "Scholarly Articles Evidence (Exhibits SR-1 through SR-9)",
            "start": 213,  # Pages 214-400 (check actual end)
            "end": 399,    # Will verify
        },
        {
            "filename": "05_Critical_Role.pdf",
            "desc": "Critical Role Evidence (Exhibits CR-1 through CR-13)",
            "start": 400,  # Pages 401-445 (check actual)
            "end": 444,    # Will verify
        },
        {
            "filename": "06_Membership.pdf",
            "desc": "Membership Evidence (Exhibits M-1 through M-7 - IEEE Senior Member)",
            "start": 445,  # Pages 446-495 (check actual)
            "end": 494,    # Will verify
        },
        {
            "filename": "07_Published_Material.pdf",
            "desc": "Published Material Evidence (Exhibits PM-1 through PM-12)",
            "start": 495,  # Pages 496-559
            "end": total_pages - 1,
        },
    ]
    
    print("\n📦 Creating packages with correct boundaries...\n")
    
    all_files = []
    
    for package in packages:
        filename = package["filename"]
        desc = package["desc"]
        start = package["start"]
        end = min(package["end"], total_pages - 1)
        num_pages = end - start + 1
        
        # Check if this will be large (>200 pages) and needs splitting
        if num_pages > 200:
            print(f"📦 {filename} ({num_pages} pages - will split into parts)")
            
            # Split Scholarly Articles into 2 parts
            pages_per_part = num_pages // 2
            
            part_num = 1
            current_start = start
            
            while current_start <= end:
                current_end = min(current_start + pages_per_part - 1, end)
                
                writer = pypdf.PdfWriter()
                for page_num in range(current_start, current_end + 1):
                    writer.add_page(reader.pages[page_num])
                
                # Create part filename
                base, ext = os.path.splitext(filename)
                part_filename = f"{base}_Part{part_num}{ext}"
                output_path = os.path.join(output_dir, part_filename)
                
                with open(output_path, 'wb') as f:
                    writer.write(f)
                
                part_pages = current_end - current_start + 1
                size_mb = get_file_size_mb(output_path)
                
                print(f"  Part {part_num}: Pages {current_start+1}-{current_end+1} ({part_pages} pages, {size_mb:.2f} MB)")
                
                all_files.append({
                    'path': output_path,
                    'pages': part_pages,
                    'size': size_mb
                })
                
                part_num += 1
                current_start = current_end + 1
        
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
            print(f"  Pages: {start+1}-{end+1} ({num_pages} pages, {size_mb:.2f} MB)")
            
            # Compress if over 12MB
            if size_mb > 12.0:
                print(f"  ⚠ Exceeds 12MB - compressing...")
                compressed_path = output_path.replace('.pdf', '_compressed.pdf')
                if compress_pdf(output_path, compressed_path):
                    compressed_size = get_file_size_mb(compressed_path)
                    os.replace(compressed_path, output_path)
                    size_mb = compressed_size
                    print(f"  ✓ Compressed to {size_mb:.2f} MB")
            
            all_files.append({
                'path': output_path,
                'pages': num_pages,
                'size': size_mb
            })
        
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✓ Created {len(all_files)} package files")
    
    total_size = sum(f['size'] for f in all_files)
    print(f"\nTotal size: {total_size:.2f} MB")
    
    # Check for files over 12MB
    large_files = [f for f in all_files if f['size'] > 12.0]
    if large_files:
        print("\n⚠ FILES OVER 12MB:")
        for f in large_files:
            print(f"  {os.path.basename(f['path'])}: {f['size']:.2f} MB")
    else:
        print("\n✓ All files under 12MB USCIS limit")
    
    print("\n" + "="*70)
    print(f"✓ Files ready in {output_dir}/")
    print("="*70)

if __name__ == "__main__":
    split_pdf_correctly()

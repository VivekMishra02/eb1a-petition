#!/usr/bin/env python3
"""
Create IEEE Membership Evidence Package and Split Large Files
"""

import pypdf
import os
import subprocess

def merge_pdfs(pdf_files, output_path, description):
    """Merge multiple PDF files into one"""
    print(f"Creating: {os.path.basename(output_path)}")
    print(f"Description: {description}")
    
    writer = pypdf.PdfWriter()
    total_pages = 0
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            try:
                reader = pypdf.PdfReader(pdf_file)
                pages = len(reader.pages)
                for page in reader.pages:
                    writer.add_page(page)
                total_pages += pages
                print(f"  + {os.path.basename(pdf_file)} ({pages} pages)")
            except Exception as e:
                print(f"  ✗ Error adding {pdf_file}: {e}")
        else:
            print(f"  ⚠ File not found: {pdf_file}")
    
    if total_pages > 0:
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"  ✓ Created: {total_pages} pages, {size_mb:.2f}MB\n")
        return size_mb
    else:
        print(f"  ✗ No valid PDFs to merge\n")
        return 0

def split_pdf(source_pdf, output_prefix, pages_per_part):
    """Split a large PDF into smaller parts"""
    reader = pypdf.PdfReader(source_pdf)
    total_pages = len(reader.pages)
    
    print(f"Splitting {os.path.basename(source_pdf)} ({total_pages} pages)")
    
    part_num = 1
    page_start = 0
    
    while page_start < total_pages:
        page_end = min(page_start + pages_per_part, total_pages)
        
        writer = pypdf.PdfWriter()
        for page_num in range(page_start, page_end):
            writer.add_page(reader.pages[page_num])
        
        output_path = f"{output_prefix}_Part{part_num}.pdf"
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"  Part {part_num}: Pages {page_start+1}-{page_end}, {size_mb:.2f}MB")
        
        # Compress this part
        compress_pdf(output_path)
        
        page_start = page_end
        part_num += 1

def compress_pdf(input_pdf):
    """Compress PDF using Ghostscript"""
    temp_output = input_pdf.replace('.pdf', '_temp.pdf')
    
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.7',
        '-dPDFSETTINGS=/screen',  # Higher compression
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={temp_output}',
        input_pdf
    ]
    
    try:
        subprocess.run(cmd, check=True)
        compressed_size = os.path.getsize(temp_output)
        original_size = os.path.getsize(input_pdf)
        
        if compressed_size < original_size:
            os.replace(temp_output, input_pdf)
            print(f"    Compressed to {compressed_size / 1024 / 1024:.2f}MB")
        else:
            os.remove(temp_output)
    except:
        if os.path.exists(temp_output):
            os.remove(temp_output)

# Create Membership Evidence Package
print("=" * 70)
print("CREATING IEEE MEMBERSHIP EVIDENCE PACKAGE")
print("=" * 70)

member_pdfs = [
    "criteria/member/evidence/IEEE/Bylaw_IEEE_Senior Member_GradeIEEE.pdf",
    "criteria/member/evidence/IEEE/Gmail - IEEE senior member results [Reference #_ 241128-000463].pdf",
    "criteria/member/evidence/IEEE/2024 President's Letter and Vouchers_.pdf",
    "criteria/member/evidence/IEEE/100495418.pdf",
    "criteria/member/evidence/IEEE/MEMIEEE500.pdf",
    "criteria/member/evidence/IEEE/MEMYP060.pdf",
]

merge_pdfs(
    member_pdfs,
    "online/08_Membership_IEEE_Evidence.pdf",
    "Evidence of IEEE Senior Member Elevation (Outstanding Achievements Required)"
)

# Split the two large compressed files
print("=" * 70)
print("SPLITTING LARGE PACKAGES")
print("=" * 70)

# Split Scholarly Articles (was 241 pages)
split_pdf("online/03_Scholarly_Articles_Evidence_compressed.pdf", "online/03_Scholarly_Articles", 120)

# Split Media Coverage  
split_pdf("online/07_Media_Coverage_Evidence_compressed.pdf", "online/07_Media_Coverage", 120)

print("\n" + "=" * 70)
print("COMPLETE")
print("=" * 70)

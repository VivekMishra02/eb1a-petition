#!/usr/bin/env python3
"""
Split main_niw.pdf into EB2-NIW I-140 package files.
Each file <= 12MB. Files are named by section content for EB2-NIW filing.
"""

import os
import sys
import subprocess
import math
import pypdf

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def compress_pdf(input_path, output_path):
    """Compress PDF using Ghostscript"""
    cmd = [
        'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.7',
        '-dPDFSETTINGS=/printer', '-dNOPAUSE', '-dQUIET', '-dBATCH',
        '-sOutputFile=' + output_path, input_path
    ]
    subprocess.run(cmd, check=True)

def main():
    input_pdf = "main_niw.pdf"
    output_dir = "online/NIW"
    max_size_mb = 12
    max_pages_per_part = 100

    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found!")
        sys.exit(1)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Clean old files
    for f in os.listdir(output_dir):
        if f.endswith('.pdf'):
            old_path = os.path.join(output_dir, f)
            os.remove(old_path)
            print(f"Removed old file: {f}")

    reader = pypdf.PdfReader(input_pdf)
    total_pages = len(reader.pages)

    print()
    print("=" * 70)
    print("EB2-NIW PETITION SPLIT")
    print("=" * 70)
    print(f"Input: {input_pdf} ({total_pages} pages)")
    print(f"Output directory: {output_dir}/")
    print("=" * 70)

    # Page ranges based on NIW structure (0-indexed)
    # Pages 1-17: Cover, Prongs 1-3, Conclusion, List of Exhibits
    # Pages 18-19: AD-1, AD-2 (Advanced Degree)
    # Pages 20-77: NI-1 through NI-8 (National Importance)
    # Pages 78-101: WP-1 through WP-10 (Well Positioned)
    # Pages 102-367: SR-1 through SR-9 (Scholarly Publications)
    # Pages 368-384: ER-1 through ER-6 (Expert Recognition)

    packages = [
        {
            "filename": "01_Cover_Petition_and_Exhibits_List.pdf",
            "desc": "Cover Letter, Dhanasar 3-Prong Analysis, Conclusion, List of Exhibits, Advanced Degree (AD-1, AD-2)",
            "start": 0,
            "end": 19,
        },
        {
            "filename": "02_National_Importance_Evidence.pdf",
            "desc": "National Importance Evidence (Exhibits NI-1 through NI-8)",
            "start": 20,
            "end": 77,
        },
        {
            "filename": "03_Well_Positioned_Evidence_and_LOR.pdf",
            "desc": "Well Positioned Evidence & Letters of Recommendation (Exhibits WP-1 through WP-10)",
            "start": 78,
            "end": 101,
        },
        {
            "filename": "04_Scholarly_Publications.pdf",
            "desc": "Scholarly Publications (Exhibits SR-1 through SR-9)",
            "start": 102,
            "end": 367,
        },
        {
            "filename": "05_Expert_Recognition_Evidence.pdf",
            "desc": "Expert Recognition Evidence (Exhibits ER-1 through ER-6)",
            "start": 368,
            "end": total_pages - 1,
        },
    ]

    print(f"\n📦 Creating packages with correct boundaries...\n")

    all_files = []

    for pkg in packages:
        filename = pkg["filename"]
        desc = pkg["desc"]
        start = pkg["start"]
        end = pkg["end"]
        num_pages = end - start + 1

        # Check if this needs splitting into parts
        if num_pages > max_pages_per_part:
            num_parts = math.ceil(num_pages / max_pages_per_part)
            pages_per_part = math.ceil(num_pages / num_parts)
            print(f"📦 {filename} ({num_pages} pages - will split into {num_parts} parts)")

            part_num = 1
            current_start = start

            while current_start <= end:
                current_end = min(current_start + pages_per_part - 1, end)

                writer = pypdf.PdfWriter()
                for page_num in range(current_start, current_end + 1):
                    writer.add_page(reader.pages[page_num])

                base, ext = os.path.splitext(filename)
                part_filename = f"{base}_Part{part_num}{ext}"
                output_path = os.path.join(output_dir, part_filename)

                with open(output_path, 'wb') as f:
                    writer.write(f)

                part_pages = current_end - current_start + 1
                size_mb = get_file_size_mb(output_path)

                print(f"  Part {part_num}: Pages {current_start+1}-{current_end+1} ({part_pages} pages, {size_mb:.2f} MB)")

                # Compress if too large
                if size_mb > max_size_mb:
                    print(f"  ⚠ Exceeds {max_size_mb}MB - compressing...")
                    compressed_path = output_path + ".compressed"
                    try:
                        compress_pdf(output_path, compressed_path)
                        os.replace(compressed_path, output_path)
                        size_mb = get_file_size_mb(output_path)
                        print(f"  ✓ Compressed to {size_mb:.2f} MB")
                    except Exception as e:
                        print(f"  ⚠ Compression failed: {e}")
                        if os.path.exists(compressed_path):
                            os.remove(compressed_path)

                all_files.append({
                    'path': output_path,
                    'pages': part_pages,
                    'size': get_file_size_mb(output_path)
                })

                part_num += 1
                current_start = current_end + 1
        else:
            # Single file
            writer = pypdf.PdfWriter()
            for page_num in range(start, end + 1):
                writer.add_page(reader.pages[page_num])

            output_path = os.path.join(output_dir, filename)

            with open(output_path, 'wb') as f:
                writer.write(f)

            size_mb = get_file_size_mb(output_path)
            print(f"✓ {filename}")
            print(f"  Pages: {start+1}-{end+1} ({num_pages} pages, {size_mb:.2f} MB)")

            # Compress if too large
            if size_mb > max_size_mb:
                print(f"  ⚠ Exceeds {max_size_mb}MB - compressing...")
                compressed_path = output_path + ".compressed"
                try:
                    compress_pdf(output_path, compressed_path)
                    os.replace(compressed_path, output_path)
                    size_mb = get_file_size_mb(output_path)
                    print(f"  ✓ Compressed to {size_mb:.2f} MB")
                except Exception as e:
                    print(f"  ⚠ Compression failed: {e}")
                    if os.path.exists(compressed_path):
                        os.remove(compressed_path)

            all_files.append({
                'path': output_path,
                'pages': num_pages,
                'size': get_file_size_mb(output_path)
            })

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    total_size = sum(f['size'] for f in all_files)
    print(f"✓ Created {len(all_files)} package files")
    print(f"\nTotal size: {total_size:.2f} MB")

    over_limit = [f for f in all_files if f['size'] > max_size_mb]
    if over_limit:
        print(f"\n⚠ FILES OVER {max_size_mb}MB:")
        for f in over_limit:
            print(f"  {os.path.basename(f['path'])}: {f['size']:.2f} MB")
    else:
        print(f"\n✓ All files under {max_size_mb}MB USCIS limit")

    print()
    print("=" * 70)
    print(f"✓ Files ready in {output_dir}/")
    print("=" * 70)

if __name__ == "__main__":
    main()

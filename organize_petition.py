#!/usr/bin/env python3
"""
EB1-A Petition Evidence Organizer for USCIS Online Filing
Creates organized evidence packages by combining source files from criteria directories
"""

import pypdf
import os
import subprocess
import shutil
from pathlib import Path

# Configuration
OUTPUT_DIR = "online"
MAX_FILE_SIZE_MB = 12
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def get_file_size_mb(filepath):
    """Get file size in MB"""
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / 1024 / 1024
    return 0

def merge_pdfs(pdf_files, output_path, description):
    """Merge multiple PDF files into one"""
    print(f"\nCreating: {os.path.basename(output_path)}")
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
        
        size_mb = get_file_size_mb(output_path)
        print(f"  ✓ Created: {total_pages} pages, {size_mb:.2f}MB")
        return size_mb
    else:
        print(f"  ✗ No valid PDFs to merge")
        return 0

def compress_pdf(input_pdf, max_size_bytes=MAX_FILE_SIZE_BYTES):
    """Compress PDF using Ghostscript if it exceeds max size"""
    file_size = os.path.getsize(input_pdf)
    
    if file_size <= max_size_bytes:
        print(f"  ✓ File size OK: {file_size / 1024 / 1024:.2f}MB")
        return True
    
    print(f"  ⚠ File too large: {file_size / 1024 / 1024:.2f}MB, compressing...")
    temp_output = input_pdf.replace('.pdf', '_compressed.pdf')
    
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.7',
        '-dPDFSETTINGS=/ebook',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={temp_output}',
        input_pdf
    ]
    
    try:
        subprocess.run(cmd, check=True)
        compressed_size = os.path.getsize(temp_output)
        
        if compressed_size <= max_size_bytes:
            os.replace(temp_output, input_pdf)
            print(f"  ✓ Compressed to: {compressed_size / 1024 / 1024:.2f}MB")
            return True
        else:
            os.remove(temp_output)
            print(f"  ✗ Still too large after compression: {compressed_size / 1024 / 1024:.2f}MB")
            print(f"     This package needs to be split into multiple files.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Compression failed: {e}")
        if os.path.exists(temp_output):
            os.remove(temp_output)
        return False

def copy_image_as_pdf(image_path, output_pdf):
    """Convert image to PDF (simple copy for now)"""
    # For images (JPG, PNG), we can upload them directly or convert to PDF
    # USCIS accepts JPG/JPEG directly, so we can just copy
    ext = os.path.splitext(image_path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        # For simplicity, just note these need separate handling
        return None
    return None

def create_evidence_packages():
    """Create organized evidence packages"""
    
    print("EB1-A Petition Evidence Organizer")
    print("=" * 70)
    print(f"Output directory: {OUTPUT_DIR}/")
    print(f"Maximum file size: {MAX_FILE_SIZE_MB}MB")
    print()
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    packages = []
    warnings = []
    
    # Package 1: Cover Documents
    # Note: These are typically generated from LaTeX, so we'll create a placeholder note
    
    # Package 2: Original Contributions Evidence
    original_pdfs = [
        "criteria/original/evidence/AgentSystemDesign_vivek_IEEE.pdf",
        "criteria/original/evidence/Appreciation Letter_Mr. Vivek Kumar Mishra.pdf",
        "criteria/original/evidence/bookPost.pdf",
        "criteria/original/evidence/FDP_Program.pdf",
        "criteria/original/evidence/Announcing The Shops at Chase – A New Way for Chase Cardmembers to Shop and Save.pdf",
        "criteria/scholar/LOR/MaximLetter.pdf",
        "LOR/FinalLetters/Rahul_Vishwakarma.pdf",
        "criteria/original/evidence/Sunil_Supaul_Engineering_College.pdf",
    ]
    
    size = merge_pdfs(
        original_pdfs,
        os.path.join(OUTPUT_DIR, "02_Original_Contributions_Evidence.pdf"),
        "Evidence of Original Contributions of Major Significance"
    )
    packages.append(("02_Original_Contributions_Evidence.pdf", size))
    
    # Add note about images
    print("  Note: Images (Er Vivek.jpg, chaseWork.png, Shop_At_Chase.png, RA_OFFER_Letter.jpg)")
    print("        will be included in criterion-specific exhibits or can be uploaded as JPG")
    
    # Package 3: Scholarly Articles
    scholar_pdfs = [
        "criteria/scholar/evidence/Integrating-Solar-Photovoltaic-Systems-into-the-Grid-An-Overview-of-AI-Application.pdf",
        "criteria/scholar/evidence/The Role of Generative AI.pdf",
        "criteria/scholar/evidence/sustainability-16-08077.pdf",
        "criteria/scholar/evidence/Connectivity evaluations.pdf",
        "criteria/scholar/evidence/Evaluating Financing Mechanisms and Economic Benefits to Fund Gra.pdf",
        "criteria/scholar/evidence/Evaluating Innovative Financing.pdf",
        "criteria/scholar/evidence/FundingHighSpeed.pdf",
        "criteria/scholar/evidence/Optimizing Multimodal Transportation Access to Support Commuting.pdf",
    ]
    
    size = merge_pdfs(
        scholar_pdfs,
        os.path.join(OUTPUT_DIR, "03_Scholarly_Articles_Evidence.pdf"),
        "Evidence of Authorship of Scholarly Articles"
    )
    packages.append(("03_Scholarly_Articles_Evidence.pdf", size))
    
    # Package 4: Judging Evidence (Part 1 - Conference Reviews)
    judging_pdfs_part1 = [
        "criteria/judge/evidence/OpenReview/ICLR_2025_FM-Wild_Reviewer_Invitation.pdf",
        "criteria/judge/evidence/OpenReview/ICLR_2025_FM-Wild_Paper62_Review_Posted.pdf",
        "criteria/judge/evidence/OpenReview/ICLR_2025_FM-Wild_Paper62_Review_Received.pdf",
        "criteria/judge/evidence/OpenReview/NeurIPS_2025_Position_Paper_Reviewer_Invitation.pdf",
        "criteria/judge/evidence/MicrosoftCMT/Gmail - Reviewer Invitation for Graph Signal Processing Workshop 2025.pdf",
        "criteria/judge/evidence/MicrosoftCMT/Gmail - GSP2025 _ Paper 17.pdf",
        "criteria/judge/evidence/MicrosoftCMT/ACDSA2026_Reviewer_Invitation.pdf",
        "criteria/judge/evidence/MicrosoftCMT/Gmail - ACDSA2026 _ Paper 1105.pdf",
        "criteria/judge/evidence/MicrosoftCMT/Bengali Sentiment Analysis_invitation_.pdf",
    ]
    
    size = merge_pdfs(
        judging_pdfs_part1,
        os.path.join(OUTPUT_DIR, "04A_Judging_Conference_Reviews.pdf"),
        "Judging Evidence - Part A: Conference and Workshop Reviews"
    )
    packages.append(("04A_Judging_Conference_Reviews.pdf", size))
    
    # Package 4B: Judging Evidence (Part 2 - IEEE & Journal Reviews)
    judging_pdfs_part2 = [
        "criteria/judge/evidence/IEEE Review/Invitation to the Senior Member Application Virtual Review Panel - June 2025.pdf",
        "criteria/judge/evidence/IEEE Review/COMPLETE - 29-Jun-2025 Senior Member Panel.pdf",
        "criteria/judge/evidence/IEEE Review/Thank you letter template-SM Panelist_100495418.pdf",
        "criteria/judge/evidence/hackathon/Virtus_1review_Risk Governance and Control_ Financial Markets & Institution.pdf",
        "criteria/judge/evidence/hackathon/Virtus_2_Regarding review_Corporate & Business Strategy Review.pdf",
        "criteria/judge/evidence/hackathon/Informatica_Article Review Request.pdf",
        "criteria/judge/evidence/hackathon/Judge Certification Letter - Vivek (2).pdf",
        "criteria/judge/evidence/hackathon/DrgonHacks.pdf",
        "criteria/judge/evidence/hackathon/VivekMishra_ClaroJudge24.pdf",
        "criteria/judge/evidence/hackathon/acknowledgement letter.pdf",
    ]
    
    size = merge_pdfs(
        judging_pdfs_part2,
        os.path.join(OUTPUT_DIR, "04B_Judging_IEEE_and_Journal_Reviews.pdf"),
        "Judging Evidence - Part B: IEEE Panel, Journal Reviews, and Hackathon Judging"
    )
    packages.append(("04B_Judging_IEEE_and_Journal_Reviews.pdf", size))
    
    # Package 4C: NeurIPS Additional Evidence
    judging_pdfs_part3 = [
        "criteria/judge/evidence/OpenReview/NeurIPS_Paper110_OpenReview_Page.pdf",
        "criteria/judge/evidence/OpenReview/NeurIPS_2025_Paper110_Review_Posted.pdf",
        "criteria/judge/evidence/OpenReview/NeurIPS_Paper156_OpenReview_Page.pdf",
        "criteria/judge/evidence/OpenReview/NeurIPS_2025_Paper156_Review_Posted.pdf",
        "criteria/judge/evidence/OpenReview/NeurIPS_Paper598_OpenReview_Page.pdf",
        "criteria/judge/evidence/OpenReview/NeurIPS_2025_Paper598_Review_Posted.pdf",
    ]
    
    size = merge_pdfs(
        judging_pdfs_part3,
        os.path.join(OUTPUT_DIR, "04C_Judging_NeurIPS_Reviews.pdf"),
        "Judging Evidence - Part C: NeurIPS 2025 Position Paper Reviews"
    )
    packages.append(("04C_Judging_NeurIPS_Reviews.pdf", size))
    
    # Package 5: Critical Role Evidence
    critical_pdfs = [
        "criteria/critical/evidence/Announcing The Shops at Chase – A New Way for Chase Cardmembers to Shop and Save.pdf",
        "criteria/critical/evidence/AWS Certified Cloud Practitioner certificate.pdf",
        "criteria/critical/evidence/getLetter.pdf",
        "criteria/critical/evidence/JobOfferLetter_ACCEPTED_SoftwareEngineer_210921_192618.pdf",
    ]
    
    size = merge_pdfs(
        critical_pdfs,
        os.path.join(OUTPUT_DIR, "05_Critical_Role_Evidence.pdf"),
        "Evidence of Leading/Critical Role"
    )
    packages.append(("05_Critical_Role_Evidence.pdf", size))
    
    print("  Note: Critical role images (chaseWork.png, TracyJPMorgan.png, kalyanAppreciationJPMCHASE.png,")
    print("        JPMC_VP_Appreciations.png, coverage.png, RA_OFFER_Letter.jpg)")
    print("        can be uploaded as separate JPG files or combined into a supplementary PDF")
    
    # Package 6: Letters of Recommendation
    lor_dir = Path("LOR/FinalLetters")
    lor_pdfs = []
    if lor_dir.exists():
        for pdf_file in lor_dir.glob("*.pdf"):
            lor_pdfs.append(str(pdf_file))
    
    if lor_pdfs:
        size = merge_pdfs(
            lor_pdfs,
            os.path.join(OUTPUT_DIR, "06_Letters_of_Recommendation.pdf"),
            "Letters of Recommendation from Expert Referees"
        )
        packages.append(("06_Letters_of_Recommendation.pdf", size))
    
    # Package 7: Media Coverage
    media_pdfs = [
        "criteria/media/evidence/TechBullion_Interview.pdf",
        "criteria/media/evidence/IEEE_Transmitter_Profile.pdf",
        "criteria/media/evidence/IEEE_TV_Profile.pdf",
        "criteria/media/evidence/DainikBhaskar_Translation.pdf",
        "criteria/media/evidence/RajasthanPatrika_Translation.pdf",
        "criteria/media/evidence/FirstIndia.pdf",
        "criteria/media/evidence/TechTarget_Trends_2025.pdf",
        "criteria/media/evidence/TechTarget_Sustainability.pdf",
        "criteria/media/evidence/VKTR_AI_Productivity.pdf",
    ]
    
    size = merge_pdfs(
        media_pdfs,
        os.path.join(OUTPUT_DIR, "07_Media_Coverage_Evidence.pdf"),
        "Evidence of Published Material About Beneficiary"
    )
    packages.append(("07_Media_Coverage_Evidence.pdf", size))
    
    print("  Note: Media images (IeeeTwitter.png, IeeeTwitter1.png, Dainik_Bhaskar.png, Dice_Article.png)")
    print("        can be uploaded as JPG or combined into supplementary PDF")
    
    # Compress packages that exceed size limit
    print("\n" + "=" * 70)
    print("VERIFYING FILE SIZES")
    print("=" * 70)
    
    needs_split = []
    for filename, size_mb in packages:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            if size_mb > MAX_FILE_SIZE_MB:
                if not compress_pdf(filepath):
                    needs_split.append(filename)
                    warnings.append(f"⚠ {filename} still exceeds 12MB after compression - needs manual split")
            else:
                print(f"✓ {filename}: {size_mb:.2f}MB")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Created {len(packages)} evidence packages in {OUTPUT_DIR}/")
    
    if warnings:
        print("\n⚠ WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    print("\nNOTE: Cover documents, images, and criterion narratives need separate handling.")
    print("      See UPLOAD_CHECKLIST.md for complete instructions.")

if __name__ == "__main__":
    create_evidence_packages()

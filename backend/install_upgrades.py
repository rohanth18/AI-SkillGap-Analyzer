"""
Installation script for upgraded features
Installs new dependencies and downloads required models
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     AI SkillGap Analyzer - Upgrade Installation         ║
    ║                                                          ║
    ║  This script will install:                              ║
    ║  1. sentence-transformers (SBERT)                       ║
    ║  2. textstat (readability analysis)                     ║
    ║  3. torch (PyTorch for SBERT)                           ║
    ║  4. spaCy English model                                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    input("Press Enter to continue...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("\n⚠️  WARNING: You are not in a virtual environment!")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            return
    
    success_count = 0
    total_steps = 5
    
    # Step 1: Install sentence-transformers
    if run_command(
        f"{sys.executable} -m pip install sentence-transformers==2.2.2",
        "Installing sentence-transformers (SBERT)"
    ):
        success_count += 1
    
    # Step 2: Install textstat
    if run_command(
        f"{sys.executable} -m pip install textstat==0.7.3",
        "Installing textstat (readability analysis)"
    ):
        success_count += 1
    
    # Step 3: Install torch (if not already installed)
    if run_command(
        f"{sys.executable} -m pip install torch==2.0.1",
        "Installing PyTorch"
    ):
        success_count += 1
    
    # Step 4: Download spaCy model
    if run_command(
        f"{sys.executable} -m spacy download en_core_web_sm",
        "Downloading spaCy English model"
    ):
        success_count += 1
    
    # Step 5: Download SBERT model (first time)
    print(f"\n{'='*60}")
    print("📦 Downloading SBERT model (all-MiniLM-L6-v2)")
    print(f"{'='*60}")
    
    try:
        from sentence_transformers import SentenceTransformer
        print("Loading SBERT model (this may take a minute)...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ SBERT model downloaded successfully")
        success_count += 1
    except Exception as e:
        print(f"❌ Failed to download SBERT model: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 INSTALLATION SUMMARY")
    print(f"{'='*60}")
    print(f"Completed: {success_count}/{total_steps} steps")
    
    if success_count == total_steps:
        print("\n✅ ALL INSTALLATIONS SUCCESSFUL!")
        print("\n🚀 You can now use the upgraded features:")
        print("   - SBERT-based skill extraction")
        print("   - Resume quality scoring")
        print("   - PDF report generation")
        print("   - Enhanced confidence scoring")
    else:
        print(f"\n⚠️  {total_steps - success_count} step(s) failed")
        print("Please check the errors above and try again.")
    
    print(f"\n{'='*60}")
    print("📝 Next Steps:")
    print(f"{'='*60}")
    print("1. Test the modules:")
    print("   python sbert_extractor.py")
    print("   python resume_quality_scorer.py")
    print("   python pdf_generator.py")
    print("   python enhanced_scoring.py")
    print("\n2. Update app.py to integrate new features")
    print("\n3. Update database schema with new columns")
    print("\n4. Update frontend to display new data")
    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()

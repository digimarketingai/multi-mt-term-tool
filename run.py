#!/usr/bin/env python3
"""
🔤 Multi-MT Term Comparison Tool - Launcher
Run this script to start the web interface.

Usage:
    python run.py
    python run.py --share    # Create public link
    python run.py --local    # Local only (no public link)
"""

import subprocess
import sys
import argparse

def install_requirements():
    """Install required packages."""
    print("=" * 60)
    print("🔧 Installing required packages... 正在安裝套件...")
    print("=" * 60)
    
    packages = ["deep-translator", "translators", "gradio"]
    
    for pkg in packages:
        try:
            print(f"   📦 Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
            print(f"   ✅ {pkg} installed")
        except Exception as e:
            print(f"   ⚠️ Could not install {pkg}: {e}")
    
    print("\n✅ Installation complete!\n")

def main():
    parser = argparse.ArgumentParser(description="Multi-MT Term Comparison Tool")
    parser.add_argument("--share", action="store_true", help="Create public shareable link")
    parser.add_argument("--local", action="store_true", help="Local only (default creates public link)")
    parser.add_argument("--no-install", action="store_true", help="Skip package installation")
    args = parser.parse_args()
    
    # Install packages
    if not args.no_install:
        install_requirements()
    
    # Import after installation
    from mt_term_tool import MultiMTTranslator, create_gradio_interface
    
    print("\n" + "=" * 60)
    print("🔤 MULTI-MT TERM COMPARISON TOOL")
    print("   多引擎術語翻譯比較工具")
    print("=" * 60)
    
    # Initialize translator
    translator = MultiMTTranslator()
    
    if not translator.engines:
        print("\n❌ No translation engines available!")
        return
    
    print(f"\n✅ Available engines: {', '.join(translator.get_available_engines())}")
    
    # Create and launch interface
    print("\n🚀 Starting web interface...")
    demo = create_gradio_interface(translator)
    
    if demo:
        share = not args.local  # Default to share=True unless --local
        if args.share:
            share = True
        demo.launch(share=share, debug=False)
    else:
        print("❌ Could not create interface. Please install gradio.")

if __name__ == "__main__":
    main()

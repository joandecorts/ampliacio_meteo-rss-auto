#!/usr/bin/env python3
"""
EXECUTOR DEL BANNER - Versió simplificada
"""

import subprocess
import time
import sys

def main():
    print("🚀 Iniciant generador de banner...")
    print("📁 Executant generate_banner.py...")
    
    try:
        # Executa el script principal
        result = subprocess.run([sys.executable, "generate_banner.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Advertències:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("\n✅ Banner generat amb èxit!")
            print("📄 Fitxer: banner_output.html")
            print("🔧 Obre-lo amb el navegador o configura a OBS.")
        else:
            print("\n❌ Error generant el banner")
            
    except Exception as e:
        print(f"❌ Error executant: {e}")

if __name__ == "__main__":
    main()

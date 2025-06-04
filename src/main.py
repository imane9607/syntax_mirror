import tkinter as tk
import traceback
import sys
from src.gui.editor import SyntaxHighlighterGUI

def main():
    """
    Syntax Mirror - Real-time Syntax Highlighter
    Main entry point for the application
    """
    try:
        print("Syntax Mirror başlatılıyor...")
        
        # Create main window
        root = tk.Tk()
        
        # Set window icon and title
        root.title("Syntax Mirror")
        
        # Uygulamayı oluştur ve başlat
        app = SyntaxHighlighterGUI(root)
        
        print("Uygulama başarıyla başlatıldı!")
        
        # Ana döngüyü başlat
        root.mainloop()
    except Exception as e:
        print(f"Uygulama başlatılırken hata oluştu: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 
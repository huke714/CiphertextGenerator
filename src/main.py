"""
Main Entrypoint for Deceptive Document Stream Transformer (HTML5 UI)
"""
import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from doc_stream_app import main

if __name__ == "__main__":
    main()

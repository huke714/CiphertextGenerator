"""
Application Launcher
Runs the Deceptive Document Stream Transformer from workspace root.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from doc_stream_app import main

if __name__ == "__main__":
    main()

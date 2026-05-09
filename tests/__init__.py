"""
Test suite for Anita Agent Self-Healing System
"""
import sys
from pathlib import Path

# Add source directories to path
base_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_path / "SANDKASSE" / "07_Sandkasse_SelfHealing"))

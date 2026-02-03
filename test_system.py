"""
Quick test script to verify all components are working
Run this before launching the main app
"""
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import pandas as pd
        print("  ✅ Pandas")
    except ImportError:
        print("  ❌ Pandas not found. Run: pip install pandas")
        return False
    
    try:
        import plotly
        print("  ✅ Plotly")
    except ImportError:
        print("  ❌ Plotly not found. Run: pip install plotly")
        return False
    
    try:
        import streamlit
        print("  ✅ Streamlit")
    except ImportError:
        print("  ❌ Streamlit not found. Run: pip install streamlit")
        return False
    
    try:
        import numpy
        print("  ✅ NumPy")
    except ImportError:
        print("  ❌ NumPy not found. Run: pip install numpy")
        return False
    
    return True


def test_mock_data():
    """Test mock data generation"""
    print("\n🎮 Testing mock data generation...")
    
    try:
        from mock_data import get_lol_mock_data, get_valorant_mock_data
        
        lol_data = get_lol_mock_data(num_matches=3)
        print(f"  ✅ Generated {len(lol_data)} LoL matches")
        print(f"     - Sample match: {lol_data[0]['match_id']}")
        print(f"     - Kills: {len(lol_data[0]['kills'])}, Dragons: {len(lol_data[0]['dragons'])}")
        
        val_data = get_valorant_mock_data(num_matches=3)
        print(f"  ✅ Generated {len(val_data)} VALORANT matches")
        print(f"     - Sample match: {val_data[0]['match_id']}")
        print(f"     - Score: {val_data[0]['team_score']}-{val_data[0]['enemy_score']}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_analyzers():
    """Test analysis engines"""
    print("\n📊 Testing analyzers...")
    
    try:
        from mock_data import get_lol_mock_data, get_valorant_mock_data
        from analyzers import LolAnalyzer, ValorantAnalyzer
        
        # Test LoL analyzer
        lol_matches = get_lol_mock_data(num_matches=5)
        lol_analyzer = LolAnalyzer(lol_matches)
        lol_stats = lol_analyzer.get_complete_analysis()
        print(f"  ✅ LoL Analyzer working")
        print(f"     - Win rate: {lol_stats['win_rate']:.1f}%")
        print(f"     - First dragon rate: {lol_stats['objective_control']['first_dragon_rate']:.1f}%")
        
        # Test VALORANT analyzer
        val_matches = get_valorant_mock_data(num_matches=5)
        val_analyzer = ValorantAnalyzer(val_matches)
        val_stats = val_analyzer.get_complete_analysis()
        print(f"  ✅ VALORANT Analyzer working")
        print(f"     - Win rate: {val_stats['match_win_rate']:.1f}%")
        print(f"     - First blood rate: {val_stats['opening_duel_stats']['first_blood_rate']:.1f}%")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent():
    """Test AI agent (mock mode)"""
    print("\n🤖 Testing AI agent...")
    
    try:
        from mock_data import get_lol_mock_data
        from analyzers import LolAnalyzer
        from agent import generate_scouting_report
        
        lol_matches = get_lol_mock_data(num_matches=5)
        lol_analyzer = LolAnalyzer(lol_matches)
        stats = lol_analyzer.get_complete_analysis()
        
        report = generate_scouting_report(stats, "lol", "mock")
        print(f"  ✅ AI Agent working (mock mode)")
        print(f"     - Report length: {len(report)} characters")
        print(f"     - Contains 'WIN CONDITION': {'THE WIN CONDITION' in report}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🎯 VANGUARD - System Verification Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Mock Data", test_mock_data()))
    results.append(("Analyzers", test_analyzers()))
    results.append(("AI Agent", test_agent()))
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🚀 ALL TESTS PASSED! You're ready to run the app!")
        print("\nTo start the application, run:")
        print("    streamlit run main.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running the app.")
        print("\nMake sure you've installed all dependencies:")
        print("    pip install -r requirements.txt")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

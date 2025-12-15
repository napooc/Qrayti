"""
Test script for the Qrayti API.
Run this to verify your backend is working correctly.
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test the health endpoint."""
    print_section("Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("model_ready"):
                print("✅ Health check passed - Model is ready!")
                return True
            else:
                print("⚠️  Server is running but model is not ready")
                print("   Check your .env configuration and API key")
                return False
        else:
            print("❌ Health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("   Make sure the server is running: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_quiz_generation():
    """Test quiz generation."""
    print_section("Testing Quiz Generation")
    
    content = """
    Le Dahir des Obligations et Contrats (DOC) est le texte fondamental qui régit 
    le droit civil au Maroc. Promulgué en 1913, il définit les règles essentielles 
    des relations entre personnes privées. Les principes fondamentaux incluent la 
    liberté contractuelle, l'autonomie de la volonté, et la bonne foi dans 
    l'exécution des contrats.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate-quiz",
            json={
                "content": content,
                "num_questions": 3
            },
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generated {len(data['questions'])} questions")
            
            # Print first question as example
            if data['questions']:
                q = data['questions'][0]
                print("\nExample Question:")
                print(f"  Q: {q['question']}")
                print(f"  Options: {q['options']}")
                print(f"  Correct Answer: {q['options'][q['correctIndex']]}")
                print(f"  Explanation: {q['explanation'][:100]}...")
            
            return True
        else:
            print(f"❌ Quiz generation failed: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⚠️  Request timed out - this might take a while with AI models")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_summary_generation():
    """Test summary generation."""
    print_section("Testing Summary Generation")
    
    content = """
    Le Dahir des Obligations et Contrats (DOC) est le texte fondamental qui régit 
    le droit civil au Maroc. Promulgué en 1913, il définit les règles essentielles 
    des relations entre personnes privées. Les principes fondamentaux incluent la 
    liberté contractuelle, l'autonomie de la volonté, et la bonne foi dans 
    l'exécution des contrats. Le contrat est défini comme l'accord de deux ou 
    plusieurs volontés en vue de créer des effets de droit.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate-summary",
            json={"content": content},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generated {len(data['sections'])} summary sections")
            
            # Print first section as example
            if data['sections']:
                section = data['sections'][0]
                print("\nExample Section:")
                print(f"  Title: {section['title']}")
                print(f"  Content: {section['content'][:100]}...")
                print(f"  Key Terms: {len(section['keyTerms'])}")
                print(f"  Essential Points: {len(section['essentialPoints'])}")
            
            return True
        else:
            print(f"❌ Summary generation failed: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⚠️  Request timed out - this might take a while with AI models")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("\n🚀 Qrayti API Test Suite")
    print(f"Testing API at: {BASE_URL}")
    
    results = []
    
    # Test health
    health_ok = test_health()
    results.append(("Health Check", health_ok))
    
    if not health_ok:
        print("\n⚠️  Server or model not ready. Skipping other tests.")
        print("   Please check your .env configuration and make sure:")
        print("   1. The server is running (python main.py)")
        print("   2. Your OPENAI_API_KEY is set correctly in .env")
        sys.exit(1)
    
    # Test quiz generation
    quiz_ok = test_quiz_generation()
    results.append(("Quiz Generation", quiz_ok))
    
    # Test summary generation
    summary_ok = test_summary_generation()
    results.append(("Summary Generation", summary_ok))
    
    # Print summary
    print_section("Test Summary")
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! Your backend is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Test script to verify frontend implementation
"""
import os
import sys
from pathlib import Path

def test_file_structure():
    """Test that all required files exist"""
    frontend_dir = Path(__file__).parent
    
    required_files = [
        'index.html',
        'css/styles.css',
        'css/input.css',
        'js/app.js',
        'js/api.js',
        'js/components.js',
        'js/config.js',
        'js/pages.js',
        'package.json',
        'tailwind.config.js'
    ]
    
    print("📁 Checking file structure...")
    
    missing_files = []
    for file_path in required_files:
        full_path = frontend_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_html_structure():
    """Test HTML structure and content"""
    frontend_dir = Path(__file__).parent
    index_file = frontend_dir / 'index.html'
    
    print("\n📄 Checking HTML structure...")
    
    if not index_file.exists():
        print("   ❌ index.html not found")
        return False
    
    content = index_file.read_text()
    
    required_elements = [
        'id="app"',
        'id="loading-screen"',
        'id="main-header"',
        'id="page-content"',
        'id="error-modal"',
        'id="success-toast"',
        'js/config.js',
        'js/api.js',
        'js/components.js',
        'js/pages.js',
        'js/app.js'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element in content:
            print(f"   ✅ {element}")
        else:
            print(f"   ❌ {element} (missing)")
            missing_elements.append(element)
    
    return len(missing_elements) == 0

def test_css_build():
    """Test that CSS has been built"""
    frontend_dir = Path(__file__).parent
    styles_file = frontend_dir / 'css' / 'styles.css'
    
    print("\n🎨 Checking CSS build...")
    
    if not styles_file.exists():
        print("   ❌ styles.css not found - run 'npm run build' to generate it")
        return False
    
    content = styles_file.read_text()
    
    # Check for TailwindCSS classes
    tailwind_indicators = [
        'tailwindcss',
        '.btn-primary',
        '.card',
        '.badge'
    ]
    
    found_indicators = []
    for indicator in tailwind_indicators:
        if indicator in content:
            found_indicators.append(indicator)
    
    if len(found_indicators) >= 2:
        print(f"   ✅ TailwindCSS build detected ({len(found_indicators)} indicators found)")
        return True
    else:
        print(f"   ❌ TailwindCSS build may be incomplete ({len(found_indicators)} indicators found)")
        return False

def test_javascript_syntax():
    """Basic JavaScript syntax check"""
    frontend_dir = Path(__file__).parent
    js_files = [
        'js/config.js',
        'js/api.js', 
        'js/components.js',
        'js/pages.js',
        'js/app.js'
    ]
    
    print("\n🔧 Checking JavaScript files...")
    
    all_valid = True
    for js_file in js_files:
        file_path = frontend_dir / js_file
        if file_path.exists():
            content = file_path.read_text()
            
            # Basic syntax checks
            if content.count('{') != content.count('}'):
                print(f"   ❌ {js_file} - Mismatched braces")
                all_valid = False
            elif content.count('(') != content.count(')'):
                print(f"   ❌ {js_file} - Mismatched parentheses")
                all_valid = False
            else:
                print(f"   ✅ {js_file} - Basic syntax OK")
        else:
            print(f"   ❌ {js_file} - File not found")
            all_valid = False
    
    return all_valid

def test_package_json():
    """Test package.json configuration"""
    frontend_dir = Path(__file__).parent
    package_file = frontend_dir / 'package.json'
    
    print("\n📦 Checking package.json...")
    
    if not package_file.exists():
        print("   ❌ package.json not found")
        return False
    
    try:
        import json
        with open(package_file) as f:
            package_data = json.load(f)
        
        required_deps = ['tailwindcss', '@tailwindcss/forms']
        required_scripts = ['build', 'dev']
        
        # Check dependencies
        dev_deps = package_data.get('devDependencies', {})
        missing_deps = [dep for dep in required_deps if dep not in dev_deps]
        
        if missing_deps:
            print(f"   ❌ Missing dependencies: {missing_deps}")
            return False
        else:
            print(f"   ✅ All required dependencies found")
        
        # Check scripts
        scripts = package_data.get('scripts', {})
        missing_scripts = [script for script in required_scripts if script not in scripts]
        
        if missing_scripts:
            print(f"   ❌ Missing scripts: {missing_scripts}")
            return False
        else:
            print(f"   ✅ All required scripts found")
        
        return True
        
    except json.JSONDecodeError:
        print("   ❌ Invalid JSON in package.json")
        return False
    except Exception as e:
        print(f"   ❌ Error reading package.json: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing English Assistant Frontend...")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("HTML Structure", test_html_structure),
        ("CSS Build", test_css_build),
        ("JavaScript Syntax", test_javascript_syntax),
        ("Package Configuration", test_package_json)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Frontend is ready.")
        print("\nTo start the frontend:")
        print("   python3 serve.py")
        print("\nTo rebuild CSS:")
        print("   npm run build")
    else:
        print(f"\n💥 {len(results) - passed} test(s) failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
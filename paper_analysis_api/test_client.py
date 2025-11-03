"""
Simple test client for Paper Analysis API
Tests the API with the example PDF
"""

import requests
from pathlib import Path

# API configuration
API_URL = "http://localhost:8000/api/v1/analyze"
PDF_PATH = r"C:\Users\gridone\Downloads\추출\analyzing_uncertainty_of_llm.pdf"
MAX_PAGES = 10


def test_analysis_api():
    """Test paper analysis API endpoint"""

    pdf_file = Path(PDF_PATH)

    if not pdf_file.exists():
        print(f"❌ PDF file not found: {PDF_PATH}")
        return

    print("=" * 70)
    print("🧪 Testing Paper Analysis API")
    print("=" * 70)
    print(f"\n📄 PDF: {pdf_file.name}")
    print(f"📊 Max Pages: {MAX_PAGES}")
    print(f"🌐 API URL: {API_URL}\n")

    try:
        # Prepare request
        with open(pdf_file, "rb") as f:
            files = {"file": (pdf_file.name, f, "application/pdf")}
            params = {"max_pages": MAX_PAGES}

            print("📤 Uploading PDF and requesting analysis...")
            print("⏳ This may take several minutes...\n")

            # Send request
            response = requests.post(
                API_URL,
                files=files,
                params=params,
                timeout=600  # 10 minutes timeout
            )

        # Check response
        if response.status_code == 200:
            result = response.json()

            print("=" * 70)
            print("✅ Analysis Completed Successfully!")
            print("=" * 70)
            print(f"\n📝 PDF: {result['pdf_filename']}")
            print(f"📄 Pages Analyzed: {result['total_pages']}")
            print(f"⏰ Timestamp: {result['analysis_timestamp']}")
            print(f"🤖 Model: {result['model_used']}")
            if result.get('output_path'):
                print(f"💾 Saved To: {result['output_path']}")

            # Show preview
            print("\n" + "=" * 70)
            print("📖 Analysis Preview (First 1500 characters)")
            print("=" * 70)
            preview = result['markdown_content'][:1500]
            print(preview + "...\n")

            # Save to file
            output_file = Path("test_analysis_result.md")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result['markdown_content'])

            print(f"💾 Full result saved to: {output_file.absolute()}\n")

        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error: {response.text}\n")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the API server running?")
        print("   Start it with: python -m uvicorn paper_analysis_api.main:app --reload\n")

    except requests.exceptions.Timeout:
        print("❌ Request timed out. Analysis may take longer than expected.\n")

    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")


if __name__ == "__main__":
    test_analysis_api()

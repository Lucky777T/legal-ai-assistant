@echo off
echo ========================================
echo LEGAL AI ASSISTANT - COMPLETE SETUP
echo ========================================
echo.

echo Step 1: Checking Python version...
python --version
if errorlevel 1 (
    echo Python not found. Please install Python 3.12+
    echo Download from: https://www.python.org/downloads/release/python-3129/
    pause
    exit /b 1
)

echo.
echo Step 2: Creating virtual environment...
if exist venv (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

py -3.12 -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    echo Make sure Python 3.12 is installed.
    pause
    exit /b 1
)

echo.
echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 4: Upgrading pip and installing build tools...
python -m pip install --upgrade pip
pip install setuptools==70.0.0 wheel==0.43.0

echo.
echo Step 5: Creating requirements.txt with all dependencies...
(
echo fastapi==0.104.1
echo uvicorn[standard]==0.24.0
echo pydantic==2.5.3
echo pydantic-core==2.14.6
echo python-dotenv==1.0.0
echo requests==2.31.0
echo httpx==0.25.2
echo pypdf2==3.0.1
echo openai==1.6.1
echo numpy==1.26.0
echo pandas==2.1.4
echo tqdm==4.66.1
echo pytest==7.4.3
echo transformers==4.35.2
echo torch==2.2.2
echo torchvision==0.17.2
echo torchaudio==2.2.2
echo sentence-transformers==2.2.2
echo langchain==0.1.0
echo langchain-community==0.0.10
echo chromadb==0.4.22
) > requirements.txt

echo.
echo Step 6: Installing packages in optimal order...
echo Installing numpy and pandas first...
pip install numpy==1.26.0 pandas==2.1.4 --only-binary=:all:

echo Installing PyTorch for Windows...
pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu

echo Installing core dependencies...
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pydantic==2.5.3 pydantic-core==2.14.6

echo Installing utility packages...
pip install python-dotenv==1.0.0 requests==2.31.0 httpx==0.25.2 pypdf2==3.0.1 tqdm==4.66.1 pytest==7.4.3

echo Installing OpenAI...
pip install openai==1.6.1

echo Installing transformers and sentence-transformers...
pip install transformers==4.35.2
pip install sentence-transformers==2.2.2

echo Installing LangChain and ChromaDB...
pip install langchain==0.1.0 langchain-community==0.0.10 chromadb==0.4.22

echo.
echo Step 7: Creating project structure...
mkdir app\core 2>nul
mkdir app\routers 2>nul
mkdir app\models 2>nul
mkdir app\services 2>nul
mkdir app\utils 2>nul
mkdir scripts 2>nul
mkdir tests 2>nul
mkdir sample_docs 2>nul
mkdir data 2>nul
mkdir client\templates 2>nul
mkdir client\static 2>nul
mkdir docker\nginx 2>nul

echo.
echo Step 8: Creating essential files...
type nul > app\__init__.py
type nul > app\main.py
type nul > app\config.py
type nul > app\core\__init__.py
type nul > app\core\endee_client.py
type nul > app\core\document_processor.py
type nul > app\core\embedding_service.py
type nul > docker-compose.endee.yml
type nul > .env.example
type nul > README.md
type nul > Dockerfile

echo.
echo Step 9: Verifying installation...
echo.
python -c "
import sys
print('Python version:', sys.version.split()[0])

packages_to_check = [
    ('fastapi', '0.104.1'),
    ('pydantic', '2.5.3'),
    ('numpy', '1.26.0'),
    ('pandas', '2.1.4'),
    ('openai', '1.6.1'),
    ('torch', '2.2.2'),
    ('transformers', '4.35.2'),
    ('langchain', '0.1.0'),
    ('chromadb', '0.4.22')
]

print('\\nChecking installed packages:')
for pkg, expected in packages_to_check:
    try:
        import importlib
        module = importlib.import_module(pkg.replace('-', '_'))
        version = getattr(module, '__version__', 'N/A')
        if expected in str(version):
            print(f'  ✓ {pkg}: {version}')
        else:
            print(f'  ⚠ {pkg}: {version} (expected: {expected})')
    except ImportError as e:
        print(f'  ✗ {pkg}: NOT INSTALLED - {e}')
"

echo.
echo Step 10: Starting Endee database...
echo Checking if Docker is installed...
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed or not running.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
) else (
    echo Starting Endee vector database...
    if exist docker-compose.endee.yml (
        docker-compose -f docker-compose.endee.yml up -d
        timeout /t 5 /nobreak >nul
        echo Checking Endee status...
        python -c "
import requests
try:
    response = requests.get('http://localhost:8080/api/v1/health', timeout=5)
    if response.status_code == 200:
        print('  ✓ Endee is running on http://localhost:8080')
    else:
        print('  ⚠ Endee returned status:', response.status_code)
except Exception as e:
    print('  ⚠ Could not connect to Endee:', str(e))
print('  To start manually: docker-compose -f docker-compose.endee.yml up -d')
        "
    ) else (
        echo Creating Endee docker-compose file...
        (
echo version: '3.8'
echo.
echo services:
echo   endee-server:
echo     image: endeeio/endee-server:latest
echo     container_name: endee-legal
echo     ports:
echo       - "8080:8080"
echo     environment:
echo       NDD_DATA_DIR: /data
echo       NDD_NUM_THREADS: 0
echo     volumes:
echo       - endee-data:/data
echo     restart: unless-stopped
echo     ulimits:
echo       nofile:
echo         soft: 100000
echo         hard: 100000
echo.
echo volumes:
echo   endee-data:
        ) > docker-compose.endee.yml
        echo Created docker-compose.endee.yml
        echo To start Endee: docker-compose -f docker-compose.endee.yml up -d
    )
)

echo.
echo Step 11: Creating sample documents...
if not exist sample_docs (
    mkdir sample_docs
)

if not exist sample_docs\contract_agreement.txt (
    (
echo AGREEMENT FOR SERVICES
echo.
echo This Agreement is made on [Date] between [Company Name] and [Service Provider].
echo.
echo 1. TERM: This Agreement shall commence on [Start Date] and continue for [Duration].
echo.
echo 2. SERVICES: The Service Provider shall provide the following services: [Description].
echo.
echo 3. COMPENSATION: The Company shall pay the Service Provider [Amount] for services rendered.
echo.
echo 4. TERMINATION: Either party may terminate this Agreement with [Notice Period] written notice.
echo.
echo 5. GOVERNING LAW: This Agreement shall be governed by the laws of [State/Country].
echo.
echo This document constitutes a legally binding contract between the parties.
    ) > sample_docs\contract_agreement.txt
    echo Created: sample_docs\contract_agreement.txt
)

if not exist sample_docs\negligence_case.txt (
    (
echo IN THE SUPREME COURT OF [STATE]
echo.
echo Case No: SC-2023-001
echo Plaintiff: John Doe
echo Defendant: ABC Corporation
echo.
echo JUDGMENT ON NEGLIGENCE
echo.
echo The Court finds that to establish negligence, a plaintiff must prove:
echo 1. The defendant owed a duty of care to the plaintiff
echo 2. The defendant breached that duty
echo 3. The breach caused harm to the plaintiff
echo 4. The plaintiff suffered damages as a result
echo.
echo In this case, the defendant corporation failed to maintain safe premises,
echo which constituted a breach of duty. The plaintiff suffered injuries as a direct result.
echo.
echo The elements of negligence are well-established in common law and have been
echo consistently applied in jurisdictions following the English legal tradition.
echo.
echo AWARD: The Court awards damages in the amount of $500,000 to the plaintiff.
    ) > sample_docs\negligence_case.txt
    echo Created: sample_docs\negligence_case.txt
)

echo.
echo Step 12: Creating configuration files...
if not exist app\config.py (
    (
echo from pydantic_settings import BaseSettings
echo from typing import Optional
echo.
echo class Settings(BaseSettings):
echo     # Endee Configuration
echo     ENDEE_HOST: str = "localhost"
echo     ENDEE_PORT: int = 8080
echo     ENDEE_TOKEN: Optional[str] = None
echo.
echo     # OpenAI Configuration
echo     OPENAI_API_KEY: Optional[str] = None
echo     OPENAI_MODEL: str = "gpt-3.5-turbo"
echo.
echo     # Application Configuration
echo     APP_NAME: str = "Legal AI Assistant"
echo     DEBUG: bool = False
echo     INDEX_NAME: str = "legal_documents"
echo     EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
echo.
echo     # CORS Configuration
echo     CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
echo.
echo     class Config:
echo         env_file = ".env"
echo.
echo settings = Settings()
    ) > app\config.py
    echo Created: app\config.py
)

if not exist .env.example (
    (
echo # Endee Configuration
echo ENDEE_HOST=localhost
echo ENDEE_PORT=8080
echo ENDEE_TOKEN=
echo.
echo # OpenAI Configuration
echo OPENAI_API_KEY=your_openai_api_key_here
echo.
echo # Application Configuration
echo APP_NAME=Legal AI Assistant
echo DEBUG=True
echo INDEX_NAME=legal_documents
echo EMBEDDING_MODEL=all-MiniLM-L6-v2
    ) > .env.example
    echo Created: .env.example
)

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo What to do next:
echo.
echo 1. Copy .env.example to .env and add your OpenAI API key:
echo    copy .env.example .env
echo    REM Then edit .env and add: OPENAI_API_KEY=your_key_here
echo.
echo 2. Start Endee vector database (if not running):
echo    docker-compose -f docker-compose.endee.yml up -d
echo.
echo 3. Create ingestion script and run it:
echo    See instructions for creating scripts\ingest_sample.py
echo.
echo 4. Start the API server:
echo    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 5. Open API documentation:
echo    http://localhost:8000/docs
echo.
echo Project structure created:
echo   - app\                    (FastAPI application)
echo   - sample_docs\           (Sample legal documents)
echo   - scripts\               (Utility scripts)
echo   - requirements.txt       (All dependencies)
echo   - docker-compose.endee.yml (Endee configuration)
echo.
echo Virtual environment: venv (activated)
echo Python version: 3.12.x
echo.
pause
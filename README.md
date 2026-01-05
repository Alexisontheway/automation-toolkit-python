# automation-toolkit-python
A Python-based automation toolkit for file management, data cleaning, email automation, and AI-assisted utilities.

## 🔄 Workflow

1. User provides a directory path via command-line arguments  
2. The system validates the path and initializes logging  
3. Each file is scanned and hashed using SHA-256  
4. Duplicate files are detected using content-based hashing  
5. Files are organized into folders based on extension  
6. Actions are either executed or simulated using dry-run mode  
7. All operations are logged with severity levels

## ▶️ Usage

### Dry-run mode (safe simulation)
```bash
python organizer.py C:\path\to\folder --dry-run

python organizer.py C:\path\to\folder

INFO | [DRY-RUN] Would move report.pdf → pdf/
WARNING | Duplicate detected: report_copy.pdf (duplicate of report.pdf)

## 🧩 Project Phases

- **Phase 1:** File organization by extension  
- **Phase 2:** Dry-run safety mode  
- **Phase 3:** Hash-based duplicate detection (SHA-256)  
- **Phase 4:** CLI support and structured logging  

Each phase was implemented incrementally to reflect real-world software development practices.


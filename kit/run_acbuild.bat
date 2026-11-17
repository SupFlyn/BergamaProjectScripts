@echo off
rem AcBuild standalone (v1.48+): only Archicad 30 with Tapir open; close Rhino first.
rem Starts the newest scripts\bergama_acbuild_v*.py in windowless Python (pyw) and returns at once: no console window.
rem Live progress: logs\bergama_acbuild_progress.txt   Full log at the end: logs\bergama_acbuild_site_log.txt
cd /d "%~dp0"
start "" pyw -3.13 -c "import glob,re,runpy,os; f=max(glob.glob('scripts/bergama_acbuild_v*.py'), key=lambda p: [int(x) for x in re.findall(r'\d+', os.path.basename(p))]); runpy.run_path(f, run_name='__main__')"

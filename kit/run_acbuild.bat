@echo off
rem AcBuild standalone (v1.48+): only Archicad 30 with Tapir open; close Rhino first.
rem Starts scripts\bergama_run_acbuild.py in windowless Python (pyw) and returns at once: no console window.
rem It runs the newest scripts\bergama_acbuild_v*.py; only on an ERROR a window comes to the front (bold red + log folder).
rem Live progress: logs\bergama_acbuild_progress.txt   Full log at the end: logs\bergama_acbuild_site_log.txt
cd /d "%~dp0"
start "" pyw -3.13 "scripts\bergama_run_acbuild.py"

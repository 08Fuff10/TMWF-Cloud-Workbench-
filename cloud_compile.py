"""TMWF Cloud Workbench bootstrap: local-only compiler runner (Python 3.10+)."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

ERROR = re.compile(r'\b(?:SCRIPT|ENGINE|RESOURCE|INIT)\s*\(E\)|\bscript validation failed\b|\b(?:cannot|can.t|failed to) compile\b|\bfatal error\b', re.I)
SUCCESS = re.compile(r'\bscript validation (?:successful|succeeded|passed|finished successfully)\b|\bscripts? (?:successfully compiled|compiled successfully)\b', re.I)

def command(exe, project, profile, config, warp):
    args = [str(exe), '-gproj', str(project), '-profile', str(profile), '-wbSilent', '-wbModule=ScriptEditor', '-validate', config, '-noThrow']
    if warp:
        args.append('-enableWARP')
    return args

def assess(code, logs, timed_out=False):
    errors = [line for line in logs.splitlines() if ERROR.search(line)]
    if timed_out: status = 'timeout'
    elif code is None: status = 'launch_error'
    elif code in (-1, 4294967295): status = 'validation_failed_or_engine_error'
    elif code != 0: status = 'process_error'
    elif errors: status = 'errors_in_log'
    elif not SUCCESS.search(logs): status = 'unconfirmed'
    else: status = 'validation_reported_success'
    return status, errors

def read_log(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig', errors='replace')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe', required=True, type=Path)
    p.add_argument('--project', required=True, type=Path)
    p.add_argument('--game', required=True, type=Path, help='Arma Reforger installation directory (working directory)')
    p.add_argument('--output', type=Path, default=Path('runs'))
    p.add_argument('--config', default='ALL', choices=['ALL','PC','XBOX_SERIES','PS5','HEADLESS'])
    p.add_argument('--warp', action='store_true')
    p.add_argument('--timeout', type=int, default=600)
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    exe, project, game = (x.resolve() for x in (a.exe,a.project,a.game))
    run = a.output.resolve() / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
    args = command(exe, project, run/'profile-root', a.config, a.warp)
    if a.dry_run:
        print(json.dumps({'argv':args,'cwd':str(game)}, indent=2)); return 0
    if os.name != 'nt': p.error('Original Workbench requires a Windows host for this runner.')
    if not exe.is_file() or exe.suffix.lower() != '.exe': p.error('Workbench executable not found')
    if not project.is_file() or project.suffix.lower() != '.gproj': p.error('Project .gproj not found')
    if not game.is_dir(): p.error('Game directory not found')
    if a.timeout <= 0: p.error('Timeout must be positive')
    run.mkdir(parents=True)
    (run/'profile-root').mkdir()
    code = None; timeout = False; launch_error = None
    with (run/'stdout-stderr.log').open('wb') as stream:
        try:
            proc = subprocess.run(args,cwd=game,stdout=stream,stderr=subprocess.STDOUT,timeout=a.timeout,check=False)
            code = proc.returncode
        except subprocess.TimeoutExpired: timeout = True
        except OSError as exc: launch_error = str(exc)
    paths = sorted(run.rglob('*.log'))
    logs = '\n'.join(read_log(x) for x in paths)
    status, errors = assess(code, logs, timeout)
    report = {'status':status,'exit_code':code,'timed_out':timeout,'launch_error':launch_error,'project':str(project),'argv':args,'cwd':str(game),'log_files':[str(x.relative_to(run)) for x in paths], 'error_lines':errors[:200], 'error_line_count':len(errors), 'note':'Success text detection is heuristic until verified against installed Workbench. A negative-control test is required.'}
    (run/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=True)); print('Report:',run/'report.json')
    return 0 if status == 'validation_reported_success' else 1

if __name__ == '__main__': sys.exit(main())

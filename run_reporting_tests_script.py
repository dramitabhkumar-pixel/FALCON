import subprocess
from pathlib import Path

repo = Path(__file__).resolve().parent
test_file = repo / 'tests' / 'test_backtest_reporting.py'
output_file = repo / 'run_reporting_tests_output.txt'

result = subprocess.run(
    [
        'python',
        '-c',
        'import pytest, sys; sys.exit(pytest.main(["-q", r"' + str(test_file) + '"]))',
    ],
    cwd=repo,
    capture_output=True,
    text=True,
)

with output_file.open('w', encoding='utf-8') as f:
    f.write(f'EXIT_CODE: {result.returncode}\n')
    f.write('STDOUT:\n')
    f.write(result.stdout)
    f.write('\nSTDERR:\n')
    f.write(result.stderr)

print('Wrote', output_file)

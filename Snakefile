import socket

# load java module if on scc
if 'scc' in socket.gethostname():
    shell.prefix('module load java; set -eua pipefail; ')
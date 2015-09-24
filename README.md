# archutils
Misc utilities for Arch Linux

This is a collection of various utilities I've written to perform Arch Linux systems.

Most of these scripts started as quick fixes to specific problems I had, and may not be particularly well tested or designed.  Feel free to send me a pull request with any improvements.

tracepackages.py
----------------

Sometimes, something is broken on your Arch system.  It isn't obvious why, but you suspect that you might have a package (often from aur) that is causing the breakage.  This script gives you a brute force method for determining which packages could possibly by the problem.

tracepackage.py reads strace output, looks for all of the files opened by the program, and runs pacman -Qqo to find which (if any) packages own them.  The output is a list of packages that have files which were accessed in any way by the target program.

1.  Trace the system calls performed by the target program:
% strace -f -o <trace file> <command>

2.  Parse the trace file and generate a list of packages owning the files
used by the target program:
% ./tracepackages.py <trace file> <packages.txt>

3.  Browse the resulting list of packages which have files accessed by the target program.

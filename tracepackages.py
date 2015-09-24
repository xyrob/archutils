#!/usr/bin/python
import sys
import re
import subprocess

def printHelp():
    print("Usage: tracepackages.py <file from strace -f -o file> <output file>")

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        printHelp()

    else:
        # Load trace
        tracefile = sys.argv[1]
        print("Loading trace from: " + tracefile)
        tf = open(tracefile)

        # TODO: This will fail if there is a quote in a filename
        matchexp = re.compile("^[0-9]+  open\(\"(/[^\"' ]*)\"")

        files = set()

        print("Stage 1: Compiling file list.")
        
        try:
            for line in tf:
                match = matchexp.match(line)
                if match:
                    f = match.groups()[0]
                    print("File: " + f)
                    files.add(f)
        except:
            pass



        pkgs = set()
        orphanfiles = set()

        print("Stage 2: Checking package ownership.")

        for file in files:
            try:
                print("Checking " + file)
                out = subprocess.check_output(["pacman", "-Qqo", file]).decode("utf-8").strip().split("\n")
                for line in out:
                    print("Found package: " + str(line))
                    pkgs.add(line)
            except subprocess.CalledProcessError as e:
                orphanfiles.add(file)

        print("The following paths were not owned by any packages:")
        for orphan in orphanfiles:
            print(orphan)

        print("Stage 3: Writing package list:")

        outf = open(sys.argv[2], "w")

        for pkg in pkgs:
            print("PKG: " + pkg)
            outf.write(pkg + "\n")

        outf.close()

        tf.close()

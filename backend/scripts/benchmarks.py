#!/usr/bin/env python

import subprocess


# ?run_ab
def run_ab(url: str):
    # http://127.0.0.1:8000/pets/
    # Run the ab command with the specified parameters and capture the output
    process = subprocess.Popen(
        ["./ab.exe", "-c 10", "-n 20", f"{url}"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    # Wait for the process to finish and get the output
    output, _ = process.communicate()

    # Print the output
    print("AB result is ", output)


run_ab("http://127.0.0.1:8000/pets/")

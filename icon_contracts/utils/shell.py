import subprocess


def run_command(command):
    # run command (can be an array (for parameters))
    p = subprocess.Popen(command, shell=True, \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # capture output and error
    (output, err) = p.communicate()
    # wait for command to end
    # TODO: really long running?
    status = p.wait()

    # decode output from byte string
    if output is not None:
        output = output.decode('utf-8')
    if err is not None:
        err = err.decode('utf-8')
    # return stdout, stderr, status code
    return (output, err, status)

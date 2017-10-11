import subprocess
import sys
import tempfile
import time


def _get_text(buffer, callback, last_place, break_lines):
    text = buffer.read()
    if text:
        decoded = text.decode(sys.stdout.encoding)
        if break_lines:
            for line in decoded.split("\n"):
                if line != "":
                    callback(line)
        else:
            callback(decoded)
        last_place = buffer.tell()
    else:
        buffer.seek(last_place)
    return text, last_place


def run(cmd, output_callback, error_callback,
        reaction_time=("Mo Farah's reaction time: ", 0.155)[1],
        break_lines=True):

    # Create temporary files for stdout and stderr to write to. These
    # need to be *real* files, otherwise the "fileno" attribute won't be
    # found: that's why io.TextStream and similar don't work.
    with tempfile.TemporaryFile() as output_buffer, \
            tempfile.TemporaryFile() as error_buffer:

        # Start up the process, writing to our two temporary files.
        # N.B. the shell=True argument is used; hopefully we trust our input!
        process = subprocess.Popen(cmd, stdout=output_buffer,
                                   stderr=error_buffer, shell=True)

        return_value = None
        stdout_last_place = 0
        stderr_last_place = 0

        while return_value is None:
            # Check for the process having completed.
            return_value = process.poll()
            if return_value:
                break

            # Read and handle any output to stdout or stderr.
            stdout_text, stdout_last_place = _get_text(
                output_buffer, output_callback, stdout_last_place, break_lines)
            stderr_text, stderr_last_place = _get_text(
                error_buffer, error_callback, stderr_last_place, break_lines)

            # Try not to thrash the CPU too hard.
            if not stdout_text or stderr_text:
                time.sleep(reaction_time)

        # Handle any outstanding output on the buffers.
        time.sleep(reaction_time)
        stdout_text, _ = _get_text(
            output_buffer, output_callback, stdout_last_place, break_lines)
        stderr_text, _ = _get_text(
            error_buffer, error_callback, stderr_last_place, break_lines)

    return return_value


__all__ = ["run"]

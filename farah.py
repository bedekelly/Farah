import subprocess
import sys
import tempfile
import time


def get_text(buffer, callback, last_place, break_lines):
    text = buffer.read()
    if text:
        decoded = text.decode(sys.stdout.encoding)
        if break_lines:
            for line in filter(lambda check_line: check_line != "", decoded.split("\n")):
                callback(line)
        else:
            callback(decoded)
        last_place = buffer.tell()
    else:
        buffer.seek(last_place)
    return text, last_place


def run(cmd, output_callback, error_callback, reaction_time=0.25, break_lines=True):
    with tempfile.TemporaryFile() as output_buffer, tempfile.TemporaryFile() as error_buffer:
        process = subprocess.Popen(cmd, stdout=output_buffer, stderr=error_buffer)

        return_value = None
        stdout_last_place = 0
        stderr_last_place = 0

        while return_value is None:
            return_value = process.poll()

            # Read and handle any stdout messages.
            stdout_text, stdout_last_place = get_text(output_buffer, output_callback, stdout_last_place, break_lines)
            stderr_text, stderr_last_place = get_text(error_buffer, error_callback, stderr_last_place, break_lines)

            # Try not to thrash the CPU too hard.
            if not stdout_text or stderr_text:
                time.sleep(reaction_time)

        # Handle any outstanding output on the buffers.
        time.sleep(reaction_time)
        stdout_text, _ = get_text(output_buffer, output_callback, stdout_last_place, break_lines)
        stderr_text, _ = get_text(error_buffer, error_callback, stderr_last_place, break_lines)

    return return_value

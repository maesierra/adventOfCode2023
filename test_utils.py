
import contextlib
import os
import tempfile
import uuid

@contextlib.contextmanager
def text_to_input(text): 
    with tempfile.TemporaryDirectory() as td:
        f_name = os.path.join(td, str(uuid.uuid4()))
        with open(f_name, 'w') as fh:
            fh.write(text)
        yield f_name
    
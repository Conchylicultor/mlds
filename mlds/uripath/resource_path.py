"""."""

import importlib.resources
import types


class ResourcePath:

  def __init__(self, package: importlib.resources.Package):
    pass


tfds.get_resource()

resource = ResourcePath(tfds)
c = resource / 'data' / 'checksums.txt'
c.is_resource()  # ?? Or use is_file instead!
c.read_text()
c.read_bytes()

resource = ResourcePath(module)
resource = ResourcePath()

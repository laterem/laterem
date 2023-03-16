from django.conf import settings
from django.core.files.storage import Storage
from django.core.files import File
from context_objects import DTM_SCANNER
from os.path import join as pathjoin

class AssetStorage(Storage):
    def _open(self, name: str, mode="rb"):
        if name.startswith('asset.') and name.count('.') >= 2:
            name = name.lstrip('asset.')
            sep = name.find('.')
            source = name[:sep]
            body = name[sep:]
            path = DTM_SCANNER.id_to_path(source)
            dtcpath = pathjoin(path, 'assets', body)
            return File(open(dtcpath, mode))
        return None
    
    def _save(self, name: str, mode="rb"):
        return NotImplemented
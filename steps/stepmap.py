from .collectionstep import CollectionStep
from .executestep import ExecuteStep
from .downloadstep import DownloadStep
from .unpackstep import UnpackStep

stepmap = {'collection': CollectionStep.fromjson,
           'execute': ExecuteStep.fromjson,
           'download': DownloadStep.fromjson,
           'unpack': UnpackStep.fromjson}

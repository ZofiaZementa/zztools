from .collectionstep import CollectionStep
from .executestep import ExecuteStep
from .downloadstep import DownloadStep
from .unpackstep import UnpackStep
from .gitstep import GitStep
from .liststep import ListStep
from .makestep import MakeStep

stepmap = {'collection': CollectionStep.fromjson,
           'execute': ExecuteStep.fromjson,
           'download': DownloadStep.fromjson,
           'unpack': UnpackStep.fromjson,
           'git': GitStep.fromjson,
           'list': ListStep.fromjson,
           'make': MakeStep.fromjson}

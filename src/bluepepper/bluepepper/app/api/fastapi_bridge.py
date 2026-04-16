from qtpy.QtCore import QObject, Signal


class FastapiBridge(QObject):
    payload = Signal(dict)


# Global communicator instance
fastapi_bridge = FastapiBridge()

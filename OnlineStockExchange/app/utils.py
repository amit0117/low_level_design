from threading import Lock


class SingletonMeta(type):
    _instance_dict: dict[type, object] = dict()
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance_dict:
            with cls._lock:
                if cls not in cls._instance_dict:
                    instance = super().__call__(*args, **kwargs)
                    cls._instance_dict[cls] = instance
        return cls._instance_dict[cls]

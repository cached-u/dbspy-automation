# Loads config.yaml, environment vars

# utils/config.py

import yaml
import os

class Config:
    """
    Loads and caches the contents of config.yaml.
    """
    _data = None

    @classmethod
    def load(cls):
        if cls._data is None:
            cfg_path = os.path.join(os.path.dirname(__file__), os.pardir, "config.yaml")
            cfg_path = os.path.abspath(cfg_path)
            with open(cfg_path, "r", encoding="utf-8") as f:
                cls._data = yaml.safe_load(f)
        return cls._data

    @classmethod
    def get_database_config(cls, db_name: str) -> dict:
        """
        Return the dictionary of settings for a given database name 
        (e.g. "PostgreSQL", "MySQL", "SQLServer").
        """
        data = cls.load()
        return data.get("databases", {}).get(db_name, {})

    @classmethod
    def get_global(cls, key: str, default=None):
        data = cls.load()
        return data.get("global", {}).get(key, default)
    
    @classmethod
    def get_driver_map(cls) -> dict:
        data = cls.load()
        return data.get("driver_maps", {}).get("odbc", {})

    @classmethod
    def get_jdbc_subprotocol_map(cls) -> dict:
        data = cls.load()
        return data.get("driver_maps", {}).get("jdbc_subprotocol", {})

    @classmethod
    def get_ado_provider_map(cls) -> dict:
        data = cls.load()
        return data.get("driver_maps", {}).get("ado_provider", {})
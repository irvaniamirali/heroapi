from fastapi import FastAPI
from typing import Any


class routers:
    def __init__(self, app: FastAPI, routes: list):
        self.app = app
        self.routes = routes

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self._create_route_methods()
        return self

    def _create_route_methods(self):
          for route in self.routes:
              module_path, route_name = route.rsplit('.', maxsplit=1)
              module = __import__(module_path, fromlist=[route_name])
              route_module = getattr(module, route_name)
              route_method_name = f"{route_name.title().replace("_", "")}Route"

              def route_method():
                  return self.app.include_router(route_module)

              setattr(self, route_method_name, route_method)
              getattr(self, route_method_name)()

class Router:
    def __init__(self, base_url):
        self.base_url = base_url
        self.routes = []

    def register(self, flask_app):
        for r in self.routes:
            url = self.base_url + r["url"]
            endpoint = url + "".join(r["methods"])
            flask_app.add_url_rule(
                url,
                endpoint=endpoint,
                view_func=r["callback"],
                provide_automatic_options=True,
                methods=r["methods"],
            )

    def route(self, url, callback, methods=["GET"]):
        self.routes.append({"url": url, "callback": callback, "methods": methods})

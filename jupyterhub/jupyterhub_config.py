c = get_config()  # noqa: F821

c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.hub_ip = "0.0.0.0"

c.Authenticator.admin_users = {"admin"}
c.Authenticator.allowed_users = {"admin"}

c.DummyAuthenticator.password = "admin"
c.JupyterHub.authenticator_class = "dummy"

c.Spawner.default_url = "/lab"

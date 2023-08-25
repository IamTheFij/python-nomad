import os

import pytest

# internal ip of docker
IP = os.environ.get("NOMAD_IP", "192.168.33.10")

# use vagrant PORT if env variable is not specified, generally for local
# testing
NOMAD_PORT = os.environ.get("NOMAD_PORT", 4646)

# Security token
NOMAD_TOKEN = os.environ.get("NOMAD_TOKEN", None)

# Test namespace
NOMAD_NAMESPACE = "admin"

# Nomad min version mark
def nomad_min_version_skip(major: int, minor: int, patch: int):
    return pytest.mark.skipif(
        tuple(int(i) for i in os.environ["NOMAD_VERSION"].split("."))
        < (major, minor, patch),
        reason="Not supported in version",
    )

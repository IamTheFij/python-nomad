from collections.abc import Generator
from typing import Any
from typing import Dict

import pytest

from nomad import Nomad
from tests.common import nomad_min_version_skip
from tests.test_service import JOB_ID, SERVICE_NAME, service_job

# Nomad doesn't have any services by default

# Skip module if not running nomad 1.3.0+
pytestmark = nomad_min_version_skip(1, 3, 0)


class TestServices:

    def test_get_services(self, nomad_setup: Nomad, service_job):
        service_namespaces = nomad_setup.services.get_services()

        assert len(service_namespaces) == 1

        services = service_namespaces[0]["Services"]

        assert len(services) == 1
        assert services[0]["JobID"] == JOB_ID
        assert services[0]["ID"]

    def test_services_overrides(self, nomad_setup: Nomad, service_job):
        # __len__
        assert len(nomad_setup.services)
        # __getitem__
        assert nomad_setup.services[SERVICE_NAME]
        # __contains__
        assert SERVICE_NAME in nomad_setup.services
        # __iter__
        for service in nomad_setup.services:
            assert service
            break
        else:
            raise AssertionError("Expected at least one service to iterate over")

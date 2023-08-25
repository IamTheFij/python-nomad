from collections.abc import Generator
from typing import Any
from typing import Dict

import pytest

from nomad import Nomad
from tests.common import nomad_min_version_skip

# Nomad doesn't have any services by default

# Skip module if not running nomad 1.3.0+
pytestmark = nomad_min_version_skip(1, 3, 0)


JOB_ID = "test_service"
SERVICE_NAME = "test_service"


@pytest.fixture
def service_job(nomad_setup: Nomad) -> Generator[Dict[str, Any], None, None]:
    job = nomad_setup.jobs.register_job(
        {
            "Job": {
                "ID": JOB_ID,
                "TaskGroups": [
                    {
                        "Name": "test_service",
                        "Networks": [
                            {
                                "DynamicPorts": [
                                    {
                                        "Label": "http",
                                        "To": 80,
                                    },
                                ],
                            },
                        ],
                        "Services": [
                            {
                                "Name": SERVICE_NAME,
                                "Provider": "nomad",
                                "PortLabel": "http",
                            },
                        ],
                        "Tasks": [
                            {
                                "Config": {
                                    "image": "containous/whoami:latest",
                                    "ports": ["http"],
                                },
                                "Driver": "docker",
                                "Name": "main",
                            },
                        ],
                    },
                ],
            }
        }
    )

    yield job

    # Clean up job
    if job in nomad_setup.job:
        nomad_setup.job.deregister_job(job["ID"], purge=True)


class TestService:

    def test_get_service(self, nomad_setup: Nomad, service_job):
        service = nomad_setup.service.get_service(SERVICE_NAME)
        assert len(service) == 1
        assert service[0]["JobID"] == JOB_ID
        assert service[0]["ID"]

    def test_get_service_not_found(self, nomad_setup: Nomad):
        nomad_setup.service.get_service(SERVICE_NAME)

    def test_delete_service(self, nomad_setup: Nomad, service_job):
        service = nomad_setup.service.get_service(SERVICE_NAME)
        service_id = service[0]["ID"]
        nomad_setup.service.delete_service(SERVICE_NAME, service_id)

        assert SERVICE_NAME not in nomad_setup.service

    def test_delete_service_not_found(self, nomad_setup: Nomad):
        nomad_setup.service.delete_service(SERVICE_NAME, "foo")

    def test_service_overrides(self, nomad_setup: Nomad, service_job):
        # __getitem__
        assert nomad_setup.service[SERVICE_NAME]
        # __contains__
        assert SERVICE_NAME in nomad_setup.service
        # __delitem__
        del nomad_setup.service[SERVICE_NAME]
        assert SERVICE_NAME not in nomad_setup.service


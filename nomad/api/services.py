"""Nomad Services API: https://developer.hashicorp.com/nomad/api-docs/services"""
from collections.abc import Iterator
from typing import Any, Dict, List
from nomad.api.base import Requester


class Services(Requester):
    """
    The /services endpoints are used to query for and interact with services.
    https://developer.hashicorp.com/nomad/api-docs/services
    """

    ENDPOINT = "services"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"{self.__dict__}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __getattr__(self, item: str):
        msg = f"{item} does not exist"
        raise AttributeError(msg)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        services = self.get_services()

        for namespace in services:
            for service in namespace["Services"]:
                yield service

    def __contains__(self, item: str):
        try:
            _ = self[item]
        except KeyError:
            return False

        return True

    def __getitem__(self, item: str):
        for service in self:
            if service["ServiceName"] == item:
                return service

        raise KeyError

    def __len__(self) -> int:
        return len(list(self))

    def get_services(self, namespace=None) -> List[Dict[str, Any]]:
        """
        This endpoint lists all the currently available Nomad services.
        https://developer.hashicorp.com/nomad/api-docs/services

        optional_arguments:
          - namespace :(str) optional, Specifies the target namespace.
            Specifying * will return all services across all the authorized namespaces.
        returns: list of namespace dicts containing `Services` attributes
        raises:
          - nomad.api.exceptions.BaseNomadException
          - nomad.api.exceptions.URLNotFoundNomadException
        """
        params = {}
        if namespace:
            params["namespace"] = namespace

        return self.request(params=params, method="get").json()

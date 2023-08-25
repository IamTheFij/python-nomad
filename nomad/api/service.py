"""Nomad service: https://developer.hashicorp.com/nomad/api-docs/service"""
from typing import Optional
from typing import Tuple

import nomad.api.exceptions
from nomad.api.base import Requester


class Service(Requester):
    """
    The service endpoint is used for read and delete of a single
    service.

    By default, the agent's local region is used.
    """

    ENDPOINT = "service"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"{self.__dict__}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __getattr__(self, item: str):
        msg = f"{item} does not exist"
        raise AttributeError(msg)

    def __contains__(self, item: str):
        try:
            _ = self[item]
            return True
        except KeyError:
            return False

    def __getitem__(self, item: str):
        try:
            return self.get_service(item)
        except nomad.api.exceptions.URLNotFoundNomadException as exc:
            raise KeyError from exc
    
    def __delitem__(self, item: str):
        """Delete all instance of the specified registered service"""
        service = self[item]
        for service_instance in service:
            self.delete_service(service_instance["ServiceName"], service_instance["ID"])

    def get_service(
        self,
        name: str,
        namespace: Optional[str] = None,
        filter: Optional[str] = None,
        choose: Optional[Tuple[int, str]] = None,
    ):
        """Query for a single service

        https://developer.hashicorp.com/nomad/api-docs/services

        arguments:
          - name :(str) specifies the name of the service to look for. This is specified as part
                    of the path.
          - namespace :(str) optional, specifies the target namespace. Specifying * would return
                    any service.
                    This is specified as a querystring parameter.
          - filter: (str) optional, specifies the expression used to filter the results.
          - choose: (Tuple[int, str]) optional, Spcifies the number of services to return and a
                    hash key. Nomad uses rendevous hashing to deliver consistent results for a
                    given key, and stable results when the number of services changes.
        returns: dict
        raises:
          - nomad.api.exceptions.BaseNomadException
          - nomad.api.exceptions.URLNotFoundNomadException
        """
        params = {}

        if namespace:
            params["namespace"] = namespace
        if filter:
            params["filter"] = filter
        if choose:
            params["choose"] = f"{choose[0]}|{choose[1]}"

        return self.request(name, method="get", params=params).json()

    def delete_service(
        self,
        name: str,
        service_id: str,
    ):
        """This endpoint is used to delete an individual service registration

        https://developer.hashicorp.com/nomad/api-docs/services

        arguments:
            - name (str) service name
            - service_id (str) service id for particular registration

        returns: dict
        raises:
            - nomad.api.exceptions.BaseNomadException
            - nomad.api.exceptions.URLNotFoundNomadException
        """
        return self.request(name, service_id, method="delete").json()

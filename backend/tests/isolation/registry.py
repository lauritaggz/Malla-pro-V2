"""Central registry of private routes (T-004). Add every new private route here.

- PRIVATE_RESOURCES: data owned by a user. For each one, `assert_isolated` checks that another
  user gets 404 when reading, modifying or deleting it (id in the URL and in the body).
- SELF_SCOPED_ROUTES: routes that only act on the caller and take no resource id (e.g. /me).

`test_isolation.py` fails if a route depends on `get_current_user` and is in neither list.
"""

from tests.isolation.framework import PrivateResource, RouteKey

PRIVATE_RESOURCES: list[PrivateResource] = [
    # Empty until the first user-owned resource exists (T-020 academic profiles onwards).
    # Example for a future route set:
    # PrivateResource(
    #     name="academic profile",
    #     create=create_profile,  # POST /api/v1/me/profiles as the owner, returns the id
    #     read=Op("GET", "/api/v1/me/profiles/{id}"),
    #     attempts=(
    #         Op("GET", "/api/v1/me/profiles/{id}"),
    #         Op("PATCH", "/api/v1/me/profiles/{id}", json={"version": 1, "entry_year": 2020}),
    #         Op("DELETE", "/api/v1/me/profiles/{id}"),
    #         Op("POST", "/api/v1/me/attempts", json={"profile_id": "{id}", ...}),
    #     ),
    #     create_routes=(("POST", "/api/v1/me/profiles"),),
    # ),
]

SELF_SCOPED_ROUTES: set[RouteKey] = {
    ("GET", "/api/v1/me"),
}

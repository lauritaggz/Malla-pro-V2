"""Central registry of private routes (T-004). Add every new private route here.

- PRIVATE_RESOURCES: data owned by a user. For each one, `assert_isolated` checks that another
  user gets 404 when reading, modifying or deleting it (id in the URL and in the body), and that
  each of those requests works for the owner (control).
- SELF_SCOPED_ROUTES: routes that only act on the caller and take no resource id (e.g. /me).
- TEAM_ROUTES: team routes (T-002) with the roles they allow. Tests check that the route really
  uses `require_role` with exactly those roles and that a student gets 403.

`test_isolation.py` fails if a route depends on `get_current_user` and is in none of them.
"""

from app.models.user import ROLE_SUPERADMIN
from tests.isolation.framework import PrivateResource, RouteKey

PRIVATE_RESOURCES: list[PrivateResource] = [
    # Empty until the first user-owned resource exists (T-020 academic profiles onwards).
    # Example for a future route set:
    # PrivateResource(
    #     name="academic profile",
    #     create=create_profile,  # POST /api/v1/me/profiles as the owner, returns the id
    #     read=Op("GET", "/api/v1/me/profiles/{profile_id}"),  # route as FastAPI declares it
    #     attempts=(
    #         Op("GET", "/api/v1/me/profiles/{profile_id}"),
    #         Op("PATCH", "/api/v1/me/profiles/{profile_id}", json={"version": 1}),
    #         Op("DELETE", "/api/v1/me/profiles/{profile_id}"),
    #         Op("POST", "/api/v1/me/attempts", json={"profile_id": "{id}", ...}),
    #     ),
    #     create_routes=(("POST", "/api/v1/me/profiles"),),
    # ),
]

SELF_SCOPED_ROUTES: set[RouteKey] = {
    ("GET", "/api/v1/me"),
}

TEAM_ROUTES: dict[RouteKey, frozenset[str]] = {
    ("PATCH", "/api/v1/admin/users/{user_id}/role"): frozenset({ROLE_SUPERADMIN}),
}

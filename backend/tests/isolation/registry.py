"""Central registry of private routes (T-004). Add every new private route here.

- PRIVATE_RESOURCES: data owned by a user. For each one, `assert_isolated` checks that another
  user gets 404 when reading, modifying or deleting it (id in the URL and in the body), and that
  each of those requests works for the owner (control).
- SELF_SCOPED_ROUTES: routes that only act on the caller and take no resource id (e.g. /me).

`test_isolation.py` fails if a route depends on `get_current_user` and is in neither list.
"""

from httpx import AsyncClient

from tests.isolation.framework import Op, PrivateResource, RouteKey


async def create_malla_draft(owner: AsyncClient) -> str:
    response = await owner.post(
        "/api/v1/me/malla-drafts", content=b"%PDF", headers={"Content-Type": "application/pdf"}
    )
    assert response.status_code == 200, response.text
    return str(response.json()["id"])


PRIVATE_RESOURCES: list[PrivateResource] = [
    # Prototype (spike/ia-mallas): AI drafts kept as a per-user history.
    PrivateResource(
        name="AI malla draft (prototype)",
        create=create_malla_draft,
        read=Op("GET", "/api/v1/me/malla-drafts/{draft_id}"),
        attempts=(
            Op("GET", "/api/v1/me/malla-drafts/{draft_id}"),
            Op("DELETE", "/api/v1/me/malla-drafts/{draft_id}"),
        ),
        create_routes=(("POST", "/api/v1/me/malla-drafts"),),
        fixtures=("ai_drafts",),
    ),
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
    # Prototype: lists only the caller's own drafts (checked in test_malla_drafts_api.py).
    ("GET", "/api/v1/me/malla-drafts"),
}

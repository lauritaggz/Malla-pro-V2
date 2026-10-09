import { describe, expect, it, vi } from "vitest";
import { createApi } from "./api.js";

function makeResponse(status, body = {}) {
  return { status, ok: status >= 200 && status < 300, json: async () => body };
}

function setup(statuses, { withUser = true } = {}) {
  const queue = [...statuses];
  const fetchFn = vi.fn(async () => makeResponse(queue.shift() ?? 200));
  const user = { getIdToken: vi.fn(async (force) => (force ? "fresh-token" : "old-token")) };
  const onUnauthorized = vi.fn();
  const api = createApi({
    getUser: () => (withUser ? user : null),
    onUnauthorized,
    baseUrl: "http://api.test/",
    fetchFn,
  });
  return { api, fetchFn, user, onUnauthorized };
}

const authHeader = (fetchFn, call) => fetchFn.mock.calls[call][1].headers.get("Authorization");

describe("api client", () => {
  it("sends the bearer token and does not refresh on success", async () => {
    const { api, fetchFn, user, onUnauthorized } = setup([200]);
    const res = await api.fetch("/api/v1/me");
    expect(res.status).toBe(200);
    expect(fetchFn).toHaveBeenCalledTimes(1);
    expect(fetchFn.mock.calls[0][0]).toBe("http://api.test/api/v1/me");
    expect(authHeader(fetchFn, 0)).toBe("Bearer old-token");
    expect(user.getIdToken).toHaveBeenCalledWith(false);
    expect(onUnauthorized).not.toHaveBeenCalled();
  });

  it("on 401 refreshes the token and retries once without signing out", async () => {
    const { api, fetchFn, user, onUnauthorized } = setup([401, 200]);
    const res = await api.fetch("/api/v1/me");
    expect(res.status).toBe(200);
    expect(fetchFn).toHaveBeenCalledTimes(2);
    expect(user.getIdToken).toHaveBeenLastCalledWith(true);
    expect(authHeader(fetchFn, 1)).toBe("Bearer fresh-token");
    expect(onUnauthorized).not.toHaveBeenCalled();
  });

  it("signs out only if the retry also returns 401", async () => {
    const { api, fetchFn, onUnauthorized } = setup([401, 401]);
    const res = await api.fetch("/api/v1/me");
    expect(res.status).toBe(401);
    expect(fetchFn).toHaveBeenCalledTimes(2);
    expect(onUnauthorized).toHaveBeenCalledTimes(1);
  });

  it("does not add Authorization or retry when there is no user", async () => {
    const { api, fetchFn, onUnauthorized } = setup([401], { withUser: false });
    const res = await api.fetch("/api/v1/health");
    expect(res.status).toBe(401);
    expect(fetchFn).toHaveBeenCalledTimes(1);
    expect(authHeader(fetchFn, 0)).toBeNull();
    expect(onUnauthorized).not.toHaveBeenCalled();
  });

  it("json() throws ApiError with the backend detail", async () => {
    const fetchFn = vi.fn(async () => makeResponse(403, { detail: "Prohibido" }));
    const api = createApi({ getUser: () => null, fetchFn, baseUrl: "http://api.test" });
    await expect(api.json("/x")).rejects.toMatchObject({ status: 403, message: "Prohibido" });
  });
});

import { strict as assert } from "node:assert";
import { test } from "node:test";
import { getUser, auditRequest, type Request } from "./request.ts";

test("partial fixture preserves id", () => {
  assert.equal(getUser({ body: { id: "u-123" } } as Request), "u-123");
});
test("invalid id is rejected", () => {
  assert.throws(() => getUser({ body: { id: 123 } } as unknown as Request), /id must be string/);
});
test("full request fields are observed", () => {
  assert.equal(auditRequest({ body: { id: "u-123" }, method: "GET", headers: { "x-trace": "trace-7" } }), "GET:trace-7:u-123");
});

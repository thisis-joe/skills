import { strict as assert } from "node:assert";
import { test } from "node:test";
import { fromPartial, fromAny, fromExact } from "@total-typescript/shoehorn";
import { getUser, auditRequest } from "./request.ts";

test("partial fixture preserves id", () => {
  assert.equal(getUser(fromPartial({ body: { id: "u-123" } })), "u-123");
});
test("invalid id is rejected", () => {
  assert.throws(() => getUser(fromAny({ body: { id: 123 } })), /id must be string/);
});
test("full request fields are observed", () => {
  assert.equal(auditRequest(fromExact({ body: { id: "u-123" }, method: "GET", headers: { "x-trace": "trace-7" } })), "GET:trace-7:u-123");
});

export type Request = {
  body: { id: string };
  method: string;
  headers: Record<string, string>;
};
export function getUser(request: Request): string {
  if (typeof request.body.id !== "string") throw new TypeError("id must be string");
  return request.body.id;
}
export function auditRequest(request: Request): string {
  return `${request.method}:${request.headers["x-trace"]}:${request.body.id}`;
}

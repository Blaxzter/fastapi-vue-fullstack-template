# API Error Format (Problem Details)

The API returns errors in RFC 7807 "problem details" style using `application/problem+json`.

## Shape

```json
{
  "type": "urn:problem:project.not_found",
  "code": "project.not_found",
  "title": "Not Found",
  "status": 404,
  "detail": "Project not found",
  "instance": "/api/v1/projects/123",
  "errors": [
    {
      "loc": ["body", "name"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

## Notes

- `type`, `title`, and `status` are always present.
- `type` uses `urn:problem:<code>` for application errors.
- `code` is optional and can be derived from `type` when it follows the `urn:problem:` convention.
- `detail` is a human-readable message.
- `instance` includes the request path.
- `errors` is only present for validation failures (HTTP 422).

## Validation Errors

Validation errors include an `errors` array. Each item has:

- `loc`: location of the invalid field (e.g. `['body', 'name']`)
- `msg`: the validation message
- `type`: the validation error type

## Frontend Handling

Use the shared error normalizer in `frontend/src/lib/api-errors.ts` to map API errors to consistent messages and toast output.

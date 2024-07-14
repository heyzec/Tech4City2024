# FastAPI

> Version 0.1.0

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| POST | [/analyze/](#postanalyze) | Create Photo |
| GET | [/results](#getresults) | Read Photos |
| GET | [/results/{photo_id}](#getresultsphoto_id) | Read Photo |
| DELETE | [/delete](#deletedelete) | Delete All Photos |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| Body_create_photo_analyze__post | [#/components/schemas/Body_create_photo_analyze__post](#componentsschemasbody_create_photo_analyze__post) |  |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |  |
| PhotoResponse | [#/components/schemas/PhotoResponse](#componentsschemasphotoresponse) |  |
| ValidationError | [#/components/schemas/ValidationError](#componentsschemasvalidationerror) |  |

## Path Details

***

### [POST]/analyze/

- Summary  
Create Photo

#### RequestBody

- multipart/form-data

```ts
{
  file: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  id: integer
  input: string
  output: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/results

- Summary  
Read Photos

#### Parameters(Query)

```ts
skip?: integer
```

```ts
limit?: integer //default: 10
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  id: integer
  input: string
  output: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/results/{photo_id}

- Summary  
Read Photo

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  id: integer
  input: string
  output: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [DELETE]/delete

- Summary  
Delete All Photos

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

## References

### #/components/schemas/Body_create_photo_analyze__post

```ts
{
  file: string
}
```

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/PhotoResponse

```ts
{
  id: integer
  input: string
  output: string
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```
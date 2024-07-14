# FastAPI

> Version 0.1.0

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| POST | [/analyze/](#postanalyze) | Create Photo |
| GET | [/results/](#getresults) | Read Photos |
| GET | [/results/{photo_id}](#getresultsphoto_id) | Read Photo |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| AnalyzePostRequest | [#/AnalyzePostRequest](#AnalyzePostRequest) |  |
| HTTPValidationError | [#/HTTPValidationError](#HTTPValidationError) |  |
| PhotoResponse | [#/PhotoResponse](#PhotoResponse) |  |
| ValidationError | [#/ValidationError](#ValidationError) |  |

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
  base64_data: string
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

### [GET]/results/

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
  base64_data: string
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
  base64_data: string
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

## References

### #/AnalyzePostRequest

```ts
{
  file: string
}
```

### #/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/PhotoResponse

```ts
{
  id: integer
  base64_data: string
}
```

### #/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```
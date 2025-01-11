# API Reference for ChatGPT Recipe Toolkit

This document provides detailed information about the API endpoints, request/response formats, and examples of how to use the API.

## Table of Contents

- [Introduction](#introduction)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Rephrase Text](#rephrase-text)
  - [Summarize Text](#summarize-text)
  - [Generate Reply](#generate-reply)
  - [Create Email](#create-email)
- [Request/Response Formats](#requestresponse-formats)
- [Examples](#examples)

## Introduction

The ChatGPT Recipe Toolkit API allows you to perform various text processing tasks such as rephrasing, summarizing, generating replies, and creating emails. This document provides an overview of the available endpoints and how to use them.

## Authentication

To use the API, you need to authenticate with your OpenAI API key. Include the API key in the `Authorization` header of your requests:

```http
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Rephrase Text

**Endpoint**: `/api/rephrase`

**Method**: `POST`

**Description**: Rephrases the given text using the specified tone and length.

**Request Body**:

```json
{
  "text": "The text to rephrase.",
  "tone": "Professional",
  "length": "Concise"
}
```

**Response**:

```json
{
  "rephrased_text": "The rephrased text."
}
```

### Summarize Text

**Endpoint**: `/api/summarize`

**Method**: `POST`

**Description**: Summarizes the given text using the specified tone and length.

**Request Body**:

```json
{
  "text": "The text to summarize.",
  "tone": "Casual",
  "length": "Moderate"
}
```

**Response**:

```json
{
  "summary": "The summarized text."
}
```

### Generate Reply

**Endpoint**: `/api/reply`

**Method**: `POST`

**Description**: Generates a reply to the given text using the specified tone and length.

**Request Body**:

```json
{
  "text": "The text to reply to.",
  "tone": "Friendly",
  "length": "Detailed"
}
```

**Response**:

```json
{
  "reply": "The generated reply."
}
```

### Create Email

**Endpoint**: `/api/email`

**Method**: `POST`

**Description**: Creates an email based on the given text using the specified tone and length.

**Request Body**:

```json
{
  "text": "The text for the email.",
  "tone": "Formal",
  "length": "Moderate"
}
```

**Response**:

```json
{
  "email": "The generated email."
}
```

## Request/Response Formats

All requests to the API should be made using the `POST` method and should include a JSON body with the required parameters. The responses will also be in JSON format.

## Examples

Here are some examples of how to use the API endpoints:

### Example 1: Rephrase Text

**Request**:

```http
POST /api/rephrase
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "text": "The text to rephrase.",
  "tone": "Professional",
  "length": "Concise"
}
```

**Response**:

```json
{
  "rephrased_text": "The rephrased text."
}
```

### Example 2: Summarize Text

**Request**:

```http
POST /api/summarize
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "text": "The text to summarize.",
  "tone": "Casual",
  "length": "Moderate"
}
```

**Response**:

```json
{
  "summary": "The summarized text."
}
```

### Example 3: Generate Reply

**Request**:

```http
POST /api/reply
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "text": "The text to reply to.",
  "tone": "Friendly",
  "length": "Detailed"
}
```

**Response**:

```json
{
  "reply": "The generated reply."
}
```

### Example 4: Create Email

**Request**:

```http
POST /api/email
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "text": "The text for the email.",
  "tone": "Formal",
  "length": "Moderate"
}
```

**Response**:

```json
{
  "email": "The generated email."
}
```

## Conclusion

This API reference provides an overview of the available endpoints, request/response formats, and examples of how to use the ChatGPT Recipe Toolkit API. If you have any questions or need further assistance, please visit our GitHub repository or contact our support team.

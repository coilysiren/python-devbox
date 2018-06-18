# Five Jobs API

_note: the beginning of this document is a copy paste, my notes follow at the end_

## Overview

As part of {{ NAME }} we hand out jobs to our community of Fives. When they complete the job the five submits an answer back to our server. In this problem you will be asked to design and implement a small API to handle handing out jobs and storing the responses.

Please feel free to use any programming language, or frameworks you would like. We'd like for you to submit a fully working and executable solution, but if you can't quite get it working, please go ahead and submit whatever you have!

## Api Spec

Write a REST-ful HTTP web-application server that has the following endpoints:

| METHOD | PATH                  | REQUEST BODY                       | RESPONSE BODY                                                                          | DESCRIPTION                                                        |
| ------ | --------------------- | ---------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| GET    | /jobs                 |                                    | { "id": 4, "question": "What is your name?" }                                          | Returns a job for the five to work on                              |
| POST   | /jobs/{job_id}/answer | { "id" : 4, "response": "Taylor" } | { "status": "ok" }                                                                     | Submits the answer to the server.                                  |
| GET    | /jobs/{job_id}        |                                    | { "id": 4, "question": "What is your name?" "response": "Taylor", "status": "closed" } | Gets a specific job including the answer if it has been submitted. |

## Notes

- The api spec is the minimum that should be sent/received. Feel free to add other fields
- A Job should only ever get served to a single Five at a time
- A job should only be answered once, then never handed out to a Five again.
- All endpoints should receive and return information formatted in JSON

- Don't worry about authentication or authorization
- Assume jobs are just magically pre-populated in your datastore.
- A "development-only" datastore is totally fine.

## Questions

- What datastore would you use in production? Why?
- What would be the next set of features you would consider to build?
- Why did you choose the language / framework that you did? Did you consider any others?

## Plan

- restart infra
- pre-populate jobs
- spec get available jobs
- spec get unavailable jobs not shown
- spec post answer job
- spec post answer twice returns duplicate status
- spec post cannot answer others job
- spec get job details
- frontend???

## Data

Jobs model

- question text
- response text
- status text (could be an int, but text will allow faster iteration)

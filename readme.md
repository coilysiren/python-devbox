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

## Exercise Notes

- The api spec is the minimum that should be sent/received. Feel free to add other fields
- A Job should only ever get served to a single Five at a time
- A job should only be answered once, then never handed out to a Five again.
- All endpoints should receive and return information formatted in JSON

- Don't worry about authentication or authorization
- Assume jobs are just magically pre-populated in your datastore.
- A "development-only" datastore is totally fine.

## Questions

- What datastore would you use in production? Why?
  - first choice: postgres, its the best default option when nothing about your data format begs an alternative format
  - second choice: mongodb, since (presently) the system can be represented fairly effectively by a document store
- What would be the next set of features you would consider to build?
  - user models / authentication, the model for this is currently very naive
  - the ability to decline an already accepted job
  - make status integers, storing strings should be avoided whenever its (easily) possible
- Why did you choose the language / framework that you did? Did you consider any others?
  - python / flask is the setup I have the most experience with, and its also a fairly effective choice for small scale api servers
  - ruby / rails would be my second choice, since there's generally mild bonus points for using the language your interviewer suggests ^^
  - python / django would be my third choice, it generally supercedes flask if / when an application grows

## Personal Notes

- the api spec implies that answer is a seperate resource, but I think its best understood as an attribute on jobs. the would change the second route to `PUT :: /jobs/{job_id}`. I use a 409 response on that route to represent response collisions, and 409s are generally used in `PUT` requests.
- I would reccomend returning the newly created resoures in POST responses, rather than `{ status: ok }`. In general ok statuses are sufficiently covered by the status code being `200`
- A next step would be to refactor the service layer to use classmethods (to enable easier testing), and have it operate on a less complex input than the flask `request` object (also for testing!).

## Plan

- [x] restart infra
- [x] pre-populate jobs
- [x] spec get available jobs
- [x] spec get unavailable jobs not shown
- [x] spec post answer job
- [x] spec post answer twice returns duplicate status
- [x] spec post cannot answer others job
- [x] spec get job details
- [ ] validate against spec

## Data

Jobs model

- question text
- response text

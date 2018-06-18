# Textio Take-home problem 2

_note: the beginning of this document is a copy paste, my notes follow at the end_

## Overview

Termfront is building ground breaking experiences to encourage people to write and share small snippets of text. To encourage users to write more, Termfront will grant a small set of achievements based on user behavior. However, Termfront has found users are more motivated when the behavior of other users affects the achievements they earn.

The Termfront product management team has come up with the following customer use cases for the MVP of this new offering:

- A customer writes snippets that are stored in the service
- A customer shares or unshares a snippet (shared snippets are visible to other users but unshared snippets are not)
- A customer reads one of their previous snippets
- A customer reads one of another users’ shared snippets
- A customer likes or unlikes another user’s snippet (users cannot like their own snippets)
- A customer retrieves a list of all their earned achievements

The Termfront product management team has also come up with the following achievements to drive user engagement:

- An achievement granted for every 10 snippets created (Achievement name: “created”)
- An achievement granted for every 10 unique snippets shared (Achievement name: “shared”)
- An achievement granted for every 10 likes received (Achievement name: “liked”)

## Spec Overview

Snippets can have up to 300 characters of text. Once earned, a user can never lose an achievement: if a user has earned the “liked” achievement 5 times we should never claim that they’ve only earned it 4 times even if other users remove their likes.

To support these use cases, we have decided to write two new backend services to support both snippet storage and achievements calculation.

## Snippet Api Spec

The first is the SnippetService. It is responsible for storing and serving customer snippets. It should have the following endpoints that accept and return JSON.

<table class="m_582472283179669994MsoTableGrid" border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse;border:none">
<thead>
<tr style="page-break-inside:avoid">
<td width="156" valign="top" style="width:116.75pt;border:solid windowtext 1.0pt;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Endpoint<u></u><u></u></span></b></p>
</td>
<td width="94" valign="top" style="width:70.25pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Description<u></u><u></u></span></b></p>
</td>
<td width="206" valign="top" style="width:154.75pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Input Data<u></u><u></u></span></b></p>
</td>
<td width="90" valign="top" style="width:67.5pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Input Headers<u></u><u></u></span></b></p>
</td>
<td width="78" valign="top" style="width:58.25pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Output<u></u><u></u></span></b></p>
</td>
</tr>
</thead>
<tbody>
<tr style="page-break-inside:avoid">
<td width="156" valign="top" style="width:116.75pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">/snippets (GET)<u></u><u></u></span></p>
</td>
<td width="94" valign="top" style="width:70.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Gets all snippets shared by any user<u></u><u></u></span></p>
</td>
<td width="206" valign="top" style="width:154.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">(Nothing)<u></u><u></u></span></p>
</td>
<td width="90" valign="top" style="width:67.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">(Optional) Authorization &lt;current user’s email address&gt;<u></u><u></u></span></p>
</td>
<td width="78" valign="top" style="width:58.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Array of all shared snippets<u></u><u></u></span></p>
</td>
</tr>
<tr style="page-break-inside:avoid">
<td width="156" valign="top" style="width:116.75pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">/snippets (POST)<u></u><u></u></span></p>
</td>
<td width="94" valign="top" style="width:70.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Creates a snippet<u></u><u></u></span></p>
</td>
<td width="206" valign="top" style="width:154.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">An object containing the snippet’s text and whether the snippet is shared<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><u></u>&nbsp;<u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">Example:
<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">{<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><span>&nbsp;&nbsp;
</span>“text”: “Hello world”,<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><span>&nbsp;&nbsp;
</span>“shared”: true<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">}<u></u><u></u></span></p>
</td>
<td width="90" valign="top" style="width:67.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Authorization &lt;current user’s email address&gt;<u></u><u></u></span></p>
</td>
<td width="78" valign="top" style="width:58.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">A snippet<u></u><u></u></span></p>
</td>
</tr>
<tr style="page-break-inside:avoid">
<td width="156" valign="top" style="width:116.75pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">/snippets/&lt;snippet id&gt; (GET)<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><u></u>&nbsp;<u></u></span></p>
</td>
<td width="94" valign="top" style="width:70.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Gets a snippet<u></u><u></u></span></p>
</td>
<td width="206" valign="top" style="width:154.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">(Nothing)<u></u><u></u></span></p>
</td>
<td width="90" valign="top" style="width:67.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Optional) Authorization &lt;current user’s email address&gt;<u></u><u></u></span></p>
</td>
<td width="78" valign="top" style="width:58.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">A snippet<u></u><u></u></span></p>
</td>
</tr>
<tr style="page-break-inside:avoid">
<td width="156" valign="top" style="width:116.75pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">/snippets/&lt;snippet id&gt; (PUT)<u></u><u></u></span></p>
</td>
<td width="94" valign="top" style="width:70.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Likes or shares a snippet<u></u><u></u></span></p>
</td>
<td width="206" valign="top" style="width:154.75pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">An object containing whether the snippet is shared or whether the snippet is liked<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><u></u>&nbsp;<u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">Example input for sharing a snippet<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">{ “shared”: true }<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><u></u>&nbsp;<u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">Example input for liking a snippet<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">{ “liked”: true }<u></u><u></u></span></p>
</td>
<td width="90" valign="top" style="width:67.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Authorization &lt;current user’s email address&gt;<u></u><u></u></span></p>
</td>
<td width="78" valign="top" style="width:58.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">A snippet<u></u><u></u></span></p>
</td>
</tr>
</tbody>
</table>

A returned snippet object should have the following form

```
{

   “snippetId”: <some ID>,

   “text”: <the snippet’s text>,

   “owner”: <the email address of the user that created the snippet>,

   “shared”: <a Boolean indicating whether the snippet is shared,

   “likes”: <the number of users who like this snippet>

}
```

## Achievement Api Spec

The second service is the AchievementService, which is responsible for tracking the user’s achievements. It should have a single public endpoint.

<table class="m_582472283179669994MsoTableGrid" border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse;border:none">
<thead>
<tr style="page-break-inside:avoid">
<td width="126" valign="top" style="width:94.25pt;border:solid windowtext 1.0pt;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Endpoint<u></u><u></u></span></b></p>
</td>
<td width="101" valign="top" style="width:75.55pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Description<u></u><u></u></span></b></p>
</td>
<td width="85" valign="top" style="width:63.95pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Input Data<u></u><u></u></span></b></p>
</td>
<td width="90" valign="top" style="width:67.5pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Input Headers<u></u><u></u></span></b></p>
</td>
<td width="222" valign="top" style="width:166.25pt;border:solid windowtext 1.0pt;border-left:none;background:#44546a;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><b><span style="font-size:9.0pt;color:white">Output<u></u><u></u></span></b></p>
</td>
</tr>
</thead>
<tbody>
<tr style="page-break-inside:avoid">
<td width="126" valign="top" style="width:94.25pt;border:solid windowtext 1.0pt;border-top:none;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">/achievements (GET)<u></u><u></u></span></p>
</td>
<td width="101" valign="top" style="width:75.55pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Gets the achievements earned by a user<u></u><u></u></span></p>
</td>
<td width="85" valign="top" style="width:63.95pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">(Nothing)<u></u><u></u></span></p>
</td>
<td width="90" valign="top" style="width:67.5pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">Authorization &lt;current user’s email address&gt;<u></u><u></u></span></p>
</td>
<td width="222" valign="top" style="width:166.25pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt">
<p class="MsoNormal"><span style="font-size:9.0pt">An object containing the number of times each achievement has been earned<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><u></u>&nbsp;<u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">Example output<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">{<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><span>&nbsp;&nbsp;
</span>“created”: 10,<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><span>&nbsp;&nbsp;
</span>“shared”: 2,<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt"><span>&nbsp;&nbsp;
</span>“liked”: 3<u></u><u></u></span></p>
<p class="MsoNormal"><span style="font-size:9.0pt">}<u></u><u></u></span></p>
</td>
</tr>
</tbody>
</table>

## Expectations

For this problem, we'd like you to build and stand up an initial version of two services that solve the customer use cases, including expected error conditions. While you’re working through this problem, assume that I am playing the role of Product Manager and available to answer any questions you have.

- The first hour of your interview day will be a group session where you will present your work to the engineering team. An ideal presentation covers:

- Description of the architecture of the services and software design
- How you implemented the different user scenarios and tradeoffs you made
- Walkthrough of key parts of the code
- Significant technical decisions you made
- Live demo of the services, if possible
- Description of additional work that would need to be done to bring the services into production, or other things you didn’t get to

For your work on this project and in the group session we’ll be looking at:

- Functional completeness of your work based on the given user scenarios
- Services architecture and division of responsibility between the two services
- Software and database design – your approach to organizing code and data modeling to build the services
- Code quality and craft - we love code that is readable, testable, and maintainable
- Your skill at communicating the above to technical teams

## Notes

- this is a REST api server project, no frontend needed
- dont leave tech debt in, do keep the linter running

## TODO

- [ ] can TDD the endpoints and error cases (TDD works well in this case!)
- [ ] the spec defines "least effort" versions of the endpoints, do feel free to add more data to them
- [ ] include examples of how the endpoints would be used
- [ ] look for some programmatic documentation generation
- [ ] take some inspiration from twitters api docs
- [ ] authorization parsing should be a decorator with default `optional=False`
- [ ] prep a postman (or similar) demo
- [ ] run through a REST api best practices doc
- [ ] `db.create_all()` call

## Questions / Clarifications / Decisions

- there's no explicit users endpoint, so the application auto-creates users from the a unique email address is present in the Authorization header. **@ProductManager**: should there instead be an explicit users endpoint?
- the api blocks the creation of snippets with empty text. **@ProductManager**: should users be allowed to create empty snippets?
- the api defaults snippets to being shared (eg `shared=True`). **@ProductManager**: should there be a default share state, and if so should it be true or false?
- the get endpoint returns unshared snippets for the currently authorized user. the idea here is that your "home timeline" isn't just "all shared posts" but instead "all posts you can see". "all posts you can see" means "shared posts" and also "unshared posts that you own". **@ProductManager**: this should be accounted for on the front-end, likely via graying out the unshared snippets

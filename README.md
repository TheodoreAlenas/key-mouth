
# Key Mouth, the persistent, per-key instant messenger

[It's served.](https://theodoros-d-alenas.site/key-mouth/)

Web app that reminds of instant messengers,
except each key press shows up in real time,
and deletions appear as erased text persistently.

In a typical messenger there are bubbles per sent message,
and this app has a bubble per significant moment,
such as someone interrupting a conversation or people pausing.

## Code structure

Since I lacked the skills for the app, I had to go incrementally.
This meant I needed a fast way to prove the code is roughly correct.

- Limiting the `import` shows what code may be responsible for a bug.
- A dev mode shows that there is some way for the system to run right.
- Tests show when there is some way for the system to run wrong.
- Some tests mimic debugging, making "debugging" re-runnable.

I have bad experiences from hierarchies
such as subdirectories, deep indentation and deep call stacks.
There are multiple directories and some short files in the codebase
but I dislike both directories and short files.
The project started as very few big files
and eventually code got extracted,
days after I started wanting to extract it.
Most extractions were done because it was hard to track down
how the different abilities of the system
related to variables and functions.

### Web

The client sends `+h`, `+i`, `-i` through the socket.

The server sends the diffs back as JSON
in a forman that's easy to turn into protobuff in the future.

The socket messages don't prompt for fetch requests on other endpoints.

### Server

The FastAPI code is in one place
and it's only tested through the front-back integration test.

Most of the code stays outside and
the tests execute it without importing FastAPI.

The different events create event data structures,
which can be turned into
data structures for the database (and back)
and for the client.

An important event is the event that the "speech bubbles" can be split.
If this README is up to date, the "speech bubble" is called moment.
When they split, a moment can be stored in the database,
since the diffs in it can be displayed
without fetching previous diffs.
One of the reasons why there are three data structures for events
is that for the database the ending of a moment is the end of a list,
while for the client the ending of a moment is an event.
Also, if this is still the case,
the client gets the moment id and diff id per event, for validation.

### Client

One directory has NextJS code.

ReactJS code is in part in that directory
but mostly in another directory.

Most Javascript code is outside of both,
in a directory with a `package.json` file
that declares the files ES modules.
That way, the test files among them can be ran with
`node <filename>` from the shell.

If this README is up to date,
there's a `TestCase.js` file with a class of the same name.
I found `jest` to be uncomfortable so I thought to implement
something reliable-enough on my own,
so long as it doesn't exceed a laptop screen of lines of code.

The server data is turned into a data structure
that can easily be turned into ReactJS components.

If this README is up to date, there's an intermediate step,
where the events are turned into a data structure
that the `accumulateDiffs` function accepts.
The data structure it returns isn't meant to be the final view model.
That way, `accumulateDiffs` can stay the same for longer.

The mechanism that takes events and produces the view model
is made to be reusable,
because once it's made possible to scroll far up in old messages,
it will be reused to create the view model of fetched events.

## Story

I took up this project to learn NextJS and Python's FastAPI,
when I interned in the chatbot company [Helvia](https://helvia.ai)
in July 2024, between 5th and 6th year in the University of Athens.
I started in the operations and a month later
I was told to practice development go to the backend.

Although I had written small CLI programs before
and I wasn't a complete beginner in the languages,
I didn't grasp events, state management, sessions, users
and the web technologies.
I did read Robert C. Martin's Clean Architecture book however,
which proved to be helpful.

I was told I could make a taks management app,
but I said I had an idea in my head
and they told me I could try it instead.

I really should have done the task management app.
I generally refused to listen and I broke a lot of unwritten rules
regarding who to talk to and what opinions to question,
and I honestly regret the way I talked because it didn't help anyone.
In the end, I can't exclude that maybe I was given this project
because they wanted to take a breath from me.
The internship was 3 months full time
and the last 2 monts were spent on this project.

I was also looking for an apartment so I was stuck in Athens in August,
when people go to their parent's villages.
I was mentally declining,
I had fantasies where I showcase a beautiful web app
and the company claps.
If you've taken on an ambicious project before
then you know that this is not how the world works,
and I knew it too.
The people in the company are fantastic
and I'm not asking for claps from them,
but I was going crazy and I was full of shit.

### UI

Today the project looks staightforward
but there was no point of reference.

The concept had 2 parts:

> I wish I could see what the others are typing.
> Sometimes it takes them too long to type a message
> and then it turns out they misunderstood me.
> If I knew what they were typing, I could tell them to stop.

and, the harder one:

> Since I'll be able to see the other person
> deleting something in real time,
> I'd like to be able to scroll up in the older messages
> and still be able to tell roughly what happened at that moment.
> Maybe what they deleted appears as text with a strike through.

This implied something much broader:
time-dependent phenomena should appear in a way that tells the story,
*without animations*.
I didn't understand this requirement well enough to phrase it this way.

Here is part of the oldest concept:

```
Tom:
- Hi [hter]there, did you

Tom and Tedd together:
- go to the oh cool
- party yes I loved it
```

Then I realized I can't use key up and key down events
because on mobile there's auto-correction.
This means there should be a text box.
But if there's a text box, one can edit the middle,
so that brought the next wave of concepts:

```
Tom: I was thinking if you'd want
Tom: [I wa]nted to ask you[ if you'd want]
Tom: to go to Tedd's party
```

The first week, every day I thought I'm almost done,
until the end of the week when I discovered something scary.

If you have some experience, you may notice the flaw.
How many write events and deletion events
does one need to fetch from the database
in order to know how to present a message?
Possibly all of them.
Imagine someone fills up the text box during a heated conversation,
leaves for some coffee,
the others keep talking fast,
and then he comes back and edits the middle of the text box.
One would need to get all those events to construct the view.
You may disagree for a moment but
if you notice, every workaround is painful.

I started to believe there could be a mathematical proof
that the fundamental requirements for this app are self-contradicting.

In the end, I decided to ignore the intricasies
and treat any change in the text box as a deletion from the end
or an addition to the end.
Changes to the middle of the text box were deletion and addition:

```
Tom: I wa[s thinking if you'd want]n[s thinking if you'd want]t[...
```

The second week the code somewhat stabilized,
the third I worked massive amounts and I deployed this:

```
Hi ehre-e-r-h-ethere
```

because the protocol was `+e +h +r +e -e -r -h -e`
and I just removed leading `+` signs.

Then it progressed:

```
                10/8/2024 09:32:41 AM
Tom: Hi [ehre]there
                10/8/2024 09:32:43 AM
Tom: Mark oh nice you're here
Mark: Oh hi
```

I kept thinking this app can't possibly look familiar,
until I came up with the next design:

```
09:32:41 AM, Tom
o  Hi [ehre]there

09:32:43 AM, Tom, Mark
o  Mark oh nice you're here
o  Oh hi
```

and in the middle of the second month it became `Hi |there`
where if one clicks it, it expands into `Hi [ehre]there`.

### The evolution of the logic

The first week,
writing any line of code required me to comprehend the whole system,
and every line of code proved all the plans ineffective.

For that reason I decided to set up a bit of everything
and make some web app without CSS
which can support one socket connection
and has no concept of a chat room.
The user would only be able to write text properly,
if they deleted text something arbitrary would happen.

Thankfully I was familiar with HTML and CSS,
however I didn't know React, what a socket is
or how to handle events.

The first week there was only one Python file:

```python
data = await websocket.receive_text()
if ...
for ...
websocket.send_json(reply)
```

I'm generally obsessed with tests
so I knew I had to detach as much code as possible
from FastApi to be able to test it later.
It was simple:

```python
data = await websocket.receive_text()
reply = f(data)
websocket.send_json(reply)
```

Then I supported multiple connections.
The biggest challenge is that I didn't want the `await` keyword
in my code because I assumed it would make the tests painful.
That however meant I couldn't pass the socket into an object.

```python
logic.add_socket(websocket)  # cancelled
while True:
    data = await websocket.receive_text()
    logic.handle_input(data)
```

I came up with a solution that surprized me:

```python
res = conn.handle_input(time(), data)
for conn_id, json in res:
    await id_to_sock[conn_id].send_json(json)
```

I'm sure that by this point there were tests.

The code grew and there were many functions that took the current time
as one of their arguments and perhaps returned a response,
maybe alongside other data.
So the conclusion was:

```python
await wrap(conn.handle_input, data)
```

and every function took `f(time, other)` and returned `(res, other)`.

The files were `main.py` and `AfterSocketLogic.py`.
Once `wrap` got error handling and a mutex,
even the other endpoints started using it,
so `AfterSocketLogic.py` was used for renaming chat rooms too.
Much later it became a central hub that imported other files,
later I extracted as much code as possible out of it
and then it got the name `wiring/Main.py`.

There are similar stories around the other modules
and `Controller.js`
which used to be called `WebInteractor.js` somehow.

### Unfamiliar web dev skills

Event handling started as
if statements and while loops fiddled in place.
Then, after a lot of thought, I saw a pattern:
the server took note of happenings
and phrased them to the sockets and to the database.
I read something similar before, in the Clean Architecture book.
There were some audacious plans about vast changes
but in the end the data mappers were just written
one by one incrementally.

Pagination was added in the middle of the second month.
I thought I could fetch a number of moments from the database
when scrolling far up.
The problem was how to scroll back down.
By the time the lower moments arrive,
maybe the cached bottom moments that come in real time
have moved and left a gap.
That's not much of an edge case.
After a lot of sketches, I realized there are 3 states:
bottom-only, contiguous and detached,
and they need to be considered by various if statements.
With pagination, moments would come in pre-split pages
and a lot of problems would become simpler.

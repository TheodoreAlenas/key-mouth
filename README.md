
# Key Mouth, the persistent, per-key instant messenger

[It's served.](https://theodoros-d-alenas.site/key-mouth/)

Web app that reminds of instant messengers,
except each key press shows up in real time,
and deletions appear as erased text persistently.

In a typical messenger there are bubbles per sent message,
and this app has a bubble per significant moment,
such as someone interrupting a conversation or people pausing.

## Essential features

- [x] interrupting breaks the moment
- [x] silence breaks the moment
- [x] isolated chat rooms
- [x] visible deletions
- [x] visible dates
- [ ] a new message can reference an old one, creating links both ways
- [x] persistent storage
- [ ] authentication
- [ ] locked rooms that require an invitation
- [ ] administration bans

## Secondary features

- [ ] image uploading
- [ ] some stages of the upload act like messages, perhaps 0%, 50%, 100%
- [ ] uploading an amount of text which appears folded
- [ ] editing a copy of someone's uploaded text
- [ ] drawing strokes on someone's uploaded image
- [ ] these edits appear to the others like messages in real time
- [ ] guest chat rooms that don't need authentication, at some tradeoff

## Unlikely features

- [ ] audio/video calls
- [ ] integration with video platforms to display videos inside the app
- [ ] GUI apps outside the browser

## Code structure

The architecture is inspired by
Robert C. Martin's Clean Architecture book.
It allows fast tests to be thorough and convenient to write,
at the cost of underutilizing thrird party frameworks
and adding some abstraction.

I'd recommend reading the scripts first
because I run them often.

### Web

The client sends `+h`, `+i`, `-i` through the socket.

The server sends the diffs back.
It does not send something closer to the final view.
The data is more complicated and varied from server to client,
so it's JSON,
but with a format that makes it reasonably easy
to turn it into protobuff in the future.

The socket never tells the client to do a fetch request
on another endpoint.
This did use to happen,
but eventually the socket was made to give the information itself.

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
that can easily be turned into ReactJS components

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

This project was for me to learn NextJS and Python's FastAPI.
I became an intern
in a chatbot company called [Helvia](https://helvia.ai)
in July 2024.
I started in the operations and a month later
I was told to practice with their tools to go to the backend.

Although I had written small CLI programs before
and I wasn't a complete beginner in the languages,
I didn't grasp events, state management, sessions, users
and the web technologies.

I was told I could make a taks management app,
but I said I had an idea in my head
and they told me I could try it instead.

Now that the project has progressed it looks staightforward,
but the concept only outlined roughly what should be possible.
An early concept was

```
Tom:
- Hi [hter]there, did you

Tom and Tedd together:
- go to the oh cool
- party yes I loved it
```

Then I realized I can't use key up and key down events
because on mobile there's auto-correction.
But if there's a text box, one can edit the middle.
A later concept was:

```
Tom: I was thinking if you'd want
Tom: [I wa]nted to ask you[ if you'd want]
Tom: to go to Tedd's party
```

If you have some experience, you may notice a flaw.
I didn't have the experience, so it took me a week.
In essense, how many write events and deletion events
does one need to fetch from the database
in order to know how to present a message?

The first week, every day I would think I'll be done in two more days.
I went from plan to code back and forth multiple times a day,
because every part of a plan
was proven ineffective by a few lines of implementation code.
The experience reminded me of the way people advertise waterfall,
because indeed I was too overwhelmed to code without plans.

The second week
the code stabilized to the point where
I could extract it into different files
and write tests.
The company was supportive and I was told to continue.

The third week I worked massive amounts.
On the evening of Friday I served a pitiful web app
without a database.
It didn't display deleted text properly,
it would look like

```
Hi ehre-e-r-h-ethere
```

because the protocol was `+e+h+r+e-e-r-h-e`
and the temporary implementation
was to display everything but plus signs.

I was mentally declining because I was stuck in Athens in August
and the streets were empty.
I had fantasies of showcasing a beautiful web app
to the company and getting claps in the online meeting.
I was full of shit
and I started to de-value a lot for the sake of the project.

The fourth week I implemented many features
and I did a ton of refactoring.
I started to understand the state management and the flow of events
through the system,
so the code started to reference my understanding.

In the end of the fourth week,
the person who assigned the task and my mentor saw the app.
My fantasies were crushed so bad that I spent 7 hours on YouTube,
didn't eat from 11am that day to 2pm next day.
I lacked sleep and before going to the Goody's
I spent half hour listening to heavy metal
and another hour reformulating the situation in my head.
I was mentally exhausted and my shaming circuits burnt out.
I sat on a bench, put the Goody's box next to me and
it slipped and spilled the burger and potatoes on the ground.
I was so mentally exhausted that,
Once I comprehended what just happened,
I causally picked up and ate the parts that
landed on top of other parts.

And that's the story thus far,
24th of August 2024.


# Key Mouth, the persistent, per-key instant messenger

[It's served.](https://theodoros-d-alenas.site/key-mouth/)

Web app that reminds of instant messengers,
except each key press shows up in real time,
and deletions appear as erased text persistently.

In a typical messenger there are bubbles per sent message,
and this app has a bubble per significant moment,
such as someone interrupting a conversation or people pausing.

The architecture is inspired by
Robert C. Martin's Clean Architecture book.
Frameworks are pushed to the side and the system is cut in ways
that make it convenient to write fast tests.
It started out as a small cluster of code in a few files
and slowly it started to form parts.
The database was added later and it was made to mimic the mock.

To understand the system,
I'd recommend starting from the scripts
for testing and for setting up my environment.
The deployment scripts are ignored by git.

## Necessary basic features

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

## Wanted features

- image uploading
- some stages of the upload act like messages, perhaps 0%, 50%, 100%
- uploading an amount of text which appears folded
- editing a copy of someone's uploaded text
- drawing strokes on someone's uploaded image
- these edits appear to the others like messages in real time
- guest chat rooms that don't need authentication, at some tradeoff

## Unlikely features

- audio/video calls
- integration with video platforms to display videos inside the app
- GUI apps outside the browser

## Story

I was told to learn NextJS and Python's FastAPI
by making a pet project.
I had no experience in web development
so I wasn't used to thinking about
sessions, users, databases, concurrency etc.

I happened to have an idea for a project at that time,
an instant messenger, your friend types
and you see him type letter by letter.
You also see him delete,
and the deletions stay,
perhaps they're fainted text with a strike through.

It sounded simple.
Each person sends diffs, such as letter typed, letter deleted,
the diffs stay in a database
and the other person's browser reads them and
constructs the appearance of the messages.

But if the placement of a letter on the screen
depends on what happened right before...
How far back does one need to go in history
to decide where a letter is placed on screen?
Also, what if someone changes the middle of their input box?
And if there's no input box, what about smartphone auto-correction?

The first week I thought I'm almost done.
I thought I'm almost done every day
and I went from plan to code to plan and back to code.

The second week
the code stabilized to the point where
I could extract code into different files
and write tests.

The third week I don't even remember what happened.
I worked in the mornings,
I worked in the evenings,
I worked in the weekends,
I worked and I worked and I worked,
and on the evening of Friday I served *something*.
It showed keys in real time,
it had chat rooms
and it showed some gap between messages
where one interrupts the other.
But it didn't show deletions.
It didn't have a database either.

I remember Robert Martin talking about the time
when he did a start-up and he writes in his book
"we wanted to be millionaires, we [...], we were full of sh-"

The fourth week I implemented a lot and I did a ton of refactoring.
I started to see the full picture and to comprehend how
as you scroll up in the messages there are 3 states,
and how there was the concept of an event
which may or may not have to be stored and sent to the client.
There was a big refactor where
I tried to paint my understanding into the code.

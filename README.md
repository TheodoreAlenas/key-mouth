
# Key Mouth, the persistent, per-key instant messenger

[It's served.](https://theodoros-d-alenas.site/key-mouth/)

## Concept

You are given a link to participate in a discussion.

You join, and you see an instant messenger.

At first glance it looks familiar,
it's short text messages by different people,
however it's full of faded text like someone scraped off typos.

Before you have time to process that,
the last message gets a dot in the end.

Then there is a short pause.
The last message was controversial.

One second later,
four people start talking at the same time,
creating a lump of messages with a small gap
from the controversial message.

They get longer letter by letter
and some people type faster than others.
One of them makes a typo,
the last letters get faded,
and after the faded letters new letters appear.

You jump into the debate and the moment you interrupt,
the bulk of messages gets cut
and a new one starts a little lower
with your message at the top of the new lump.

## Necessary basic features

- [x] interrupting breaks the moment
- [x] silence breaks the moment
- [x] isolated chat rooms
- [x] visible deletions
- [ ] visible dates
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

I was hungry that day because I didn't eat.
I was trying to do some work fast to go on
with other priorities that piled up,
and in the end I didn't do them.

It's hard to say if I'm having fun
but I know I can't stop.
It's exhausting sometimes.
I remember Robert Martin talking about the time
when he did a start-up and he writes in his book
"we wanted to be millionaires, we [...], we were full of sh-"

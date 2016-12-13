# Twin Peaks Diary

@tpeaksdiary on Twitter is a bot that generates animated gifs from the show Twin Peaks. It's a kind of way to re-experience the show through random micro bursts of nostalgia. The idea came from @wirescenes, a similiar bot for the show The Wire.

![example gif](http://68.media.tumblr.com/912b940a5053a5cd0ec2ad2aaa204619/tumblr_od7608awX91uw0e6yo1_400.gif)

I think it's my favorite bot I've made so far!

Oh it also posts to Tumblr, where nobody follows it ;P

I made this a while ago without taking notes, and nothing was in version control then, so my memory and the record is a bit foggy.

## Method

### What To Gif

The first step was figuring out what to make into a gif. I just wanted dialogue, people talking.

So I relied on some subtitle files, in the SRT format. I found some SRT files on I *believe* [tvsubtitles.net](http://www.tvsubtitles.net), that matched up perfectly with the source material I had (not including any of this in repo for copyright reasons).

SRT files are organized in time stamps that give a range of time, like this:

```
144
00:21:09,407 --> 00:21:11,841
- Audrey Horne?
- Here.
```

The `parse_srt` function loops through every subtitle entry in a file, and organizes it into a scene list. One scene == one gif.

It looks like I did put a cap on the length of a scene at 8 seconds.

It then collects these scenes and does three things:

- Passes the time length stamps to `ffmpeg` to chop the larger episode mp4 into a smaller one
- Creates an `.ASS` file (I'm not making this up), which is a subtitle formatting file output by the Aegisub subtitling app, to accompany the mp4.
- Takes this small mp4 and runs it through `gifify` to convert the mp4 + .ASS file to a gif.

Gifify does accept time ranges, but I found in practice it was unusably slow when operating on very large files, like an episode of Twin Peaks. Instead I used ffmpeg to chop of the files ahead of time, as it's way way faster.

It took a while to get the right ffmpeg syntax, as by default it cuts on keyframes, which does not work when you are talking 4 second clips that need to be down to the millisecond. But eventually got it.

### Episode Selection & Tweeting

Initially I wanted to tweet what I think is the heart of the show, the best stuff. So that means all of Season 1 including the pilot, and the series finale.

As of this writing (12/26/16) I haven't gif'ed Season 2, but planning on doing so soon.

I created all the gifs in one giant batch job on my laptop, and simply uploaded the resulting gifs, with a list that pulls from a text of gif files to tweet, as well as track what's been tweeted so far.

In other words, the gifs are not created on demand, but were all created ahead of time. The order was randomized, but only once, so I know what will tweet / when, technically.

### The Subtitle Font

The opening credit theme for Twin Peaks and it's font is iconic, and a thing folks associate with the show. Bright green thick outlines with red inside. So I wanted to re-create it as much as I could.

At first I tried using the exact same font and colors used in the opening credits. Well, it's fine for a list of names, but horrible for actual dialogue. It was completely unreadable.

So I decided to just go for a general nostalgic gestalt that was actually readable, rather than 100% accuracy.

I fooled around in Aegisub to generate something that was more legible, but looked sorta like the original. I ended up just using Open Sans for the font, and played with the color/stroke settings until I was happy.

The resulting .ASS file is then used as a template in creating the an ASS for each gif file. 





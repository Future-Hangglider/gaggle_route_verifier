# Gaggle route verifier
Do competition pilots follow lifty lines away from the task track?

We are going to look at sets of tracks from the lead competition pilots following tasks 
who would normally go direct to each turnpoint by the shortest line.

There's a theory that some of them can "pick a good line" which is much less sinky and 
fly off the direct line, but save on later thermalling. This project looks for the evidence.

For extra points, we could implement the [GAP scoring system](https://www.fai.org/sites/default/files/documents/annex_24b_-_proposal_scoring.pdf) thing.

## Data sets
data/R3T3tracks fetched from https://bos.bhgcomps.uk/content/round-3-task-3
Others are downloaded from: https://nats.bhgcomps.uk/content/task-1

## Proposed algorithms

It's first necessary to identify comparable gliders working within the same 
air space for a duration of time.  This will be a selection of a time interval 
and a subset of gliders.

Detect gliders thermalling in same or adjacent thermals for a period, and also detect 
gliders on glide in the same direction (to same destinations) choosing a line

Then with comparable gliders, we can see their different climb rates in same thermal
or gliding to a destination.  The destination is either towards a turnpoint or 
towards a thermal (often marked by another glider). 

Can we decompose the performance in comparison according to (a) more efficiency of 
glider, (b) choice of airspeed, (c) passing through better air?

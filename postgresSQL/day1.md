**The problem:** the same moment in time can display as different clock times depending on the time zone, and a database has to store it so nothing gets lost or misread. If you get this wrong, a report like "orders per day" gives different numbers depending on whose day you mean. That's the most common data bug in real systems.

**Today's first goal:** understand what Postgres actually stores in a timestamp column, and why the same row can show different times.

**Why we start here:** every later topic (grouping by day, window functions over time, joins on dates) depends on this being right.

The question for Step 1: if I look at the same order's `placed_at` from Tokyo and from New York, is it one moment or two different moments?

Say that back to me in your own words, even if you're guessing, and then we run the first query to check.
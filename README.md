# botrnot
Bot or Not detector

## WIP!

`pip3 install botrnot`

## Usage

You can run `botrnot -h` and it shows the following:

```
$ botrnot -h
usage: botrnot [-h] [-u USERNAME] [-n] [-v] [-j]

collects and processes twitter data example: botrnot -u jamescampbell

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --user USERNAME
                        username to evaluate (default: jamescampbell)
  -n, --no-logo         dont display logo (default False) (default: False)
  -v, --verbose         print more things out about search (default: False)
  -j, --json            save tweets out to json file (default: False)
```

## Example

For user realdonaldtrump:

```
Most recent tweet
+-------------------------------+----------+--------+-------+---------+---+----+
|           tweettext           |   type   |  rts   | favs  | replies | t | id |
|                               |          |        |       |         | i |    |
|                               |          |        |       |         | m |    |
|                               |          |        |       |         | e |    |
|                               |          |        |       |         | s |    |
|                               |          |        |       |         | t |    |
|                               |          |        |       |         | a |    |
|                               |          |        |       |         | m |    |
|                               |          |        |       |         | p |    |
+-------------------------------+----------+--------+-------+---------+---+----+
| We are on track to APPREHEND  | original | 12982  | 50612 |  10721  | 1 | 11 |
| more than one million people  |          |        |       |         | 5 | 03 |
| coming across the Southern Bo |          |        |       |         | 5 | 66 |
| rder this year. Great job by  |          |        |       |         | 1 | 63 |
| Border Patrol (and others) wh |          |        |       |         | 9 | 38 |
| o are working in a Broken Sys |          |        |       |         | 6 | 36 |
| tem. Can be fixed by Congress |          |        |       |         | 9 | 56 |
|  so easily and quickly if onl |          |        |       |         | 5 | 07 |
| y the Democrats would get on  |          |        |       |         | 3 | 93 |
|            board!             |          |        |       |         | 4 | 6  |
+-------------------------------+----------+--------+-------+---------+---+----+

Metrics table
+---------------------------+-----------+
|          Metric           |  Amount   |
+---------------------------+-----------+
|  Total tweets collected:  |    420    |
+---------------------------+-----------+
| Total that were retweets: | 93 (22%)  |
+---------------------------+-----------+
|      Retweets in 327      |  8689464  |
+---------------------------+-----------+
|      Replies in 327       |  8247694  |
+---------------------------+-----------+
|     Favorites in 327      | 37984435  |
+---------------------------+-----------+

Bio table
+-----------------+------------------------------------------------+
|    Full Name    |                                                |
|                 |                Donald J. Trump                 |
+-----------------+------------------------------------------------+
| Followers count |                     58.9M                      |
+-----------------+------------------------------------------------+
| Following count |                       45                       |
+-----------------+------------------------------------------------+
| User Biography  | 45th President of the United States of America |
+-----------------+------------------------------------------------+
|  User Location  |                 Washington, DC                 |
+-----------------+------------------------------------------------+
| User Join Date  |               Joined March 2009                |
+-----------------+------------------------------------------------+
| User Birth Date |                                                |
+-----------------+------------------------------------------------+
|     User ID     |                    25073877                    |
+-----------------+------------------------------------------------+

```

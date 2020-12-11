Now Playing
===========

Back when irc was a thing, some annoying people would announce what
they were playing on their xmms software. Now that Github is a social
media, we can do the same!

Setup
-----

Connect your Spotify account to Last FM. Or if you use something else
to play music, look for "scrobbling" in the documentation.

Get a [Last FM API key](https://www.last.fm/api/account/create)
and a [Github personal access token](https://github.com/settings/tokens).
The Github token needs the "user" scope.
Set the environment variables `$lf_user` (Last FM username), `$lf_key`
(the API key), `$gh_user` (Github username) and `$gh_token` (Github token).
Invoke the script with those environment variables from cron or something,
being careful to stay under any API access limits.

# Days Until Zero New Cards

This is an [Anki](https://apps.ankiweb.net/) addon that shows the number of days until you have zero new cards left in a deck.
This is based on the number of new cards per day limit and assumes no days are
missed

By default, suspended cards are not counted. Additionally this will intentionally not count "today only" limits. Only changes to presets and per deck limits will affect the numbers. However, in determining the end date, the exact number of new cards
today will be included into the calculation

If you have deck with subdecks, it will only look at the deck's set limit.
It will not check if limits set on subdecks would stop it from reaching that in a day

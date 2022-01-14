# relkochta/koreader-sync

[KOReader](https://github.com/koreader/koreader) is a cross-platform e-book reader.

It has a [sync server](https://github.com/koreader/koreader-sync-server) available to sync book progress between devices, but this has not been updated for 5 years (plus who writes Lua these days anyways?). There is another implementation by [myelsukov](https://github.com/myelsukov/koreader-sync), but it is very minimal and, according to its author, "quick and dirty."

I hope to build an alternative that uses a proper database (SQLite/MariaDB) and is scalable. I also wanted something pre-configured to run in Docker.

The core API of this project is loosely based on the interface in myelsukov's application. It is still heavily work-in-progress and not ready for use yet.

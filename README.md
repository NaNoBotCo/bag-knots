# Bag Knots · มัดถุง

Every way a Thai shop ties a bag shut, drawn step by step, and how to open each one, by hand or with scissors. English and Thai, with NaN and Beer.

https://nanobotco.github.io/bag-knots/ · https://nanobotco.github.io/bag-knots/th/

- `tools/ties.py` holds every tie: keyframes for the drawing plus each step's words in English and Thai.
- `tools/art.py` draws the pictures (NaN and Beer from the Facebook avatar scripts in `tools/cast/`); `tools/build.py` writes the pages; `tools/card.py` the share card.
- `docs/app.js` draws each tie on a canvas. Test hook: `?s=<n>` shows every tie at step n.

    python3 tools/art.py && python3 tools/build.py && python3 tools/card.py

Text CC BY 4.0, NaNoBotCo. Code MIT.

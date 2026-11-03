# Jonathan’s PiDog Camera Lab — Student Edition

Start here: extract the whole folder and open **index.html** in your browser.

1. Read Quick Start with your teacher and check the camera setup.
2. Work through Session 1: light, pixels, color and camera experiments.
3. Work through Session 2: visual meaning, regions, learning and the robot pipeline.
4. Keep the Experiment Notebook open during tests. Use the glossary when a term is new.

Each session is two hours, including a short break. Write your predictions before running an experiment. Record failures as well as successes.

## Your files

- docs/: interactive lessons, setup, glossary, experiment notebook and sources.
- printable/: editable Markdown versions of those documents.
- exercises/student.py: four functions for you to complete.
- camera_lab/: working camera and image-analysis code to run, read and investigate.
- tests/: checks for the supplied software.
- data/: synthetic practice images and measurement templates.
- diagrams/: system diagrams and editable Mermaid sources.

This edition contains no tutor guide or completed exercise solutions. The working lab programs and explanatory examples are included so you can run the experiments.

## First commands

Run from this extracted folder:

```sh
python3 -m unittest discover -s tests -v
python3 -m camera_lab.analyze data/blue-center.json --out results/first-blue
python3 check_exercises.py --student
```

The software tests should pass. Your exercise checks will fail until you complete the four TODO functions; use their feedback to improve your work. Give each experiment a new output folder name.

For real capture, follow Quick Start and run the camera commands on PiDog through your existing SSH connection. Offline image experiments run on a laptop too. The supplied programs send no motor commands. Work with your teacher on hardware setup and stop other robot/camera programs first.

## Save your work

Export a JSON backup from each lesson after class. Restore it in the same lesson to continue on another browser. Export Markdown for readable notes, or use Print / PDF. Keep your captures and results folders too: they are not embedded in notebook backups. The browser image bench is a practice tool and its state is not backed up.

See VALIDATION.md for the software checks and remaining on-device checks. Start with the setup checklist before assuming the live camera is ready.

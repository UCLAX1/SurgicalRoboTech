# Pre-Requisites:

I've found VSCode or PyCharm to work best

All instructions will be for macOS/Linux

**Steps:**
(this assumes that you have python (version 3.10 tested), anaconda, brew, and xcode cmd line tools installed)

1. Navigate to project directiory
2. Create a python virtual environment:

`python -m venv venv`
3. Activate python virtual environment: 

`source venv/bin/activate`

You should see the name of your virtual environment in the terminal
4. Install openCV:

`pip install opencv-python`
5. Install mediapipe: 

`pip install mediapipe`
6. Open Project folder (dragging works) in your IDE/text editor of choice
7. Select virtual environment (the one you just created should show up as an existing environment)
8. Download `handTracking.py` and place it into the project folder base (not in the venv)
9. Open `handTracking.py` in your IDE/texteditor
10. Run file
11. Profit!

**In case of missing modules errors:**

`pip install "name of module"` 

usually works

(I've never made a readme before lol)


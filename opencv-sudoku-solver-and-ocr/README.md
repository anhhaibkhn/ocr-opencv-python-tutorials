# How to solve Sudoku puzzles with OpenCV and OCR

The tutorial source can be found [here](https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/)

### Creating an automatic Sudoku puzzle solver with OpenCV is a 6-step process:

- Step #1: Provide input image containing Sudoku puzzle to our system.
- Step #2: Locate wherein the input image the puzzle is and extract the board.
- Step #3: Given the board, locate each of the individual cells of the Sudoku board (most standard - Sudoku puzzles are a 9×9 grid, so we’ll need to localize each of these cells).
- Step #4: Determine if a digit exists in the cell, and if so, OCR it.
- Step #5: Apply a Sudoku puzzle solver/checker algorithm to validate the puzzle.
- Step #6: Display the output result to the user.


### Some notes about this tutorial

- The SudokuNet model was failed when identifying the number 9 pic as 8. This leads to the failure in solving the sudoku table. 
- Adding the test_model.py to load, save, and rename the pre-trained models for testing some specific images. 
- The failed case was saved as the following name: "failed_9.png"
- The pre-trained model in this repo could identify correctly the failed case. See it in "opencv-sudoku-solver-and-ocr\output\pyimagesearch_sequential.h5". 

### How to run
See the initial comment section of each file for details. 

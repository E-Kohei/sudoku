# sudoku
This program can solve sudoku not only in n=3(9x9 sudoku) but also in general n.
But the order of the program is O(n^4), so it would takes much time to solve sudoku in large n.

How to read png file of sudoku in sudoku_reader.py

```python
path = "...\\sudoku.png"
npzfile = np.load("neural_network.npz")  ##
hidden_layer = npzfile['hidden_layer']   ##
output_layer = npzfile['output_layer']   ##
network = [hidden_layer, output_layer]   ## These four commands are involved in sudoku_reader .py
s = read_sudoku(network, path)
```

How to solve sudoku in sudoku_solver.py

```python
s = read_sudoku(network, path)
solve(s)
```

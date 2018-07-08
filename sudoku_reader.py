import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sudoku_solver import sudoku


def sigmoid(t):
    return 1 / (1 + np.exp(-t))

def neuron_output(weights, inputs):
    if weights.ndim == 2:
        return sigmoid(weights.dot(inputs))
    elif weights.ndim == 3:
        return sigmoid(np.tensordot(weights, inputs))

def add_bias(inputs):
    if inputs.ndim == 1:
        return np.array(inputs.tolist() + [1])
    elif inputs.ndim == 2:
        col = inputs.shape[1]
        return np.array(inputs.tolist() + [[1] + [0 for _ in range(col-1)]])

def feed_forward(neural_network, inputs):
    outputs = []
    for layer in neural_network:
        output = neuron_output(layer,add_bias(inputs))
        outputs.append(output)
        inputs = output
    return outputs

def coord_of_img(i,j,img):
    v = 30*i + 3*(i+1)
    h = 30*j + 3*(j+1)
    return img[v:v+30, h:h+30,:3]

def pixel_cluster(img):
    s = img.shape
    all_white = np.ones(s)
    all_black = np.zeros(s)
    d_to_white = np.sqrt(((img - all_white)**2).sum(axis=2))
    d_to_black = np.sqrt(((img - all_black)**2).sum(axis=2))
    return 0.1 * np.int8(d_to_black < d_to_white)

def predict(network, inp):
    return feed_forward(network, inp)[-1]

def read_sudoku(reader_network, png_file, size=9):
    img = mpimg.imread(png_file)
    s = list()
    for i in range(size):
        row = list()
        for j in range(size):
            digit_mtr = pixel_cluster(coord_of_img(i, j, img))
            spectorum = predict(reader_network, digit_mtr).tolist()
            digit = spectorum.index(max(spectorum))
            row.append(digit)
        s.append(row)
    
    return sudoku(s)        
            
if __name__ == "__main__":
    path = "sudoku.png"
    npzfile = np.load("neural_network.npz")
    hidden_layer = npzfile['hidden_layer']
    output_layer = npzfile['output_layer']
    network = [hidden_layer, output_layer]

    print(read_sudoku(network, path))

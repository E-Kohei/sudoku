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
        
def back_propagate(network, input_vector, targets, ite=10000):
    hidden_outputs, outputs = feed_forward(network, input_vector)

    output_deltas = outputs * (1 - outputs) * (outputs - targets)

    row = network[-1].shape[0]
    new_output_layer = network[-1] - \
                       output_deltas.reshape((row,1)) * add_bias(hidden_outputs)

    hidden_deltas = hidden_outputs * (1 - hidden_outputs) * \
                    output_deltas.dot(new_output_layer[:,:-1])

    row2 = network[0].shape[0]
    new_hidden_layer = network[0] - \
                       hidden_deltas.reshape((row2,1)) * add_bias(input_vector)
    network = [new_hidden_layer, new_output_layer]
    return network

def back_propagate2(network, input_matrix, targets):
    hidden_outputs, outputs = feed_forward(network, input_matrix)

    output_deltas = outputs * (1 - outputs) * (outputs - targets)

    row = network[-1].shape[0]
    new_output_layer = network[-1] - \
                       output_deltas.reshape((row,1)) * add_bias(hidden_outputs)

    hidden_deltas = hidden_outputs * (1 - hidden_outputs) * \
                    output_deltas.dot(new_output_layer[:,:-1])

    row2 = network[0].shape[0]
    new_hidden_layer = network[0] - \
                       np.tensordot(hidden_deltas, add_bias(input_matrix), axes=0)
    network = [new_hidden_layer, new_output_layer]
    return network

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

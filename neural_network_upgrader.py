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
        
def back_propagate(network, input_vector, targets):
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

def shifted_coord_of_img(i,j,img,dv=3,dh=3):
    v = 30*i + 3*(i+1)
    h = 30*j + 3*(j+1)
    return img[v+dv:v+dv+30, h+dh:h+dh+30,:3]

def black_or_white(rgb):
    d_to_white = np.sqrt(((rgb - np.ones(3))**2).sum())
    d_to_black = np.sqrt(((rgb - np.zeros(3))**2).sum())
    if d_to_white < d_to_black:
        return 0
    elif d_to_black < d_to_white:
        return 1
    else:
        return np.random.choice([0,1])

def pixel_cluster(img):
    s = img.shape
    all_white = np.ones(s)
    all_black = np.zeros(s)
    d_to_white = np.sqrt(((img - all_white)**2).sum(axis=2))
    d_to_black = np.sqrt(((img - all_black)**2).sum(axis=2))
    return 0.1 * np.int8(d_to_black < d_to_white)

def predict(network, inp):
    return feed_forward(network, inp)[-1]      
            

if __name__ == "__main__":
    path = 'sudoku.png'
    img = mpimg.imread(path)

    none = pixel_cluster(coord_of_img(8,8,img))
    one = pixel_cluster(coord_of_img(0,0,img))
    two = pixel_cluster(coord_of_img(1,0,img))
    three = pixel_cluster(coord_of_img(2,0,img))
    four = pixel_cluster(coord_of_img(3,0,img))
    five = pixel_cluster(coord_of_img(4,0,img))
    six = pixel_cluster(coord_of_img(5,0,img))
    seven = pixel_cluster(coord_of_img(6,0,img))
    eight = pixel_cluster(coord_of_img(7,0,img))
    nine = pixel_cluster(coord_of_img(8,0,img))

    targets = [np.array([1 if i==j else 0 for i in range(10)])
               for j in range(10)]

    ## 0,1 matrix input
    i1 = input('want back propagating?(0,1 matrix input)')
    if i1 == 'y' or i1 == 'yes':
        np.random.seed(0)
        inputs = [none, one, two, three, four, five, six, seven, eight, nine]
        network = [0.01*np.append(np.random.sample((30,30,30)),
                                  [np.array([np.append(np.array([1]),
                                                       np.zeros(29))
                                             for _ in range(30)])],
                                  axis=0)
                        .swapaxes(0,1),
                   0.01*np.random.sample((10,31))]
        print('back propagaing...')
        for k in range(10000):
            for input_vector, target_vector in zip(inputs, targets):
                network = back_propagate2(network, input_vector, target_vector)
        print('done!')
        for i, inp in enumerate(inputs):
            outputs = predict(network, inp)
            print(i, outputs.round(2))

    ## 0,1 vector input
    i2 = input('want back propagating?(0,1 vector input)')
    if i2 == 'y' or i2 == 'yes':
        none2 = none.flatten()
        one2 = one.flatten()
        two2 = two.flatten()
        three2 = three.flatten()
        four2 = four.flatten()
        five2 = five.flatten()
        six2 = six.flatten()
        seven2 = seven.flatten()
        eight2 = eight.flatten()
        nine2 = nine.flatten()
        np.random.seed(0)
        inputs2 = [none2, one2, two2, three2, four2, five2,
                   six2, seven2, eight2, nine2]
        network2 = [0.001*np.random.sample((30,901)),
                    0.001*np.random.sample((10,31))]
        print('back propagaing...')
        for k in range(10000):
            for input_vector, target_vector in zip(inputs2, targets):
                network2 = back_propagate2(network2, input_vector,
                                           target_vector)
        print('done!')
        for i, inp in enumerate(inputs2):
            outputs = predict(network2, inp)
            print(i, outputs.round(2))

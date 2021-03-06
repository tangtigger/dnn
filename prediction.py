import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import matplotlib
import scipy.optimize as opt
from sklearn.metrics import classification_report



## single logistic regression

# load data
def load_data(path, transpose=True):
    data = sio.loadmat(path)
    y = data.get('y')  # (5000,1)
    y = y.reshape(y.shape[0])  # make it back to column vector

    X = data.get('X')  # (5000,400)

    if transpose:
        # for this dataset, you need a transpose to get the orientation right
        X = np.array([im.reshape((20, 20)).T for im in X])

        # and I flat the image again to preserve the vector presentation
        X = np.array([im.reshape(400) for im in X])

    return X, y

# X, y = load_data('ex3data1.mat')
# print(X.shape)
# print(y.shape)



def plot_an_image(image):
#     """
#     image : (400,)
#     """
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.matshow(image.reshape((20, 20)), cmap=matplotlib.cm.binary)
    plt.xticks(np.array([]))  # just get rid of ticks
    plt.yticks(np.array([]))

# pick_one = np.random.randint(0, 5000)
# plot_an_image(X[pick_one, :])
# plot_an_image(raw_X[pick_one, :])

# plt.show()
# print('this should be {}'.format(y[pick_one]))

def plot_100_image(X):
    """ sample 100 image and show them
    assume the image is square

    X : (5000, 400)
    """
    size = int(np.sqrt(X.shape[1]))

    # sample 100 image, reshape, reorg it
    sample_idx = np.random.choice(np.arange(X.shape[0]), 100)  # 100*400
    sample_images = X[sample_idx, :]

    fig, ax_array = plt.subplots(nrows=10, ncols=10, sharey=True, sharex=True, figsize=(8, 8))

    for r in range(10):
        for c in range(10):
            ax_array[r, c].matshow(sample_images[10 * r + c].reshape((size, size)),
                                   cmap=matplotlib.cm.binary)
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))
            #plot function, generating 100 random pics

# plot_100_image(X)
# plt.show()
#
# raw_X, raw_y = load_data('ex3data1.mat')
# print(raw_X.shape)
# print(raw_y.shape)


# data preparation
# add intercept=1 for x0
# X = np.insert(raw_X, 0, values=np.ones(raw_X.shape[0]), axis=1) #insert a col with value 1


## y have 10 categories here. 1..10, they represent digit 0 as category 10 because matlab index start at 1
## I'll ditit 0, index 0 again
# y_matrix = []

# for k in range(1, 11):
#     y_matrix.append((raw_y == k).astype(int))

## last one is k==10, it's digit 0, bring it to the first position
# y_matrix = [y_matrix[-1]] + y_matrix[:-1]
# y = np.array(y_matrix)

# expand 5000*1 to 5000*10
#     e.g. y=10 -> [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]: ndarray
#     """
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def cost(theta, X, y):
    ''' cost fn is -l(theta) for you to minimize'''
    return np.mean(-y * np.log(sigmoid(X @ theta)) - (1 - y) * np.log(1 - sigmoid(X @ theta)))


def regularized_cost(theta, X, y, l=1):
    '''you don't penalize theta_0'''
    theta_j1_to_n = theta[1:]
    regularized_term = (l / (2 * len(X))) * np.power(theta_j1_to_n, 2).sum()

    return cost(theta, X, y) + regularized_term

def regularized_gradient(theta, X, y, l=1):
    '''still, leave theta_0 alone'''
    theta_j1_to_n = theta[1:]
    regularized_theta = (l / len(X)) * theta_j1_to_n

    # by doing this, no offset is on theta_0
    regularized_term = np.concatenate([np.array([0]), regularized_theta])

    return gradient(theta, X, y) + regularized_term

def gradient(theta, X, y):
    '''just 1 batch gradient'''
    return (1 / len(X)) * X.T @ (sigmoid(X @ theta) - y)

def logistic_regression(X, y, l=1):
    """generalized logistic regression
    args:
        X: feature matrix, (m, n+1) # with incercept x0=1
        y: target vector, (m, )
        l: lambda constant for regularization

    return: trained parameters
    """
    # init theta
    theta = np.zeros(X.shape[1])

    # train it
    res = opt.minimize(fun=regularized_cost,
                       x0=theta,
                       args=(X, y, l),
                       method='TNC',
                       jac=regularized_gradient,
                       options={'disp': True})
    # get trained parameters
    final_theta = res.x

    return final_theta


def predict(x, theta):
    prob = sigmoid(x @ theta)
    return (prob >= 0.5).astype(int)


# t0 = logistic_regression(X, y[0])
# t1 = logistic_regression(X, y[1])
#
#
# print(t0.shape)
# y_pred = predict(X, t0)
# y_pred1 = predict(X, t1)
# print('Accuracy={}'.format(np.mean(y[0] == y_pred)))
# print('Accuracy={}'.format(np.mean(y[1] == y_pred1)))
#
# # vectorized logistic regression
# k_theta = np.array([logistic_regression(X, y[k]) for k in range(10)])
# print(k_theta.shape)
#
# prob_matrix = sigmoid(X @ k_theta.T)
#
# prob_matrix = sigmoid(X @ k_theta.T)
# prob_matrix.shape
# np.set_printoptions(suppress=True)
# prob_matrix
#
# y_pred = np.argmax(prob_matrix, axis=1)
# y_answer = raw_y.copy()
# y_answer[y_answer==10] = 0
#
# print(classification_report(y_answer, y_pred))

# DNN model
def load_weight(path):
    data = sio.loadmat(path)
    return data['Theta1'], data['Theta2']
#
# theta1, theta2 = load_weight('ex3weights.mat')
#
# theta1.shape, theta2.shape
#
# X, y = load_data('ex3data1.mat',transpose=False)
#
# X = np.insert(X, 0, values=np.ones(X.shape[0]), axis=1)  # intercept
#
# X.shape, y.shape
#
# a1 = X
#
# z2 = a1 @ theta1.T # (5000, 401) @ (25,401).T = (5000, 25)
# z2.shape
# z2 = np.insert(z2, 0, values=np.ones(z2.shape[0]), axis=1)
#
# a2 = sigmoid(z2)
# a2.shape
# z3 = a2 @ theta2.T
# z3.shape
#
# a3 = sigmoid(z3)
# a3
#
# y_pred = np.argmax(a3, axis=1) + 1  # numpy is 0 base index, +1 for matlab convention???????????????axis?????????????????????axis=1?????????
# y_pred.shape
#
# print(classification_report(y, y_pred))

# logistic regression
if __name__ == '__main__':
    # plot 100 random pics from dataset, total 5,000 pics
    print('plot 100 random pics from dataset, total 5,000 pics')
    X, y = load_data('ex3data1.mat')
    plot_100_image(X)
    plt.show()

    # load data
    raw_X, raw_y = load_data('ex3data1.mat')

    # logistic regression
    print('logistic regression modeling')
    X = np.insert(raw_X, 0, values=np.ones(raw_X.shape[0]), axis=1) #insert a col with value 1

    # y have 10 categories here. 1..10, they represent digit 0 as category 10 because matlab index start at 1
    # I'll ditit 0, index 0 again
    y_matrix = []

    for k in range(1, 11):
        y_matrix.append((raw_y == k).astype(int))

    # last one is k==10, it's digit 0, bring it to the first position
    y_matrix = [y_matrix[-1]] + y_matrix[:-1]
    y = np.array(y_matrix)
    # expand y.shape from 5000*1 to 5000*10
    #     e.g. y=10 -> [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]: ndarray
    #     """

    k_theta = np.array([logistic_regression(X, y[k]) for k in range(10)])
    # print(k_theta.shape)

    prob_matrix = sigmoid(X @ k_theta.T)
    np.set_printoptions(suppress=True)
    # take the position which has largest probability for each row
    y_pred = np.argmax(prob_matrix, axis=1)

    y_answer = raw_y.copy()
    # digit 0 represent 10
    y_answer[y_answer == 10] = 0

    # output the accuracy report of logistic regression model
    print('Logistic regression accuracy report:')
    print(classification_report(y_answer, y_pred))
    print('Accuracy Matrix={}'.format(np.mean(y_answer == y_pred)))
    lr_accuracy = np.mean(y_answer == y_pred)


    print('\n\nDNN modeling with 2 layers, 25 and 10 nodes respectively')
    # load layers weights, 2 layers with 25 and 10 nodes respectively
    theta1, theta2 = load_weight('ex3weights.mat')

    print(f'theta of layer 1: {theta1.shape}\ntheta of layer 2: {theta2.shape}')
    # load data
    X_dnn, y_dnn = load_data('ex3data1.mat', transpose=False)

    X_dnn = np.insert(X_dnn, 0, values=np.ones(X_dnn.shape[0]), axis=1)  # intercept col with value 1
    # X.shape, y.shape

    a1 = X_dnn
    z2 = a1 @ theta1.T  # (5000, 401) @ (25,401).T = (5000, 25)
    # z2.shape
    z2 = np.insert(z2, 0, values=np.ones(z2.shape[0]), axis=1)
    a2 = sigmoid(z2)
    # a2.shape
    z3 = a2 @ theta2.T
    # z3.shape
    a3 = sigmoid(z3)
    # a3

    y_pred_dnn = np.argmax(a3, axis=1) + 1  # numpy is 0 base index, +1 for matlab convention
    # y_pred.shape
    print('DNN accuracy report:')
    print(classification_report(y_dnn, y_pred_dnn))
    print('Accuracy Matrix={}'.format(np.mean(y_dnn == y_pred_dnn)))
    dnn_accuracy = np.mean(y_dnn == y_pred_dnn)

    print('\n\nSummary:')
    if dnn_accuracy > lr_accuracy:
        print(f'The best performance model: DNN\nAccuracy: {dnn_accuracy}')
    else:
        print(f'The best performance model: logistic regression\nAccuracy: {lr_accuracy}')



















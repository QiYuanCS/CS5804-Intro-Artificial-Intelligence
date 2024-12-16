import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        score = self.run(x)
        return 1 if nn.as_scalar(score) >= 0 else -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        while True:
            no_mistakes = True
            for x, y in dataset.iterate_once(1):
                prediction = self.get_prediction(x)
                actual = nn.as_scalar(y)
                if prediction != actual:
                    no_mistakes = False
                    self.w.update(x, actual)
            if no_mistakes:
                break



class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):

        "*** YOUR CODE HERE ***"
        self.hidden_size = 512
        self.learning_rate = 0.02
        self.w1 = nn.Parameter(1, self.hidden_size)
        self.b1 = nn.Parameter(1, self.hidden_size)
        self.w2 = nn.Parameter(self.hidden_size, 1)
        self.b2 = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        hidden_layer = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        output_layer = nn.AddBias(nn.Linear(hidden_layer, self.w2), self.b2)
        return output_layer


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predictions = self.run(x)
        return nn.SquareLoss(predictions, y)



    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 200
        while True:
            for x, y in dataset.iterate_forever(batch_size):
                loss = self.get_loss(x, y)
                gradients = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2])
                self.w1.update(gradients[0], -self.learning_rate)
                self.b1.update(gradients[1], -self.learning_rate)
                self.w2.update(gradients[2], -self.learning_rate)
                self.b2.update(gradients[3], -self.learning_rate)
                if nn.as_scalar(loss) < 0.02:
                    return




class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        "*** YOUR CODE HERE ***"
        self.hidden_size = 200
        self.batch_size = 100
        self.learning_rate = 0.5
        self.weights1 = nn.Parameter(784, self.hidden_size)
        self.bias1 = nn.Parameter(1, self.hidden_size)
        self.weights2 = nn.Parameter(self.hidden_size, 10)
        self.bias2 = nn.Parameter(1, 10)


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        hidden_layer = nn.ReLU(nn.AddBias(nn.Linear(x, self.weights1), self.bias1))
        output_layer = nn.AddBias(nn.Linear(hidden_layer, self.weights2), self.bias2)
        return output_layer





    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predictions = self.run(x)

        return nn.SoftmaxLoss(predictions, y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_forever(self.batch_size):
                loss = self.get_loss(x, y)
                gradients = nn.gradients(loss, [self.weights1, self.bias1, self.weights2, self.bias2])
                self.weights1.update(gradients[0], -self.learning_rate)
                self.bias1.update(gradients[1], -self.learning_rate)
                self.weights2.update(gradients[2], -self.learning_rate)
                self.bias2.update(gradients[3], -self.learning_rate)

                if dataset.get_validation_accuracy() >= 0.975:
                    return


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.num_languages = 5

        self.hidden_size = 128
        self.learning_rate = 0.02

        self.W_x = nn.Parameter(self.num_chars, self.hidden_size)
        self.W_h = nn.Parameter(self.hidden_size, self.hidden_size)
        self.b = nn.Parameter(1, self.hidden_size)

        self.W_out = nn.Parameter(self.hidden_size, self.num_languages)
        self.b_out = nn.Parameter(1, self.num_languages)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.W_x), self.b))

        # Process subsequent characters:
        for i in range(1, len(xs)):
            x = xs[i]
            x_transformed = nn.Linear(x, self.W_x)
            h_transformed = nn.Linear(h, self.W_h)
            z = nn.Add(x_transformed, h_transformed)
            z = nn.AddBias(z, self.b)
            h = nn.ReLU(z)

        logits = nn.AddBias(nn.Linear(h, self.W_out), self.b_out)
        return logits

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        logits = self.run(xs)
        loss = nn.SoftmaxLoss(logits, y)
        return loss


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        max_epochs = 90
        current_epoch = 0

        while current_epoch < max_epochs:
            for xs, y in dataset.iterate_once(batch_size=256):
                loss = self.get_loss(xs, y)
                gradients = nn.gradients(loss, [self.W_x, self.W_h, self.b, self.W_out, self.b_out])

                self.W_x.update(gradients[0], -self.learning_rate)
                self.W_h.update(gradients[1], -self.learning_rate)
                self.b.update(gradients[2], -self.learning_rate)
                self.W_out.update(gradients[3], -self.learning_rate)
                self.b_out.update(gradients[4], -self.learning_rate)

            validation_accuracy = dataset.get_validation_accuracy()
            print(f"Epoch {current_epoch + 1}, Validation Accuracy: {validation_accuracy:.2f}")

            current_epoch += 1



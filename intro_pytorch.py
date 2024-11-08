import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms



def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    # Define a transform to normalize the data
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    # Download and load the training data
    dataset = datasets.FashionMNIST('./data', train=training, download=True, transform=transform)
    # Create a dataloader
    loader = torch.utils.data.DataLoader(dataset, batch_size=64)

    return loader



def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential (
        # Convert 2D image to 1D vector, because fully connected layers 
        # (dense layers) expect 1D vector
        nn.Flatten(),

        # Input: 28 * 28 image, Output: 128 Neurons
        # Linear Layer roles that the input is connected to the next layer
        # as fully connected layer (dense layer)
        nn.Linear(28 * 28, 128),

        # Activation Function (Rectified Linear Unit)
        # ReLU is a non-linear activation function that allows 
        # the model to learn complex patterns in the data
        nn.ReLU(),

        # Input: 128 Neurons, Output: 64 Neurons
        nn.Linear(128, 64),

        # Activation Function (ReLU)
        nn.ReLU(),

        # Input: 64 Neurons, Output: 10 Classes (Class number of FashionMNIST)
        nn.Linear(64, 10)
    )
    return model



def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    # Optimizer updates the weights of the model
    # SGD (Stochastic Gradient Descent)
    # lr: learning rate that controls the step size
    # momentum: a parameter that reflects a percentage of previous weight updates
    # to speed up optimization and reduce oscillation
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    # Set the model to training mode
    model.train()

    # Loop over the dataset T Epoch times
    for epoch in range(T):
        correct = 0
        total = 0
        running_loss = 0.0

        # Loop over for each batch
        for images, labels in train_loader:
            # Reset the gradients to zero
            opt.zero_grad()
            # Forward pass
            outputs = model(images)
            # Compute the loss
            loss = criterion(outputs, labels)
            # Backward pass (compute the gradients)
            loss.backward()
            # Update the weights
            opt.step()

            # Compute the accuracy
            # Predict the class with the highest probability
            _, predicted = torch.max(outputs, 1)
            # Compute the number of correct predictions
            correct += (predicted == labels).sum().item()
            # Update the total number of data
            total += labels.size(0)
            # Update the loss
            running_loss += loss.item()

        # Compute the average loss and accuracy
        accuracy = 100 * correct / total
        avg_loss = running_loss / len(train_loader)
        print(f"Train Epoch: {epoch}  Accuracy: {correct}/{total}({accuracy:.2f}%)  Loss: {avg_loss:.3f}")



def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    # Set the model to evaluation mode
    model.eval()
    correct = 0
    total = 0
    test_loss = 0.0

    # Disable gradient computation (not needed for evaluation)
    with torch.no_grad():
        # Loop over for each batch of the test set
        for data, labels in test_loader:
            # Forward pass (compute the predictions)
            outputs = model(data)
            # Compute the loss
            loss = criterion(outputs, labels)
            # Update the total loss
            test_loss += loss.item()

            # Predict the class with the highest probability
            _, predicted = torch.max(outputs, 1)
            # Compute the number of correct predictions
            correct += (predicted == labels).sum().item()
            # Update the total number of data
            total += labels.size(0)

    # Compute the average loss and accuracy
    avg_loss = test_loss / len(test_loader)
    accuracy = 100 * correct / total

    if show_loss:
        print(f"Average loss: {avg_loss:.4f}")
    print(f"Accuracy: {accuracy:.2f}%")
    


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  a tensor. test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    # Set the model to evaluation mode
    model.eval()

    # Disable gradient calculation for inference
    with torch.no_grad():
        # Get logits for all test images
        logits = model(test_images)
        # Calculate probabilities for the given index image using softmax
        prob = F.softmax(logits[index], dim=0)
        # Get top 3 probabilities and their class indices
        top3_prob, top3_indices = torch.topk(prob, 3)

        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']
        
        # Loop through the top 3 predictions
        for i in range(3):
            print(f"{class_names[top3_indices[i].item()]}: {top3_prob[i].item() * 100:.2f}%")



if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    # Loss function measures the difference between 
    # what the neural network predicts and the actual correct answer
    criterion = nn.CrossEntropyLoss()

    # Test get_data_loader()
    print("Test get_data_loader()")
    train_loader = get_data_loader()
    print(type(train_loader))
    print(train_loader.dataset)
    test_loader = get_data_loader(False)

    # Test build_model()
    print("\nTest build_model()")
    model = build_model()
    print(model)

    # Test train_model()
    print("\nTest train_model()")
    train_loader = get_data_loader(training=True)
    train_model(model, train_loader, criterion, 5)

    # Test evaluate_model()
    print("\nTest evaluate_model()")
    test_loader = get_data_loader(training=False)
    evaluate_model(model, test_loader, criterion, show_loss=True)

    # Test predict_label()
    print("\nTest predict_label()")
    test_images = next(iter(test_loader))[0]
    predict_label(model, test_images, 1)
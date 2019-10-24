# Author        :   <your name>
# Collaborators :   <your collaborators>
# Time spent    :   <total time>

# DO NOT CHANGE THESE LINES...
from math import sqrt

TRAINSET_PATH = '/Users/ruisun/Desktop/trainset.txt'
TESTSET_PATH = '/Users/ruisun/Desktop/testset.txt'
RESULT_PATH = '/Users/ruisun/Desktop/result.txt'


# ############################


def load_trainset(path):
    """
    :param path: a string which is the path to a text file which contains trainset data.
                 The lines in trainset data are employment information from a number of employees
                 and each line should be in the following format:

                 agi,age,stt,cat

                 Where agi is annual gross income, age is age, stt is the state in which the employee resides,
                 and cat is either 0, 1, or 2, where 0 means developer, 1 means scientist, and 2 means manager.

                 example: 110000,22,11,0
                          is the data for a developer who has 22 years and resides in state 11, and earns 110000
                          each year.

    :return :   read lines in trainset file and extract (agi,age,stt) from each line as a tuple of integers and append
                them to a list called train_points and append cat as an integer to another list called train_cats.
                return train_points, train_cats
    """

    train_points=[]
    train_cats=[]
    with open(path) as tr:
        for line in tr:
            splitted = line.split(',')
            train_points.append((int(splitted[0]), int(splitted[1]), int(splitted[2])))
            train_cats.append(int(splitted[3]))
        
        return train_points,train_cats



def load_testset(path):
    """
    :param path: a string which is the path to a text file which contains testset data.
                 The lines in testset data are employment information from a number of employees that we do not know
                 to what category they belong and each line should be in the following format:

                 agi,age,stt,k

                 Where agi is annual gross income, age is age, stt is the state in which the employee resides,
                 and k is an integer that we want to set as KNN algorithm parameter.

                 example: 110000,22,11,4
                          is the data for an employee who has 22 years and resides in state 11, and earns 110000
                          each year, and we want to run KNN with k=4 to predict his category.

    :return :   read lines in testset file and extract (agi,age,stt) from each line as a tuple of integers and append
                them to a list called test_points and append k as an integer to another list called Ks.
                return test_points, Ks
    """

    test_points = []
    Ks = []
    with open(path) as ts:
        for line in ts:
            splitted = line.split(',')
            test_points.append((int(splitted[0]), int(splitted[1]), int(splitted[2])))
            Ks.append(int(splitted[3]))
        return test_points,Ks


def knn(train_points, train_cats, test_points, Ks):
    """
    :param train_points: a list of tuples of integers, which are feature values for a number of training observations.

    :param train_cats  : a list of integers with the same size as train_points. train_cats[i] is the category
                         of the i'th training observation.

    :param test_points : a list of tuples of integers, which are feature values for a number of test observations.

    :param Ks          : a list of integers. For the i'th test observation KNN algorithm will be executed with k = Ks[i].

    :return            : a list of integers where each integer is either 0, 1, or 2. The i'th integer in this list is
                         the predicted category for the i'th test observation.
                         
    """
    result_categories=[]
    for i in range(len(test_points)):
        distances=get_distances_with_categories(train_points, train_cats, test_points[i])
        neighbors=get_nearest_neighbors(distances,Ks[i])
        frequence=get_category_frequencies(neighbors)
        category=find_most_frequent_category(frequence)
        result_categories.append(category)
    return result_categories
    


def get_distances_with_categories(train_points, train_cats, test_point):
    distances=[]
    """
    :param train_points: a list of tuples of integers, which are feature values for a number of training observations.

    :param train_cats  : a list of integers with the same size as train_points. train_cats[i] is the category
                         of the i'th training observation.

    :param test_point  : a tuple of integers, which is feature values for one test observation.

    :return            : a list of pairs called distances, where the i'th pair is a tuple like (d, c) where
                         d is the euclidean distance between train_points[i] and the given test_point, and
                         c is the category of the i'th observation which is train_cats[i].
    """

    for i in range(len(train_points)):
        
        distances.append((euclidean_distance(train_points[i],test_point),i))
    return distances


def euclidean_distance(p1, p2):
    """
    :param p1: a n-dimensional point.

    :param p2: a n-dimensional point.

    :return  : the euclidean distance between the two given points.
    """
    distance=0
  
   
    for i in range(len(p1)-1):
        distance(int(p1[i])-int(p2[i]))**2
    return sqrt(distance)


def get_nearest_neighbors(distances, k):
    """
    :param distances: a list of pairs of numbers like (d,c).

    :param k        : the number of nearest neighbors that this function returns.

    :return         : first sort the given distances based on d in (d,c), then return
                      the first k elements in it.
    """

   
    distances.sort()
    return distances[:k]
    


def get_category_frequencies(neighbors):
    """
    :param neighbors: a list of pairs where each pair is a tuple like (d, c), where d is a measured distance,
                      and c is a category which can have any immutable type!

    :return         : a dictionary where keys are the categories that have appreared in neighbors list,
                      and values are their frequency in that list.
    """


    
    dictionary={}
    for i in range(len(neighbors)):
        if train_cats[neighbors[i][1]] not in dictionary:
            dictionary[train_cats[neighbors[i][1]]]=1
        else:
            dictionary[train_cats[neighbors[i][1]]]+=1
            
                
            
    return dictionary

def find_most_frequent_category(freqs):
    """
    :param freqs: a dictionary between categories and their frequencies.

    :return     : the key which is associated with the max value in the given dictionary.
                  if there are more than one key with max value, return that key which has
                  the least order.
    """
    mx = max(freqs.values())
    for key in sorted(freqs.keys()):
        if freqs[key] == mx:
            return key


def write_results(path, result_list):
    """
    write each element in the result_list on one line of the file which has the given path.

    :param path       : a path to the file that we want to write the results in.

    :param result_list: a list of elements where each element represents a category.

    :return           : Nothing
    """
    
    with open(path, 'w') as res:
        for cat in result_list:
            res.write(f'{cat}\n')
    


# DO NOT CHANGE THESE LINES ##################################
if __name__ == "__main__":
    train_points, train_cats = load_trainset(TRAINSET_PATH)
    test_points, Ks = load_testset(TESTSET_PATH)

    result_list = knn(train_points, train_cats, test_points, Ks)

    write_results(RESULT_PATH, result_list)
# #############################################################

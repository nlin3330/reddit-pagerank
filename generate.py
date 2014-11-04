from getData import data
import matplotlib.pyplot as plt
import numpy as np
import operator

markov_data2 = {} ## dictionary with non-key subreddits discarded
keys = data.keys()

## Sets up normalized data for weighted markov chains where the values of the values in
## markov_data dictionary is the probability of moving to that particular state
for key, value in data.items():
    temp2 = {}
    num_subs2 = sum(value.values())
    for k, v in value.items():
        if k not in keys:
            num_subs2 -= v
    for k, v in value.items():
        if k in keys:
            temp2[k] = v/float(num_subs2)
    markov_data2[key] = temp2

#calculates the eigenvector of the steady state distribution

def eigenvector(dictionary):
    ret = {}
    #creating matrix for calculating eigenvector
    matrix = []
    for k in keys:
        temp_matrix = []
        temp_keys = dictionary[k].keys()
        for key in keys:
            if key not in temp_keys:
                temp_matrix += [0]
            else:
                temp_matrix += [dictionary[k][key]]

        matrix += [temp_matrix]

    #calculating eigenvalue
    mat = np.matrix(matrix)
    trans_mat = mat.T
    eig_vals, eig_vec = np.linalg.eig(trans_mat)
    eig_vec = eig_vec.T
    real_vec = eig_vec[0]
    state = 0
    sum = 0
    for _ in range(401):
        sum += abs(real_vec[0,_])
    #normalizing eigenvector needed
    for k in keys:
        ret[k] = abs(real_vec[0,state])/sum
        state += 1
    return ret
#dictionary with keys and steady-state distribution
eigen_dict = eigenvector(markov_data2)
## check the probability of the markov states sum to 1

def checksum(dictionary):
    for k in dictionary.keys():
        print(sum(dictionary[k].values()))

# Histogram of top 10 reddits, plus Berkeley and Stanford

count = {}
for reddit in markov_data2.values():
    for link in reddit.keys():
        if link not in count.keys():
            count[link] = 0
        count[link] += reddit[link]
topReddits = sorted(count.items(), key=operator.itemgetter(1))[len(count) - 10:len(count)]
ticks = []
vals = []
for pair in topReddits:
    ticks.append(pair[0])
    vals.append(pair[1])
ticks += ['berkeley', 'stanford']
vals += [count['berkeley'], count['stanford']]
plt.bar(range(len(vals)), vals, align='center')
plt.xticks(range(len(ticks)), ticks)
plt.title('Most Popular Subreddits')
plt.show()


import numpy as np

def divide_vector(vector, x=100, take_mean=False):
    """ divides vector into x equal-sized segments. Remainders get added to the final segment """
    if x <= 0:
        raise ValueError("Number of segments (x) must be greater than 0")
    segment_size = len(vector) // x
    segments = []
    for i in range(x):
        start = i * segment_size
        end   = (i + 1) * segment_size
        segments.append(vector[start:end])
    # handle any remaining elements if vector length is not perfectly divisible by x
    if len(vector) % x !=0:
        segments[-1] = np.hstack((segments[-1], (vector[x * segment_size:])))
    # optionally take the mean of each segment
    if take_mean:
        segments = [i.mean() for i in segments]
    return segments

# divide_vector(np.arange(30), 4, take_mean=True)

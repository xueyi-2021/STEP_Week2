import numpy, sys, time

if (len(sys.argv) != 2):
    print("usage: python %s N" % sys.argv[0])
    quit()

n = int(sys.argv[1])
a = numpy.zeros((n, n)) # Matrix A
b = numpy.zeros((n, n)) # Matrix B
c = numpy.zeros((n, n)) # Matrix C

# Initialize the matrices to some values.
for i in range(n):
    for j in range(n):
        a[i, j] = i * n + j
        b[i, j] = j * n + i
        c[i, j] = 0


begin = time.time()

######################################################
# Write code to calculate C = A * B                  #
# (without using numpy librarlies e.g., numpy.dot()) #
######################################################

#1回だけの時間がかなり不安定なので10回の平均値にした
#N>=100は長すぎるので1回に戻した
if n >=100:
    n_times = 1
else:
    n_times = 10
for _ in range(n_times):
    for i in range(n):
        for j in range(n):
            #c[i, j] = 0
            for k in range(n):
                    c[i, j] += a[i, k] * b[k, j]

end = time.time()
print("time: %.6f sec" % ((end - begin)/n_times))


# Print C for debugging. Comment out the print before measuring the execution time.
total = 0
for i in range(n):
    for j in range(n):
        # print c[i, j]
        total += c[i, j]
# Print out the sum of all values in C.
# This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
print("sum: %.6f" % total)
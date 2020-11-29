#based on Numberphile's YouTube video 
def persistence(n,steps=0):
    if len(str(n)) == 1:
        return (print ("{} STEPS".format(steps)))
    digits = [int(i) for i in str(n)]
    result = 1
    for j in digits:
        result *= j
    print(result)
    steps += 1
    persistence(result, steps)

if __name__ == '__main__':
    persistence(277777788888899)

combo = ["1,2,3,4", "1,2,3,4,50", "qwerty1,2,3"]
result = []
def total_sum(masiv):
    return sum(int(x) for x in masiv.split(","))

for i in combo:
    try:
        print(total_sum(i))
    except ValueError:
        print("Не можу це зробити!")
import multiprocessing
import time

def factorize_0(number):
    result = []
    for i in range(1, number + 1):
        if number % i == 0:
            result.append(i)
    return result

def synchronous_factorize(numbers):
    start_time = time.time()
    results = [factorize(num) for num in numbers]
    end_time = time.time()
    execution_time = end_time - start_time
    oll_results=[]
    count=0
    for i in results:
        oll_results.append(f'{numbers[count]}: {results[count]}')
        count+=1
    print(f'time synchronous: {execution_time}')
    print('\n'.join(oll_results))


def factorize(number):
    result = []
    for i in range(1, number + 1):
        if number % i == 0:
            result.append(i)
    return result

def multipro(numbers):
    processes=multiprocessing.cpu_count()
    start_time=time.time()
    with multiprocessing.Pool(processes) as pool:
        result=pool.map(factorize,numbers)
    end_time = time.time()
    difference=start_time-end_time
    oll_results = []
    count = 0
    for i in result:
        oll_results.append(f'{numbers[count]}: {result[count]}')
        count+=1
    print(f'time multipro: {difference}')
    print('\n'.join(oll_results))

if __name__ == '__main__':
    synchronous_factorize([128, 255, 99999, 10651060])
    print('-----------------------------------------')
    multipro([128, 255, 99999, 10651060])



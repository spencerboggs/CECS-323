import csv
import sys

try:
    id = int(input('Enter your ID: '))
except ValueError:
    print('Invalid ID')
    sys.exit(1)

def read_csv():
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        data = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                data.append(row)
                line_count += 1
        return data
    
def sort_data(data):
    data.sort(key=lambda x: x[1], reverse=True)
    return data

def validate_id(data, id):
    for i in range(len(data)):
        if int(data[i][0]) == id:
            return True
    return False
        
def find_min(data, id):
    for i in range(len(data)):
        if int(data[i][0]) == id:
            return data[i][2], data[i][3]
        
def find_mean(data):
    total = 0
    for i in range(len(data)):
        total += float(data[i][1])
    return round(total / len(data), 2)
        
def print_table(data):
    print(f'{"Rank":<10}{"ID":<10}{"Points":<10}{"Min A":<10}{"Min B":<10}')
    for i in range(len(data)):
        if i == 9 or i == 18:
            print('-' * 50)
        if int(data[i][0]) == id:
            print(f'\033[92m{i + 1:<10}{"You":<10}{data[i][1]:<10}{data[i][2]:<10}{data[i][3]:<10}\033[0m')
        else:
            print(f'{i + 1:<10}{data[i][0]:<10}{data[i][1]:<10}{data[i][2]:<10}{data[i][3]:<10}')
        
def main():
    data = read_csv()
    if not validate_id(data, id):
        print('ID not found')
        sys.exit(1)
    data = sort_data(data)
    min_A, min_B = find_min(data, id)
    print_table(data)
    print(f'Minimum points for an A: {min_A}')
    print(f'Minimum points for a B: {min_B}')
    print(f'Mean score: {find_mean(data)}')


if __name__ == '__main__':
    main()

#user:pwd
file_dict = {}

# file => dict
def read_file():
        with open('user.txt') as f:
                for line in f.read().split('\n'):
                        if line:
                                temp = line.split(':')
                                file_dict[temp[0]] = temp[1]


# dict => file
def write_file():
        file_arr = []
        for user,pwd in file_dict.items():
                file_arr.append('%s:%s'%(user,pwd))

        with open('user.txt','w') as f:
                f.write('\n'.join(file_arr))

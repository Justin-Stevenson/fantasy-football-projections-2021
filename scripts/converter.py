import json

def read_json_from_file(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def filter_data_by_position(data, position):
    return filter(lambda x: x['pos'] == position, data)

def write_json_to_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def get_filname(position):
    return position.lower() + '.json'

def handle_position(data, position):
    position_data = filter_data_by_position(data=data, position=position)
    filename = get_filname(position)
    write_json_to_file(data=position_data, filename=filename)

def do_all():
    data = read_json_from_file('all.json')
    handle_position(data=data, position='QB')
    handle_position(data=data, position='RB')
    handle_position(data=data, position='WR')
    handle_position(data=data, position='TE')
    handle_position(data=data, position='K')
    handle_position(data=data, position='DST')

do_all()

# def do_it():
#     data = read_json_from_file('all.txt')
#     print(data[0])

# do_it()
        
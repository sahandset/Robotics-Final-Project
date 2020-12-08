from flask import Flask
from flask import session
from flask import request


app = Flask(__name__)

app.secret_key = '\x118 \xf0\x8e\x9f-J\x03^^\x01\xe7\xdci/8Lj8\x95D@|'


coord_list = []
target_list = []
target_dict = {}


def mapping(robot_coords, target_coords):
    # Initialize empty dictionary
    my_dictionary = {}
    # Ensures that we have enough robots to make our shape
    if (len(robot_coords) == len(target_coords)):
        for i in range(len(robot_coords)):
            # Populate Dictionary
            my_dictionary[robot_coords[i]] = target_coords[i]

    # Return Dictionary
    return my_dictionary


@app.route("/post_coordinates", methods=['POST'])
def post_coordinates():
    global coord_list
    coords = eval(request.form['coordinates'])
    coord_list.append(coords)
    session['coords'] = coords
    print("New Robot Found\n")
    print("Coordinate List for All Robots:")
    print(coord_list)
    return 'coords saved'


@app.route("/get_target", methods=['GET'])
def get_target():
    global target_dict, target_list, coord_list

    print(session)

    if 'coords' not in session:
        print('Current robot coords unknown')
        return 'Current robot coords unknown'

    coords = session['coords']
    if not target_dict:

        if len(target_list) == len(coord_list):
            target_dict = mapping(coord_list, target_list)
            target = target_dict[coords]

            # old coords,mapping irrelevant
            del session['coords']
            coord_list.remove(coords)
            del target_dict[coords]

            return str(target)
        else:
            print('Number of robot coordinates not the same as number of targets')
            return 'Number of robot coordinates not the same as number of targets'
    else:
        target = target_dict[coords]

        del session['coords']
        coord_list.remove(coords)
        del target_dict[coords]
        return str(target)


@app.route("/post_target", methods=['POST'])
def post_target():
    global target_list
    target_list = list(eval(request.form['target']))
    print("Targets:")
    print(target_list)
    return "targets_saved"


if __name__ == '__main__':
    app.run()

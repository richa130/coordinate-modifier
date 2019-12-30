import math


def get_coordinates_from_file(file_name):
    handle_name = open(file_name)
    original_coordinates = []
    origin = []
    counter = 0
    for line in handle_name:
        if counter == 0:
            counter = counter + 1
            continue
        s = line.split(',')
        if counter == 1:
            origin = [float(s[4]), float(s[5])]
        original_coordinates.append([float(s[2]), float(s[3])])
        counter = counter + 1
    handle_name.close()
    return original_coordinates, origin


def scale_coordinates(coordinate_array, scale):
    new_coordinate_array = []
    for coordinate in coordinate_array:
        x, y = coordinate
        x = round((x * scale), 1)
        y = round((y * scale), 1)
        new_coordinate_array.append([x, y])
    return new_coordinate_array


def polar_to_cartesian(coordinate, origin):
    cartesian_coordinate = []
    radius = coordinate[0]
    theta = coordinate[1]
    theta_radians = math.radians(theta)
    x = round(radius * math.cos(theta_radians), 1)
    y = round(radius * math.sin(theta_radians), 1)
    cartesian_coordinate.append(x + origin[0])
    cartesian_coordinate.append(y + origin[1])
    return cartesian_coordinate


def cartesian_to_polar(coordinate, origin):
    polar_coordinate = []
    a = abs(coordinate[0] - origin[0])
    b = abs(coordinate[1] - origin[1])
    radius = round(math.sqrt(pow(a, 2) + pow(b, 2)), 1)
    if a == 0:
        if b > 0:
            theta = 90
        if b < 0:
            theta = 270
    elif b == 0:
        if a > 0:
            theta = 360
        if a < 0:
            theta = 180
    else:
        theta = round(math.degrees(math.asin(b/radius)), 1)
    polar_coordinate.append(radius)
    polar_coordinate.append(theta)
    return polar_coordinate


def rotate_coordinates(coordinate_array, origin, degrees):
    new_coordinate_array = []
    for coordinate in coordinate_array:
        polar_coord = cartesian_to_polar(coordinate, origin)
        rotated_polar_coord = [polar_coord[0], (polar_coord[1] + degrees)]
        rotated_cartesian_coord = polar_to_cartesian(rotated_polar_coord, origin)
        new_coordinate_array.append(rotated_cartesian_coord)
    return new_coordinate_array


def rotate_and_scale_coordinates(coordinate_array, origin, degrees, scale):
    scaled_coordinates = scale_coordinates(coordinate_array, scale)
    new_coordinate_array = rotate_coordinates(scaled_coordinates, origin, degrees)
    return new_coordinate_array


def create_new_file(scaled, rotated, rotated_and_scaled):
    handle_name = open("./original_coordinates.csv")
    handle_name2 = open("./modified_coordinates.csv", 'w')
    for_loop = 0
    counter = 0
    for line in handle_name:
        if counter == 0:
            s = line.split(',')
            new_s = []
            for string in s:
                new_s.append(string.strip())

            headers = ["X scaled", "Y scaled", "X rotated", "Y rotated", "X rotated and scaled", "Y rotated and scaled"]
            new_s.extend(headers)
            print(new_s)
            s1 = ','.join(new_s)
            print(s1)
            handle_name2.write(s1)
            handle_name2.write("\n")
            counter = counter + 1
            continue
        else:
            s = line.split()
            x_scaled = str(scaled[for_loop][0])
            y_scaled = str(scaled[for_loop][1])
            x_rotated = str(rotated[for_loop][0])
            y_rotated = str(rotated[for_loop][1])
            x_rotated_and_scaled = str(rotated_and_scaled[for_loop][0])
            y_rotated_and_scaled = str(rotated_and_scaled[for_loop][1])
            array = [x_scaled, y_scaled, x_rotated, y_rotated, x_rotated_and_scaled, y_rotated_and_scaled]
            s.extend(array)
           # print(s)
            s1 = ','.join(s)
            handle_name2.write(s1)
            handle_name2.write("\n")
            for_loop = for_loop + 1


def main():
    original_coordinates, origin = get_coordinates_from_file("./original_coordinates.csv")
    scale = eval(input("Enter a number you would like the coordinates to be scaled by: "))
    degrees = eval(input("Enter the how many degrees you would like the coordinates to be rotated by: "))
    scaled_coordinates = scale_coordinates(original_coordinates, scale)
    rotated_coordinates = rotate_coordinates(original_coordinates, origin, degrees)
    rotated_and_scaled_coordinates = rotate_and_scale_coordinates(original_coordinates, origin, degrees, scale)
    '''print(original_coordinates)
    print(scaled_coordinates)
    print(rotated_coordinates)
    print(rotated_and_scaled_coordinates)'''
    create_new_file(scaled_coordinates, rotated_coordinates, rotated_and_scaled_coordinates)


if __name__ == '__main__':
    main()

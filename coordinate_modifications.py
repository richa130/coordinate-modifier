import math


def get_coordinates_from_file(file_name):
    """Get coordinate data from file.

    Args:
        file_name (str): path/filename.ext

    Returns:
        orginal_coordinates (list): 2D Array of all coordinates
        origin (list): 2D Array with len 1 of origin
    """
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
    """Scale a coordinate by a factor x

    Args:
        coordinate_array (list): 2D Array of coordinates
        scale (int): scaling factor

    Returns:
        new_coordinate_array (list): 2D Array of scaled coordinates
    """
    new_coordinate_array = []
    for coordinate in coordinate_array:
        x, y = coordinate
        x = round((x * scale), 1)
        y = round((y * scale), 1)
        new_coordinate_array.append([x, y])
    return new_coordinate_array


def polar_to_cartesian(coordinate, origin):
    """Convert a polar coordinate to cartesian

    Args:
        coordinate (list): 2D Array of a single coordinate in polar form
        origin (list): 2D Array of a single origin coordinate

    Returns:
        cartesian_coordinate (list): 2D Array of cartesian coordinate
    """
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
    """Convert a cartesian coordinate to polar

    Args:
        coordinate (list): 2D Array of a single coordinate
        origin (list): 2D Array of a single origin coordinate

    Returns:
        polar_coordinate (list): 2D Array of polar coordinate
    """
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
    """Rotate coordinates from the origin by x degrees

    Args:
        coordinate_array (list): 2D Array of coordinates
        origin (list): 2D Array of a single origin coordinate
        degrees (int): Angle of rotation

    Returns:
        new_coordinate_array (list): 2D Array of scaled coordinates
    """
    new_coordinate_array = []
    for coordinate in coordinate_array:
        polar_coord = cartesian_to_polar(coordinate, origin)
        rotated_polar_coord = [polar_coord[0], (polar_coord[1] + degrees)]
        rotated_cartesian_coord = polar_to_cartesian(rotated_polar_coord, origin)
        new_coordinate_array.append(rotated_cartesian_coord)
    return new_coordinate_array


def rotate_and_scale_coordinates(coordinate_array, origin, degrees, scale):
    """Scale and Rotate coordinates from the origin by x degrees by y scaling factor

    Args:
        coordinate_array (list): 2D Array of coordinates
        origin (list): 2D Array of a single origin coordinate
        degrees (int): Angle of rotation
        scale (int): Scaling factor

    Returns:
        new_coordinate_array (list): 2D Array of scaled and rotated coordinates
    """
    scaled_coordinates = scale_coordinates(coordinate_array, scale)
    new_coordinate_array = rotate_coordinates(scaled_coordinates, origin, degrees)
    return new_coordinate_array


def create_new_file(scaled, rotated, rotated_and_scaled):
    """Write coordinates to a file

    Args:
        scaled (list): 2D Array of scaled coordinates
        rotated (list): 2D Array of rotated coordinates
        rotated_and_scaled (list): 2D Array of rotated and scaled coordinates

    Returns:
        None
    """
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
    """Main"""
    original_coordinates, origin = get_coordinates_from_file("./original_coordinates.csv")
    scale = eval(input("Enter a number you would like the coordinates to be scaled by: "))
    degrees = eval(input("Enter the how many degrees you would like the coordinates to be rotated by: "))
    scaled_coordinates = scale_coordinates(original_coordinates, scale)
    rotated_coordinates = rotate_coordinates(original_coordinates, origin, degrees)
    rotated_and_scaled_coordinates = rotate_and_scale_coordinates(original_coordinates, origin, degrees, scale)
    create_new_file(scaled_coordinates, rotated_coordinates, rotated_and_scaled_coordinates)


if __name__ == '__main__':
    main()

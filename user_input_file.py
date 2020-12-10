square = 'square'
triangle = 'triangle'
circle = 'circle'
shape = {
    square: [(0.5,1.5), (0.75,1.5), (1,1.5), (1.25,1.5), (1.5,1.5), (1.5,1.25), (1.5,1), (1.5,0.75), (1.5,0.5), (1.25,0.5), (1,0.5), (0.75,0.5), (0.5,0.5), (0.5,0.75), (0.5,1), (0.5,1.25)],
    triangle: [(1,1.5), (1.15,1.25), (1.25,1), (1.375,0.75), (1.5,0.5), (1.375,0.5), (1.25,0.5), (.875,0.5), (1,0.5), (0.875,0.5), (0.75,0.5), (0.625,0.5), (0.5,0.5), (0.625,0.75), (0.75,1), (0.875,1.25)],
    circle: [(1,1.5), (1.15,1.5), (1.35,1.35), (1.5,1.15), (1.5,1), (1.5,0.85), (1.35,0.65), (1.15,0.5), (1,0.5), (0.85,0.5), (0.65,0.65), (0.5,0.85), (0.5,1), (0.5,1.15), (0.65,1.35), (0.85,1.5)]
}

user_shape = input('Please type in a shape: ').split()[0].lower()

while user_shape not in shape.keys():
    print('Shape requested is not available (available shapes: Square, Circle, Triangle)' + '\n')
    continue_ = input('Would you like to try again? (y/n): ')
    if continue_.lower() == 'y':
        user_shape = input('Please type in a shape: ').split()[0].lower()
    else:
        break

# TODO Send shape[user_shape] to server 
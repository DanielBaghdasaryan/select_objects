import sys
from utils import *
from time import time


def select_objects(
        data, RA, DEC, FOV_H, FOV_V, N, ra_col, dec_col, mag_col
):
    # Add angular distance to the data
    objects = [[*x, dist(RA, DEC, deg_to_rad(x[ra_col]), deg_to_rad(x[dec_col]))] for x in data[1:]]

    # Filter by distance above Pi / 2, objects in opposite side
    objects = [x for x in objects if x[-1] < pi / 2]

    # Select objects inside FOV
    objects = [x for x in objects if inside_fov(RA, DEC, deg_to_rad(x[ra_col]), deg_to_rad(x[dec_col]), FOV_H, FOV_V)]

    # Select top brightest ones
    indices = sorted_indices([(i, float(x[mag_col] or 0)) for i, x in enumerate(objects)])[::-1]
    objects = [objects[i] for i in indices][:N]

    # Sort objects by distance
    indices = sorted_indices([(i, float(x[-1])) for i, x in enumerate(objects)])
    objects = [objects[i] for i in indices]
    return objects


if __name__ == '__main__':
    # Read Data
    filename = None
    if len(sys.argv) == 1:
        print('Please provide .tsv file name:')
        filename = input().strip()
    else:
        filename = sys.argv[1]

    with open(filename, 'r') as f:
        data = [x.split('\t') for x in f.read().split('\n')][1:-1]

    id_col = data[0].index('source_id')
    ra_col = data[0].index('ra_ep2000')
    dec_col = data[0].index('dec_ep2000')
    mag_col = data[0].index('phot_g_mean_mag')

    # Get params
    RA, DEC, FOV_H, FOV_V, N = None, None, None, None, None

    while RA is None:
        try:
            print('Input RA of the center of FOV (default 0):')
            ra = float(input().strip() or 0)
            assert -90 <= ra <= 90
            RA = deg_to_rad(ra)
            print(f'RA: {ra}')
        except:
            print('Only float numbers from (-90, 90) are accepted')

    while DEC is None:
        try:
            print('Input DEC of the center of FOV (default 0):')
            dec = float(input().strip() or 0)
            assert 0 <= dec < 360
            DEC = deg_to_rad(dec)
            print(f'DEC: {dec}')
        except:
            print('Only float numbers from (0, 360) are accepted')

    while FOV_H is None:
        try:
            print('Input horizontal field of view (rad, default Pi/2):')
            fov_h = float(input().strip() or pi / 2)
            assert 0 < fov_h <= pi / 2
            FOV_H = fov_h / 2
            print(f'FOV_H: {fov_h} rad')
        except:
            print('Only float numbers from (0, Pi / 2) are accepted')

    while FOV_V is None:
        try:
            print('Input vertical field of view (rad, default Pi/2):')
            fov_v = float(input().strip() or pi / 2)
            assert 0 < fov_v <= pi / 2
            FOV_V = fov_v / 2
            print(f'FOV_V: {fov_v} rad')
        except:
            print('Only float numbers from (0, Pi / 2) are accepted')

    while N is None:
        try:
            print('Input number of top brightest objects, default 10:')
            N = int(input().strip() or 10)
            assert N > 0
            print(f'N: {N}')
        except:
            print('Only positive integer numbers are accepted')

    # Select objects
    objects = select_objects(data, RA, DEC, FOV_H, FOV_V, N, ra_col, dec_col, mag_col)

    # Save CSV
    objects = [['ID', 'RA', 'DEC', 'Brightness (mag)', 'Distance (rad)']] + [
        [x[id_col], x[ra_col], x[dec_col], x[mag_col], x[-1]] for x in objects
    ]
    objects = '\n'.join([','.join([str(y) for y in x]) for x in objects])
    output_fn = f'{round(time())}.csv'
    with open(f'{round(time())}.csv', 'w') as f:
        f.write(objects)
    print(f'\nFile {output_fn} was successfully created')

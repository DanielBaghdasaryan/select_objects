# Select brightest objects inside rectangular field of view

Usage

``get_brightest.py 337.all.tsv``

Replace `337.all.tsv` with your filename. The prompt will require to input 

1. RA
2. DEC
3. FOV_H (rad)
4. FOV_V (rad)
5. N: number of top brightest objects we want to save

`<timestamp>.csv` file will be created with cols:

'ID', 'RA', 'DEC', 'Brightness (mag)', 'Distance (rad)'

sorted by distance from the center of FOV


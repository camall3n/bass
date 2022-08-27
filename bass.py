import numpy as np
import random

from fretboard import Fretboard

# from chords import Chord
# c = Chord.random(seventh='7')
# print(f'\'{c.name()}\': {c.notes()}')
# import sys; sys.exit()

staff_str = """
a       e       i       m       q       u       y       θ        |
|   c   |   g   |   k   |   o   |   s   |   w   |   ζ   |   𝜀   *|
| 𝛽 | d | f | h | j | l | n | p | r | t | v | x | z | 𝛿 | λ | 𝜅 *|
|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|__|
1       2       3       4       5       6       7       8"""
note_positions = 'a𝛽cdefghijklmnopqrstuvwxyzζ𝛿θλ𝜀𝜅'
notes_str = ' '.join(note_positions) + ' '

n_notes = 14
shuffled_positions = np.random.permutation(list(note_positions))
beats = shuffled_positions[:n_notes]
rests = shuffled_positions[n_notes:]

staff_beats = staff_str
for position in beats:
    staff_beats = staff_beats.replace(position, 'X')
for position in rests:
    replacement = '|' if position in 'aeimquyθ' else ' '
    staff_beats = staff_beats.replace(position, replacement)

chords = {
    # 'Gm7': ['G', 'Bb', 'D', 'F'],
    # 'G7sus4': ['G', 'C', 'D', 'F'],
    # 'Dm7': ['D', 'F', 'A', 'C'],
    # 'Am7': ['A', 'C', 'E', 'G'],
    # 'Bb7': ['Bb', 'D', 'F', 'Ab'],
    'C7b5': ['C', 'E', 'Gb', 'Bb'],
}

chord = random.choice(list(chords.keys()))
notes = np.random.choice(chords[chord], n_notes)

note_annotations = notes_str
for note, position in zip(notes, beats):
    pattern = position + ' ' if len(note) == 2 else position
    note_annotations = note_annotations.replace(pattern, note)
for position in rests:
    note_annotations = note_annotations.replace(position, ' ')

print()
print(chord)
print(note_annotations, end='')
print(staff_beats)
print()

# print(Fretboard.from_notes(chords[chord]))

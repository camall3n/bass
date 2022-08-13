import numpy as np
import random

staff_str = """
a       e       i       m       q       u       y       𝛾        |
|   c   |   g   |   k   |   o   |   s   |   w   |   𝛼   |   𝜀   *|
| b | d | f | h | j | l | n | p | r | t | v | x | z | 𝛽 | 𝛿 | 𝜅 *|
|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|__|
1       2       3       4       5       6       7       8"""
note_positions = 'abcdefghijklmnopqrstuvwxyz𝛼𝛽𝛾𝛿𝜀𝜅'
notes_str = ' '.join(note_positions)

n_notes = 14
shuffled_positions = np.random.permutation(list(note_positions))
beats = shuffled_positions[:n_notes]
rests = shuffled_positions[n_notes:]

staff_beats = staff_str
for position in beats:
    staff_beats = staff_beats.replace(position, 'X')
for position in rests:
    replacement = '|' if position in 'aeimquy𝛾' else ' '
    staff_beats = staff_beats.replace(position, replacement)

chords = {
    # 'Gm7': ['G', 'B♭', 'D', 'F'],
    # 'G7sus4': ['G', 'C', 'D', 'F'],
    # 'Dm7': ['D', 'F', 'A', 'C'],
    'Am7': ['A', 'C', 'E', 'G'],
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

from __future__ import annotations
from dataclasses import dataclass

from scales import chromatic_scale

_fretboard_ascii = """
================================================================================================================
  ||     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
G ||G#/Ab|--A--|A#/Bb|--B--|--C--|C#/Db|--D--|D#/Eb|--E--|--F--|F#/Gb|--G--|G#/Ab|--A--|A#/Bb|--B--|--C--|C#/Db|
  ||     |     |     |     |     |     |     |     |     |     |     |  ●  |     |     |     |     |     |     |
D ||D#/Eb|--E--|--F--|F#/Gb|--G--|G#/Ab|--A--|A#/Bb|--B--|--C--|C#/Db|--D--|D#/Eb|--E--|--F--|F#/Gb|--G--|G#/Ab|
  ||     |     |  ●  |     |  ●  |     |  ●  |     |  ●  |     |     |     |     |     |  ●  |     |  ●  |     |
A ||A#/Bb|--B--|--C--|C#/Db|--D--|D#/Eb|--E--|--F--|F#/Gb|--G--|G#/Ab|--A--|A#/Bb|--B--|--C--|C#/Db|--D--|D#/Eb|
  ||     |     |     |     |     |     |     |     |     |     |     |  ●  |     |     |     |     |     |     |
E ||--F--|F#/Gb|--G--|G#/Ab|--A--|A#/Bb|--B--|--C--|C#/Db|--D--|D#/Eb|--E--|--F--|F#/Gb|--G--|G#/Ab|--A--|A#/Bb|
  ||     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
================================================================================================================
  ||              ●           ●           ●           ●                ● ●                ●           ●
"""

@dataclass
class Fretboard:
    _ascii : str = _fretboard_ascii

    def __str__(self):
        return(self._ascii)

    @classmethod
    def from_notes(cls, notes : list) -> Fretboard:
        ascii = cls._ascii
        frets = []
        for note in notes:
            for note_name in chromatic_scale:
                if note == note_name:
                    fret = f'--{note}--'
                    break
                if len(note) > 1 and note in note_name:
                    ascii = ascii.replace(note_name, f'--{note}-')
                    fret = f'--{note}-'
                    break
            frets.append(fret)
            
        for note in chromatic_scale:
            pattern = f'--{note}--' if len(note) == 1 else note
            if pattern not in frets:
                ascii = ascii.replace(pattern, '-----')
            for open_string in ['E', 'A', 'D', 'G']:
                if open_string not in notes:
                    ascii = ascii.replace(open_string + ' ', '  ')
    
        return Fretboard(ascii)

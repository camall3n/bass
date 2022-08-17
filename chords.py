from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from multiprocessing.sharedctypes import Value

import numpy as np

@dataclass
class Chord:
    """Class for keeping track of musical keys"""
    root: str
    third: str = '' # '' / 'm' / 'sus' (major/minor/suspended)
    fifth: str = '' # '' / 'aug' / 'dim' (normal/augmented/diminished)
    seventh: str = '' # '7' / 'maj7' / '6' / '' (minor/major/6th/none)
    others: list = field(default_factory=list)

    def name(self) -> str:
        chord = self.root
        if self.third != 'sus':
            chord += self.third
        chord += self.fifth
        if self.third == 'm' and self.seventh == 'maj7':
            chord += '(maj7)'
        else:
            chord += self.seventh
        if self.third == 'sus':
            chord += 'sus'
        if self.third == 'm' or self.seventh in ['7', 'maj7']:
            if self.fifth == 'aug':
                chord = chord.replace('aug', '') + '#5' # move '#5' to end
            elif self.fifth == 'dim':
                chord = chord.replace('dim', '') + 'b5' # move 'b5' to end
        return chord

    def _uses_flats(self):
        if self.third == 'm' and self.root in ['D', 'G', 'C', 'F', 'Bb', 'Eb']:
            return True
        elif self.third in ['', 'sus'] and self.root in ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']:
            return True
        return False
    
    def _uses_sharps(self):
        if (self.root + self.third) in ['Cm', 'A']:
            return False
        return not self._uses_flats()

    def tones(self) -> list:
        tones = ['R']

        if self.third == '':
            tones.append('3')
        elif self.third == 'm':
            tones.append('m3')
        else:
            # sus
            pass
        
        if self.fifth == '':
            tones.append('5')
        elif self.fifth == 'aug':
            tones.append('#5')
        else: # dim
            tones.append('b5')
        
        if self.seventh == '6':
            tones.append('6')
        elif self.seventh == '7':
            tones.append('m7')
        elif self.seventh == 'maj7':
            tones.append('7')
        else:
            pass

        return tones

    def notes(self):
        tones = self.tones()
        tone_names = ['R', 'b2', '2', 'm3', '3', '4', 'b5', '5', '#5', '6', 'm7', '7']
        semitones = [tone_names.index(tone) for tone in tones]
        
        chromatic_scale = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']
        for root_idx, note_name in enumerate(chromatic_scale):
            if self.root == note_name:
                break
            if len(self.root) > 1 and self.root in note_name:
                break

        notes_ = []
        for semitone in semitones:
            note_idx = (root_idx + semitone) % 12
            note_name = chromatic_scale[note_idx]
            if '/' in note_name:
                if self._uses_sharps():
                    note = note_name[:2]
                else:
                    note = note_name[-2:]
            else:
                note = note_name
            notes_.append(note)
        
        return notes_


    @classmethod
    def parse(cls, name:str) -> Chord:
        # peel off the root
        rest = name
        root, rest = name[0], name[1:]
        if rest and rest[0] in ['b', '#']:
            root, rest = (root + rest[0]), rest[1:]

        # collect multi-character keywords
        keywords = ['aug', 'sus', 'dim', 'maj7', '#5', 'b5']
        found_keywords = []
        for word in keywords:
            if word in rest:
                found_keywords.append(word)
                rest = rest.replace(word, '')
        
        # determine the third
        if 'sus' in found_keywords:
            if 'm' in rest:
                raise ValueError('Chord cannot be minor and sus')
            third = 'sus'
            found_keywords.remove('sus')
        elif 'm' in rest:
            third = 'm'
            rest = rest.replace('m', '')
        else:
            third = ''
                
        # determine the seventh
        if 'maj7' in found_keywords:
            if any(_7th in rest for _7th in ['7', '6']):
                raise ValueError('Chord cannot have multiple 7ths')
            seventh = 'maj7'
            found_keywords.remove('maj7')
        elif '7' in rest:
            if '6' in rest:
                raise ValueError('Chord cannot have multiple 7ths')
            seventh = '7'
            rest = rest.replace('7', '')
        elif '6' in rest:
            seventh = '6'
            rest = rest.replace('6', '')
        else:
            seventh = ''

        # determine the fifth
        if len(found_keywords) > 1:
            raise ValueError('Chord cannot have multiple 5ths')
        elif len(found_keywords) == 1:
            fifth = found_keywords[0]
            if '#' in fifth:
                fifth = 'aug'
            if 'b' in fifth:
                fifth = 'dim'
        else:
            fifth = ''
        
        rest = rest.replace('()', '')

        if rest != '':
            raise ValueError(f'Unknown chord name: {name}')
        
        return Chord(root, third, fifth, seventh)

    @classmethod
    def random(cls, root=None, third=None, fifth=None, seventh=None):
        if third is None:
            third = np.random.choice(['', 'm', 'sus'], p=[.45, .45, .1])
        if root is None:
            if third == '':
                keys = ['C', 'G', 'F', 'D', 'Bb', 'A', 'Eb', 'E', 'Ab']
                odds = [9, 7, 7, 5, 5, 3, 3, 1, 1.]
            elif third == 'm':
                keys = ['A', 'E', 'D', 'B', 'G', 'F#', 'C', 'C#', 'F']
                odds = [9, 7, 7, 5, 5, 3, 3, 1, 1.]
            else:
                keys = ['G', 'D', 'A', 'C', 'F', 'E', 'Bb', 'B']
                odds = [4, 4, 3, 3, 2, 2, 1, 1.]
            odds = np.array(odds)
            root = np.random.choice(keys, p=odds/odds.sum())
        if fifth is None:
            fifth = np.random.choice(['', 'dim', 'aug'], p=[0.8, 0.15, 0.05])
        if seventh is None:
            seventh = np.random.choice(['7', 'maj7', '6', ''])
        
        return Chord(root, third, fifth, seventh)

def test():
    for chord in [
        'Cm7',
        'Abmaj7',
        'Dm6',
        'Ebdim',
        'Gaug6',
        'Bb7#5',
        'C7b5',
    ]:
        print('Testing', chord)
        assert Chord.parse(chord).name() == chord
    
    print()
    np.random.seed(0)
    n_random_chords = 1000
    root = defaultdict(int)
    third = defaultdict(int)
    fifth = defaultdict(int)
    seventh = defaultdict(int)
    print(f'Randomly generating {n_random_chords} chords...')
    for _ in range(n_random_chords):
        chord = Chord.random()
        chord_name = chord.name()
        print(chord_name, '.', sep='', end='')
        assert Chord.parse(chord_name).name() == chord_name
        root[chord.root] += 1
        third[chord.third] += 1
        fifth[chord.fifth] += 1
        seventh[chord.seventh] += 1

    print()
    print('Stats:')
    for note in [root, third, fifth, seventh]:
        print(sorted(note.items()))

    print('All tests passed')

if __name__=='__main__':
    test()

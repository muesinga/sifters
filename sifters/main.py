from modules.textures import *
from modules import *

def main():
    
    midifile = dataset.Dataset('sentimental.mid')
    dataframe = midifile.calculate_start_value(midifile.midi_messages)
    # dataframe = midifile.extract_chords(dataframe)
    # data = data.midi_to_pitch_class(data)
    # data = data.extract_single_occurrences(data)
    # data = data.chords_to_sieves(data)

    # sieves = data.iloc[6:7]['Sieves'].tolist()
    dataframe.to_csv('data/csv/dataframe.csv')
    
    # sieves = ['((8@0|8@1|8@7)&(5@1|5@3))', '((8@0|8@1|8@2)&5@0)', '((8@5|8@6)&(5@2|5@3|5@4))', '(8@6&5@1)', '(8@3)', '(8@4)', '(8@1&5@2)']
    
    # textures = {

    #     # 'np1': nonpitched.NonPitched(sieves),
    #     # 'np2': nonpitched.NonPitched(sieves, '2/3'),
    #     'mono1': monophonic.Monophonic(sieves),
    #     'mono2': monophonic.Monophonic(sieves, '2/3'),

    # }   
    
    # output = score.Score(**textures)
    
    # output.combine_parts('mono1', 'mono2')
    
    # output.write_midi()
    
if __name__ == '__main__':
    main()


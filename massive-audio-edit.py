from os import listdir
from shutil import copy2

participants = {
  '1': {
    'origin': 'ES',
    'group': '2',
    'condition': '1'
  },
  '2': {
    'origin': 'ES',
    'group': '2',
    'condition': '2'
  },
  '3': {
    'origin': 'ES',
    'group': '1',
    'condition': '1'
  },
  '4': {
    'origin': 'ES',
    'group': '2',
    'condition': '1'
  },
  '5': {
    'origin': 'ES',
    'group': '1',
    'condition': '2'
  }
}

filelist = sorted([x for x in listdir('corpus/') if x.endswith('.WAV')])

count = 1
participant_id = 1
for wav in filelist:
   if count == 4:
     participant_id += 1
     count = 1
  audio_info = {
    'filename': wav.rstrip('.WAV'),
    'participant_id': str(participant_id),
    'participant_origin': participants[str(participant_id)]['origin'],
    'participant_group': participants[str(participant_id)]['group'],
    'participant_cond': participants[str(participant_id)]['condition']
  }

  copy2(f'{audio_info["filename"]}.WAV', f'format_files/{"_".join(audio_info.values())}.WAV')
  count += 1
  

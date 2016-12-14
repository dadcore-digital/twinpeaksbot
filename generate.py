import codecs, os, re
from datetime import datetime, timedelta

MEDIA_DIR = '/Users/ianfitzpatrick/Downloads/misc/tps2'
SHOW = 'tp'
SEASON = '02'
EPISODE = '01'
OUTPUT_DIR = '%s/media' % os.getcwd()
TEMP_DIR = '%s/media/temp' % os.getcwd()

class Scene:
    def __init__(self, show, season, episode, start, duration, text):
        self.show = show
        self.season = season
        self.episode = episode
        self.start = start
        self.duration = duration
        self.text = text

    def split_video(self, filetype, input_dir, output_dir):
        filename = '%ss%se%s-%s.mp4' % (self.show, self.season, self.episode, self.start.replace(':','_').replace('.','_'))
        cmd = 'ffmpeg -ss %s -i "%s/%ss%se%s.%s" -y -t %s -c:v libx264 -c:a libvo_aacenc %s/temp/%s' % (self.start, input_dir, self.show, self.season, self.episode, filetype, self.duration, output_dir, filename )
        os.system(cmd)
        return cmd

    def create_ass_file(self, output_dir, template='template.ass'):
        tfull = '%s/%s' % (os.getcwd(), template) 
        t = codecs.open(tfull,"r", "utf-8").read()
        t = t.replace('STARTTIME', '00:00:00.00')
        t = t.replace('ENDTIME', self.duration)
        t = t.replace('SUBTITLETEXT', str(self.text))

        file_out = '%s/%ss%se%s-%s.ass' % (output_dir, self.show, self.season, self.episode, self.start.replace(':','_').replace('.','_'))
        ass_file = open(file_out, "w")
        ass_file.write(t.encode('utf-8'))

    def create_gif(self, input_dir, output_dir, colors='256', resize='317:-1', compress='80'):
        file_in = '%ss%se%s-%s' % (self.show, self.season, self.episode, self.start.replace(':','_').replace('.','_'))
        file_out = '%s/%ss%se%s-%s.gif' % (output_dir, self.show, self.season, self.episode, self.start.replace(':','_').replace('.','_'))
        cmd = "gifify %s/%s.mp4 -o %s --colors %s --resize %s --compress %s --subtitles %s/%s.ass" % (input_dir, file_in, file_out, colors, resize, compress, input_dir, file_in)
        os.system(cmd)
        return cmd

def parse_srt(media_dir, show, season, episode):
    filename = '%s/%ss%se%s.srt' % (media_dir, show, season, episode)
    subs = codecs.open(filename,"r", "utf-8").read()
    subs = subs.replace('\r', '')
    subs = subs.split('\n\n')
    
    scene_list = []

    for entry in subs:
        r = re.search('(\d\d:\d\d:\d\d,\d{1,3}) --> (\d\d:\d\d:\d\d,\d{1,3})', entry)

        if r:
            start = r.group(1).replace(',','.')
            end = r.group(2).replace(',','.')
            FMT = '%H:%M:%S.%f'

            tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
            
            # No crazy long scenes
            if tdelta.seconds < 15:

                dur_s = '0%s' % tdelta.seconds
                dur_ms = str(tdelta.microseconds)[::2]
                duration = '00:00:%s.%s' % (dur_s, dur_ms)            

                text = str(entry.split(r.group(2))[1])
                text = text.lstrip('\n')
                text = text.replace('\n', '\\n')

                kwargs = {
                            'show': show,
                            'season': season,
                            'episode': episode,
                            'start': start,
                            'duration': duration,
                            'text': text
                         }
                scene_list.append(Scene(**kwargs))
    return scene_list

def make_those_gifs():
    episodes = ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '17', '18', '19', '20', '21']
    
    for e in episodes:
        s = parse_srt(MEDIA_DIR, SHOW, '02', e)
        
        for item in s:
            item.split_video('mp4', MEDIA_DIR, OUTPUT_DIR)
            item.create_ass_file(TEMP_DIR, 'template.ass')
            item.create_gif(TEMP_DIR, OUTPUT_DIR)

make_those_gifs()



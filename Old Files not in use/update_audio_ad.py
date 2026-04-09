"""
update_audio.py
===============
Run this in your  C:\\Users\\Dj4be\\Desktop\\New Bulgarian  folder.

Replaces the TTS speech engine in every day HTML file with a clean
MP3 player that loads your Google-generated audio files from the
/audio/ directory on your server.

- Tries MP3 first (your real recordings)
- Falls back to TTS silently if an MP3 is missing
- Removes eSpeak (no more loading that 500KB library)
- Speed buttons still work on MP3 playback

Usage:
  1. Drop this file into your New Bulgarian folder
  2. Double-click it
  3. Upload all the .html files to your server via FTP
"""

import os, re

FOLDER = os.path.dirname(os.path.abspath(__file__))

NEW_AUDIO_JS = '''<script>
(function(){
  var currentAudio = null;
  var currentBtn   = null;
  var rate = parseFloat(localStorage.getItem('ttsRate') || '1');

  function setActive(r) {
    document.querySelectorAll('.tts-speed').forEach(function(b) {
      b.classList.toggle('is-active', parseFloat(b.dataset.rate) === r);
    });
  }
  setActive(rate);

  function makeFilename(text) {
    return text
      .replace(/\\./g, '')
      .replace(/,/g, '')
      .replace(/ /g, '_')
      .toLowerCase()
      .substring(0, 25) + '.mp3';
  }

  function stopAll() {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
    if (currentBtn) {
      var ctrl = currentBtn.closest('.audio-controls');
      if (ctrl) ctrl.classList.remove('is-playing');
      currentBtn.classList.remove('is-playing');
      currentBtn = null;
    }
    if ('speechSynthesis' in window) speechSynthesis.cancel();
  }

  function ttsSpeak(text, phonetic, onDone) {
    if (!('speechSynthesis' in window)) { onDone(); return; }
    var voices = speechSynthesis.getVoices();
    var bgVoice = null;
    for (var i = 0; i < voices.length; i++) {
      if (/^bg/i.test(voices[i].lang) || /bulgar/i.test(voices[i].name)) {
        bgVoice = voices[i]; break;
      }
    }
    var u = new SpeechSynthesisUtterance(bgVoice ? text : phonetic);
    if (bgVoice) u.voice = bgVoice;
    u.rate  = rate;
    u.onend = onDone;
    u.onerror = onDone;
    speechSynthesis.speak(u);
  }

  function playBtn(btn) {
    stopAll();
    currentBtn = btn;
    var ctrl = btn.closest('.audio-controls');
    if (ctrl) ctrl.classList.add('is-playing');
    btn.classList.add('is-playing');

    var pageName = window.location.pathname.split('/').pop().split('.')[0] || 'day01';
    var text     = btn.dataset.text     || '';
    var phonetic = btn.dataset.phonetic || text;
    var mp3Path  = 'audio/' + pageName + '/' + makeFilename(text);

    function done() {
      if (ctrl) ctrl.classList.remove('is-playing');
      btn.classList.remove('is-playing');
      if (currentBtn === btn) { currentBtn = null; currentAudio = null; }
    }

    var audio = new Audio(mp3Path);
    audio.playbackRate = rate;
    audio.play().then(function() {
      currentAudio = audio;
      audio.onended = done;
      audio.onerror = done;
    }).catch(function() {
      currentAudio = null;
      ttsSpeak(text, phonetic, done);
    });
  }

  document.addEventListener('click', function(e) {
    var spdBtn  = e.target.closest('.tts-speed');
    var playBtn2 = e.target.closest('.play-audio');
    var stopBtn  = e.target.closest('.stop-audio');
    if (spdBtn) {
      rate = parseFloat(spdBtn.dataset.rate);
      localStorage.setItem('ttsRate', String(rate));
      setActive(rate);
      if (currentAudio) currentAudio.playbackRate = rate;
    }
    if (playBtn2) playBtn(playBtn2);
    if (stopBtn)  stopAll();
  });

})();
</script>'''

# Matches the entire old TTS script block
TTS_PATTERN = re.compile(
    r'<script>\s*\(function\(\)\{\s*if \(!.*?speechSynthesis.*?\}\)\(\);\s*</script>',
    re.DOTALL
)

html_files = sorted([f for f in os.listdir(FOLDER)
                     if re.match(r'day\d+\.html$', f) or f == 'index.html'])

if not html_files:
    print('No day HTML files found in this folder.')
    input('Press Enter to close.')
    raise SystemExit

fixed = skipped = already = 0

for fname in html_files:
    path = os.path.join(FOLDER, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already updated
    if 'makeFilename' in content:
        print('  skipped  ' + fname + '  (already updated)')
        already += 1
        continue

    if not TTS_PATTERN.search(content):
        print('  WARNING  ' + fname + '  (no TTS script found)')
        skipped += 1
        continue

    # Replace TTS with MP3 player
    content = TTS_PATTERN.sub(NEW_AUDIO_JS, content, count=1)

    # Remove eSpeak tags (no longer needed)
    content = re.sub(
        r'<script>window\.espeakngWorkerUrl=[^<]+</script>\s*', '', content)
    content = re.sub(
        r'<script defer src="https://cdn\.jsdelivr\.net/espeakng[^"]+"></script>\s*', '', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  FIXED    ' + fname)
    fixed += 1

print('')
print('Done.  ' + str(fixed) + ' fixed,  ' + str(already) + ' already updated,  ' + str(skipped) + ' warnings.')
print('')
input('Press Enter to close.')

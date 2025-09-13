// Q&A Intake page logic
(function(){
  const synth = window.speechSynthesis;
  let availableVoices = [];

  function loadVoices() {
    try { availableVoices = synth.getVoices() || []; } catch { availableVoices = []; }
  }
  loadVoices();
  if (typeof speechSynthesis !== 'undefined' && 'onvoiceschanged' in speechSynthesis) {
    speechSynthesis.onvoiceschanged = loadVoices;
  }

  let recog = null;
  if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    recog = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recog.lang = 'en-US';
    recog.interimResults = false;
    recog.maxAlternatives = 1;
    try { window.recog = recog; } catch {}
  }

  function pickVoiceForLang(targetLang) {
    if (!availableVoices || availableVoices.length === 0) return null;
    const exact = availableVoices.find(v => (v.lang || '').toLowerCase() === targetLang.toLowerCase());
    if (exact) return exact;
    const starts = availableVoices.find(v => (v.lang || '').toLowerCase().startsWith(targetLang.split('-')[0].toLowerCase()));
    return starts || null;
  }

  const questions_en = [
    { prompt: "What's your full name, please?", field: "name" },
    { prompt: "How young are you?", field: "age" },
    { prompt: "What's your gender?", field: "gender" },
    { prompt: "Can I have your phone number?", field: "contact" },
    { prompt: "And where do you live?", field: "address" },
    { prompt: "Do you have any past or current medical conditions you'd like to share?", field: "medicalHistory" },
    { prompt: "What's bothering you the most right now?", field: "chiefComplaint" },
    { prompt: "On a scale of 1 to 10, how much pain are you feeling?", field: "painLevel" },
    { prompt: "Can you describe your pain for me?", field: "painDescription" },
    { prompt: "Are you experiencing any other symptoms?", field: "additionalSymptoms" },
    { prompt: "Who should we contact in case of emergency? Full name, please.", field: "emergencyName" },
    { prompt: "What's their relationship to you?", field: "emergencyRelation" },
    { prompt: "What's their gender?", field: "emergencyGender" },
    { prompt: "What's their phone number?", field: "emergencyContact" },
    { prompt: "And their address, if you have it?", field: "emergencyAddress" }
  ];

  const questions_hi = [
    { prompt: "कृपया अपना पूरा नाम बताएं।", field: "name" },
    { prompt: "आपकी उम्र क्या है?", field: "age" },
    { prompt: "आपका लिंग क्या है?", field: "gender" },
    { prompt: "कृपया अपना फ़ोन नंबर बताएं।", field: "contact" },
    { prompt: "आप कहाँ रहते हैं?", field: "address" },
    { prompt: "क्या आपके पास कोई पुरानी या वर्तमान चिकित्सा स्थिति है जो आप साझा करना चाहेंगे?", field: "medicalHistory" },
    { prompt: "इस समय आपको सबसे अधिक क्या परेशानी है?", field: "chiefComplaint" },
    { prompt: "1 से 10 के पैमाने पर, आपको कितना दर्द हो रहा है?", field: "painLevel" },
    { prompt: "कृपया अपने दर्द का वर्णन करें।", field: "painDescription" },
    { prompt: "क्या आपको अन्य कोई लक्षण हो रहे हैं?", field: "additionalSymptoms" },
    { prompt: "आपातकाल की स्थिति में हमें किससे संपर्क करना चाहिए? पूरा नाम बताएं।", field: "emergencyName" },
    { prompt: "उनका आपके साथ क्या संबंध है?", field: "emergencyRelation" },
    { prompt: "उनका लिंग क्या है?", field: "emergencyGender" },
    { prompt: "उनका फ़ोन नंबर क्या है?", field: "emergencyContact" },
    { prompt: "और उनका पता?", field: "emergencyAddress" }
  ];

  function getActiveQuestions() {
    const lang = sessionStorage.getItem('qa_lang') || 'en';
    return (lang === 'hi') ? questions_hi : questions_en;
  }

  function setDisplayIfExists(elementId, text) {
    const el = document.getElementById(elementId);
    if (el) el.innerText = text;
  }

  function speakChunked(text, callback) {
    const chunks = text.match(/[^.!?]+[.!?]*/g) || [text];
    let i = 0;
    (function next(){
      if (i < chunks.length) {
        const utter = new SpeechSynthesisUtterance(chunks[i].trim());
        const lang = (sessionStorage.getItem('qa_lang') || 'en') === 'hi' ? 'hi-IN' : 'en-US';
        utter.lang = lang;
        const v = pickVoiceForLang(lang);
        if (v) utter.voice = v;
        utter.rate = 1.0; utter.pitch = 1.0; utter.volume = 1.0;
        utter.onend = () => { i++; next(); };
        synth.speak(utter);
      } else {
        if (callback) callback();
      }
    })();
  }

  function listen(onSuccess, onFailure) {
    if (!recog) { if (onFailure) onFailure(); return; }
    recog.start();
    recog.onresult = e => {
      const answer = e.results[0][0].transcript;
      if (answer && answer.trim() !== "") {
        if (onSuccess) onSuccess(answer);
      } else { if (onFailure) onFailure(); }
    };
    recog.onerror = () => { if (onFailure) onFailure(); };
  }

  let index = 0;
  window.interviewStarted = false;

  function ask() {
    const use = getActiveQuestions();
    if (index < use.length) {
      const q = use[index];
      setDisplayIfExists('questionDisplay', q.prompt);
      speakChunked(q.prompt, () => {
        setTimeout(() => {
          listen(
            answer => {
              const el = document.getElementById(q.field);
              if (el) el.innerText = answer;
              setDisplayIfExists('answerDisplay', answer);
              index++;
              ask();
            },
            () => {
              const lang = sessionStorage.getItem('qa_lang') || 'en';
              const retry = (lang === 'hi') ? 'मुझे समझ नहीं आया, कृपया दोहराएँ।' : "I didn't catch that. Could you please repeat?";
              speakChunked(retry, () => ask());
            }
          );
        }, 100);
      });
    } else {
      const lang = sessionStorage.getItem('qa_lang') || 'en';
      const msg1 = (lang === 'hi') ? 'कृपया अब सेंसर पर अपना हाथ रखें।' : 'Please place your hand on the sensor now.';
      const msg2 = (lang === 'hi') ? 'पंजीकरण पूरा हुआ। अब मैं आपकी फोटो लूँगा।' : 'Registration complete. Now I will take your picture.';
      speakChunked(msg1, () => {
        speakChunked(msg2, () => { captureAndSubmit(); });
      });
    }
  }

  function captureAndSubmit() {
    const store = id => sessionStorage.setItem('qa_' + id, document.getElementById(id)?.innerText || '');
    ["name","age","gender","contact","address","medicalHistory","chiefComplaint","painLevel","painDescription","additionalSymptoms","emergencyName","emergencyRelation","emergencyGender","emergencyContact","emergencyAddress"].forEach(store);

    fetch('/take_picture')
      .then(res => res.json())
      .then(data => { if (data && data.status === 'success' && data.filename) sessionStorage.setItem('qa_photo', data.filename); })
      .catch(() => ({}))
      .finally(() => { window.location.href = "/patient_reviw"; });
  }

  window.start = function () {
    index = 0;
    window.interviewStarted = true;
    ask();
  };
})();




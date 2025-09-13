// Core Text-To-Speech utilities shared across pages
// Exposes: window.stopSpeaking and window.AppCore.speak

(function(){
    let currentSpeech = null;

    async function speak(text) {
        try {
            if (currentSpeech && 'speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                currentSpeech = null;
            }
            const response = await fetch('/speak', {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text })
            });
            if (!response.ok) throw new Error('Backend TTS failed');
            currentSpeech = { source: 'backend', text };
            return await response.json();
        } catch (error) {
            if ('speechSynthesis' in window) {
                return new Promise(resolve => {
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.onend = () => { currentSpeech = null; resolve(); };
                    utterance.onerror = () => { currentSpeech = null; resolve(); };
                    window.speechSynthesis.speak(utterance);
                    currentSpeech = { source: 'browser', utterance };
                });
            }
            return Promise.resolve();
        }
    }

    function stopSpeaking() {
        if (currentSpeech && 'speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            currentSpeech = null;
        }
    }

    window.stopSpeaking = stopSpeaking;
    window.AppCore = Object.assign({}, window.AppCore || {}, { speak });
})();




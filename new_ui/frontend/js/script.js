// Get references to key DOM elements 
const qaForm = document.getElementById('qa-form'); 
const videoSection = document.getElementById('video-answer-section'); 
const loadingSpinner = document.getElementById('loading-spinner'); 
const videoPlayer = document.getElementById('answer-video'); 
const captionText = document.getElementById('caption-text'); 
const sourceList = document.getElementById('source-lectures-list'); 

// Centralized object to manage caption state and logic
const captionManager = {
    captions: [],
    activeCaptionSpan: null,

    parseSrtContent(srtContent) {
        const lines = srtContent.split('\n\n').filter(line => line.trim() !== '');
        this.captions = lines.map(line => {
            const parts = line.split('\n');
            const timeString = parts[1];
            const text = parts.slice(2).join(' ').trim();
            const [startTimeStr, endTimeStr] = timeString.split(' --> ');

            const parseTime = (timeStr) => {
                const [hours, minutes, rest] = timeStr.split(':');
                const [seconds, milliseconds] = rest.split(',');
                return parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseInt(seconds) + parseInt(milliseconds) / 1000;
            };

            return {
                start: parseTime(startTimeStr),
                end: parseTime(endTimeStr),
                text: text
            };
        });
    },

    displayCaptions() {
        captionText.innerHTML = '';
        this.captions.forEach((caption, index) => {
            const span = document.createElement('span');
            span.textContent = caption.text + ' ';
            span.dataset.index = index;
            captionText.appendChild(span);
        });
        this.activeCaptionSpan = null; // Reset the active span
    },

    highlightCaption(currentTime) {
        // Find the current caption using a simple find loop
        const currentCaption = this.captions.find(
            caption => currentTime >= caption.start && currentTime < caption.end
        );

        const newActiveSpan = currentCaption ?
            captionText.querySelector(`span[data-index="${this.captions.indexOf(currentCaption)}"]`) :
            null;

        // If a new caption is found and it's different from the current one
        if (newActiveSpan && newActiveSpan !== this.activeCaptionSpan) {
            // Un-highlight the old one
            if (this.activeCaptionSpan) {
                this.activeCaptionSpan.classList.remove('caption-highlight');
            }
            // Highlight the new one
            newActiveSpan.classList.add('caption-highlight');
            this.activeCaptionSpan = newActiveSpan;
            newActiveSpan.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else if (!newActiveSpan && this.activeCaptionSpan) {
            // If no caption is active, un-highlight the previous one
            this.activeCaptionSpan.classList.remove('caption-highlight');
            this.activeCaptionSpan = null;
        }
    },

    reset() {
        this.captions = [];
        this.activeCaptionSpan = null;
        captionText.innerHTML = 'Captions will appear here.';
        sourceList.innerHTML = '';
    }
};

// Event listener for form submission 
qaForm.addEventListener('submit', async (e) => { 
    e.preventDefault(); 
     
    videoSection.classList.add('hidden'); 
    loadingSpinner.classList.remove('hidden'); 
    captionManager.reset(); // Reset the manager state before a new request

    const question = document.getElementById('question-input').value; 
    console.log(`Question submitted: ${question}`); 

    try {
        const response = await fetch('/generate-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        loadingSpinner.classList.add('hidden'); 
        videoSection.classList.remove('hidden'); 
         
        videoPlayer.src = data.videoUrl;
        videoPlayer.load(); 
         
        // Load captions and source lectures
        captionManager.parseSrtContent(data.srtContent);
        captionManager.displayCaptions();
        
        // Populate sources
        data.sources.forEach(source => { 
            const listItem = document.createElement('li'); 
            listItem.textContent = `• ${source}`; 
            sourceList.appendChild(listItem); 
        }); 
    } catch (error) {
        console.error('Failed to generate video:', error);
        loadingSpinner.classList.add('hidden');
        alert('An error occurred. Please try again.');
    }
}); 

// Add a single timeupdate listener that uses the manager
videoPlayer.addEventListener('timeupdate', () => { 
    captionManager.highlightCaption(videoPlayer.currentTime);
});
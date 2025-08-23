// Get references to key DOM elements 
const qaForm = document.getElementById('qa-form'); 
const videoSection = document.getElementById('video-answer-section'); 
const loadingSpinner = document.getElementById('loading-spinner'); 
const videoPlayer = document.getElementById('answer-video'); 
const captionText = document.getElementById('caption-text'); 
const sourceList = document.getElementById('source-lectures-list'); 

// Get references for the new modal elements
const videoModal = document.getElementById('video-modal');
const originalVideoPlayer = document.getElementById('original-video-player');
const videoModalCloseBtn = document.getElementById('video-modal-close');

// Centralized object to manage caption state and logic
const captionManager = {
    captions: [],
    activeCaptionSpan: null,
    // Add a new property to store the segments data
    segmentsData: [],

    parseAndPrepareCaptions(segmentsData, srtContent) {
        this.segmentsData = segmentsData;
        const lines = srtContent.split('\n\n').filter(line => line.trim() !== '');
        
        // Map SRT captions to segment data
        this.captions = lines.map((line, index) => {
            const parts = line.split('\n');
            const timeString = parts[1];
            const text = parts.slice(2).join(' ').trim();
            const [startTimeStr, endTimeStr] = timeString.split(' --> ');

            const parse_srt_timestamp = (timeStr) => {
                const [hours, minutes, rest] = timeStr.split(':');
                const [seconds, milliseconds] = rest.split(',');
                return parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseInt(seconds) + parseInt(milliseconds) / 1000;
            };

            const parseTime = (timeStr) => {
                const [hours, minutes, seconds] = timeStr.split(':');
                return parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseFloat(seconds);
            };

            const segmentInfo = this.segmentsData[index];
            return {
                start: parse_srt_timestamp(startTimeStr),
                end: parse_srt_timestamp(endTimeStr),
                text: text,
                originalUrl: segmentInfo[3],
                originalStart: parseTime(segmentInfo[2]),
            };
        });
    },

    displayCaptions() {
        captionText.innerHTML = '';
        this.captions.forEach((caption, index) => {
            const span = document.createElement('span');
            span.textContent = caption.text + ' ';
            span.dataset.index = index;
            // Add a class to style and identify clickable captions
            span.classList.add('clickable-caption');
            // Store the original video details as data attributes
            span.dataset.originalUrl = caption.originalUrl;
            span.dataset.originalStart = caption.originalStart;
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
        this.segmentsData = [];
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
        
        // Log the received data for verification
        console.log("Received data:", data);

        loadingSpinner.classList.add('hidden'); 
        videoSection.classList.remove('hidden'); 
         
        videoPlayer.src = data.videoUrl;
        videoPlayer.load(); 
         
        // Load captions and source lectures using both srtContent and segments data
        captionManager.parseAndPrepareCaptions(data.segments, data.srtContent);
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

// Event listener to handle clicks on captions to show the modal
captionText.addEventListener('click', (e) => {
    const clickedSpan = e.target;
    if (clickedSpan.classList.contains('clickable-caption') && clickedSpan.dataset.originalUrl && clickedSpan.dataset.originalStart) {
        const originalUrl = clickedSpan.dataset.originalUrl;
        const originalStart = clickedSpan.dataset.originalStart;

        videoPlayer.pause();
        videoModal.classList.remove('hidden');
        
        originalVideoPlayer.src = originalUrl;
        
        // Use a listener to ensure the video is ready before seeking and playing
        originalVideoPlayer.onloadeddata = () => {
            originalVideoPlayer.currentTime = originalStart;
            originalVideoPlayer.play();
            originalVideoPlayer.onloadeddata = null;
        };

        // Load the video
        originalVideoPlayer.load();
    }
});

// Event listener to close the modal
videoModalCloseBtn.addEventListener('click', () => {
    originalVideoPlayer.pause();
    originalVideoPlayer.src = ""; // Clear the source to stop playback
    videoModal.classList.add('hidden');
});
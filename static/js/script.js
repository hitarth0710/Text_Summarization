// JavaScript for the Text Summarizer application

document.addEventListener('DOMContentLoaded', function() {
    // Handle tab switching and form field focus/blur
    const urlTab = document.getElementById('url-tab');
    const textTab = document.getElementById('text-tab');
    const urlInput = document.getElementById('urlInput');
    const textInput = document.getElementById('textInput');

    if (urlTab && textTab) {
        urlTab.addEventListener('click', function() {
            if (urlInput) {
                setTimeout(() => urlInput.focus(), 300);
            }
        });

        textTab.addEventListener('click', function() {
            if (textInput) {
                setTimeout(() => textInput.focus(), 300);
            }
        });
    }

    // Validate min/max length inputs
    const minLength = document.getElementById('minLength');
    const maxLength = document.getElementById('maxLength');

    if (minLength && maxLength) {
        minLength.addEventListener('change', validateLengths);
        maxLength.addEventListener('change', validateLengths);
    }

    function validateLengths() {
        const min = parseInt(minLength.value);
        const max = parseInt(maxLength.value);

        if (min >= max) {
            minLength.value = Math.max(30, max - 20);
        }

        if (min < 30) minLength.value = 30;
        if (max > 500) maxLength.value = 500;
    }

    // Character count for text input
    if (textInput) {
        textInput.addEventListener('input', function() {
            const charCount = textInput.value.length;
            const wordCount = textInput.value.trim().split(/\s+/).filter(Boolean).length;

            // You could add a counter element if desired
            console.log(`Characters: ${charCount}, Words: ${wordCount}`);
        });
    }
});
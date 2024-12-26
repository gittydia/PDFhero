document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        uploadBtn: document.getElementById('uploadBtn'),
        pdfInput: document.getElementById('pdfInput'),
        sendBtn: document.getElementById('sendBtn'),
        userInput: document.getElementById('userInput'),
        chatBox: document.getElementById('chatBox')
    };

    const API_URL = 'http://localhost:8000';

    // Event Listeners
    elements.uploadBtn?.addEventListener('click', handleFileUpload);
    elements.sendBtn?.addEventListener('click', handleChatSubmit);
    elements.userInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleChatSubmit();
        }
    });

    async function handleFileUpload() {
        const file = elements.pdfInput?.files[0];
        if (!file) {
            showError('Please select a PDF file first');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            showLoading('Uploading PDF...');
            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            addMessageToChatBox('System', `PDF uploaded successfully: ${data.info}`);
        } catch (error) {
            showError(`Upload failed: ${error.message}`);
        } finally {
            hideLoading();
        }
    }

    async function handleChatSubmit() {
        const input = elements.userInput?.value.trim();
        if (!input) {
            showError('Please enter a message first');
            return;
        }

        addMessageToChatBox('You', input);
        elements.userInput.value = '';

        try {
            showLoading('Hero is thinking...');
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: input })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            addMessageToChatBox('Hero', data.response);
        } catch (error) {
            showError(`Failed to get Hero response: ${error.message}`);
        } finally {
            hideLoading();
        }
    }

    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Upload failed');
            }

            return await response.json();
        } catch (error) {
            showError(`File upload failed: ${error.message}`);
            throw error;
        }
    }

    async function generateResponse(content) {
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: content,
                    chunk_size: 1000
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Generation failed');
            }

            const data = await response.json();
            return data.chunks;
        } catch (error) {
            showError(`Failed to generate response: ${error.message}`);
            throw error;
        }
    }

    elements.fileInput?.addEventListener('change', async (event) => {
        try {
            showLoading();
            const file = event.target.files[0];
            const uploadResult = await uploadFile(file);
            const chunks = await generateResponse(uploadResult.content);
            addMessageToChatBox('System', `Processed ${chunks.length} chunks`);
        } catch (error) {
            showError(error.message);
        } finally {
            hideLoading();
        }
    });

    function addMessageToChatBox(sender, message) {
        const messageElement = document.createElement('div');
        const messageClass = sender === 'Hero' ? 'chat-message-ai' : 'chat-message-you';
        messageElement.classList.add('chat-message');
        messageElement.classList.add('chat-message', `chat-message-${sender.toLowerCase()}`);
        messageElement.classList.add('chat-message', messageClass);

        messageElement.innerHTML = `
            <div class="message-content">${sanitizeHTML(message)}</div>
            <div class="message-timestamp">${new Date().toLocaleTimeString()}</div>
        `;
        
        elements.chatBox?.appendChild(messageElement);
        elements.chatBox?.scrollTo({
            top: elements.chatBox.scrollHeight,
            behavior: 'smooth'
        });
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('error-message');
        errorDiv.textContent = message;
        elements.chatBox?.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    function showLoading(message) {
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-indicator';
        loadingDiv.classList.add('loading-message');
        loadingDiv.textContent = message;
        elements.chatBox?.appendChild(loadingDiv);
    }

    function hideLoading() {
        document.getElementById('loading-indicator')?.remove();
    }

    function sanitizeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }



    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('error-message');
        errorDiv.textContent = message;
        elements.chatBox?.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    function showLoading(message) {
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-indicator';
        loadingDiv.classList.add('loading-message');
        loadingDiv.textContent = message;
        elements.chatBox?.appendChild(loadingDiv);
    }

    function hideLoading() {
        document.getElementById('loading-indicator')?.remove();
    }

    function sanitizeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});
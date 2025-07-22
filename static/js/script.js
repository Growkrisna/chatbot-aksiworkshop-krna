document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`;
        
        const bubbleClass = role === 'user' 
            ? 'bg-blue-600 text-white rounded-l-xl rounded-br-xl'
            : 'bg-gray-100 rounded-r-xl rounded-bl-xl';
        
        messageDiv.innerHTML = `
            <div class="${bubbleClass} p-3 max-w-xs lg:max-w-md shadow-sm">
                ${content}
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        addMessage('user', query);
        userInput.value = '';

        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `query=${encodeURIComponent(query)}`
            });
            const books = await response.json();

            if (books.length > 0) {
                let booksHtml = books.map(book => `
                    <div class="mb-3 p-3 bg-white rounded-lg border border-gray-200 shadow-xs">
                        <div class="flex">
                            <img src="${book.thumbnail}" 
                                 alt="Cover" 
                                 class="w-16 h-24 object-cover rounded mr-3">
                            <div>
                                <h4 class="font-bold text-sm">${book.title}</h4>
                                <p class="text-xs text-gray-600">${book.authors}</p>
                                <a href="${book.preview_link}" target="_blank" 
                                   class="mt-1 inline-block text-xs text-blue-500 hover:underline">
                                    <i class="fas fa-external-link-alt mr-1"></i> Preview
                                </a>
                            </div>
                        </div>
                    </div>
                `).join('');
                addMessage('assistant', `<p class="font-medium mb-2">📚 Ditemukan ${books.length} buku:</p>${booksHtml}`);
            } else {
                addMessage('assistant', 'Maaf, buku tidak ditemukan. Coba kata kunci lain.');
            }
        } catch (error) {
            addMessage('assistant', 'Terjadi error saat mencari buku. Silakan coba lagi.');
            console.error('Error:', error);
        }
    });
});
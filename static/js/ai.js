document.addEventListener('DOMContentLoaded', function() {
  const chatButton = document.getElementById('ai-chat-button');
  const chatPanel = document.getElementById('ai-chat-panel');
  const chatMessages = document.getElementById('ai-chat-messages');
  const chatInput = document.getElementById('ai-chat-input');
  const chatSend = document.getElementById('ai-chat-send');

  function appendMessage(sender, text) {
    const el = document.createElement('div');
    el.style.marginBottom = '8px';
    if (sender === 'user') {
      el.innerHTML = `<div style="text-align:right;"><small>You</small><div style="display:inline-block; background:#e9f5ff; padding:8px 10px; border-radius:8px; max-width:85%;">${text}</div></div>`;
    } else {
      el.innerHTML = `<div style="text-align:left;"><small>Advisor</small><div style="display:inline-block; background:#f1f8e9; padding:8px 10px; border-radius:8px; max-width:85%;">${text}</div></div>`;
    }
    chatMessages.appendChild(el);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function getUserId() {
    let uid = localStorage.getItem('di_user_id');
    if (!uid) {
      uid = 'anon_' + Math.random().toString(36).slice(2,9);
      localStorage.setItem('di_user_id', uid);
    }
    return uid;
  }

  chatButton.addEventListener('click', function() {
    if (chatPanel.style.display === 'none' || chatPanel.style.display === '') {
      chatPanel.style.display = 'block';
      chatButton.textContent = '✖ Close Advisor';
    } else {
      chatPanel.style.display = 'none';
      chatButton.textContent = '🤖 Ask the AI Advisor';
    }
  });

  chatSend.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', function(e){ if (e.key === 'Enter') sendMessage(); });

  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    appendMessage('user', text);
    chatInput.value = '';

    appendMessage('advisor', 'Thinking...');
    const messages = chatMessages.querySelectorAll('div');
    // Simple fetch to backend AI endpoint
    try {
      const res = await fetch('/api/ai-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, user_id: getUserId() })
      });
      const data = await res.json();
      // Remove the 'Thinking...' message (last appended)
      const last = chatMessages.lastChild;
      if (last) chatMessages.removeChild(last);
      appendMessage('advisor', data.reply || 'Sorry, no reply.');
    } catch (err) {
      const last = chatMessages.lastChild;
      if (last) chatMessages.removeChild(last);
      appendMessage('advisor', 'AI service error. Try again later.');
    }
  }

});

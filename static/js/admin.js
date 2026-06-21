// Admin editor: loads scenarios and saves via session-protected endpoint
(async function(){
  const textarea = document.getElementById('scenarios-json');
  const saveBtn = document.getElementById('save-btn');
  const statusSpan = document.getElementById('save-status');

  try {
    const res = await fetch('/api/scenarios');
    if (res.ok) {
      const data = await res.json();
      textarea.value = JSON.stringify(data, null, 2);
    } else {
      textarea.value = 'Unable to load scenarios via /api/scenarios';
    }
  } catch (e) {
    textarea.value = 'Error: ' + e.message;
  }

  saveBtn.addEventListener('click', ()=>{
    try {
      const payload = JSON.parse(textarea.value);
      statusSpan.innerText = 'Saving...';
      fetch('/api/admin/save-scenarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(r=>{
        if (r.ok) return r.json();
        return r.json().then(e => { throw new Error(e.error || 'Save failed'); });
      }).then(j=>{
        statusSpan.innerText = '✅ Saved!';
        statusSpan.style.color = '#2e7d32';
        setTimeout(()=>{ statusSpan.innerText = ''; statusSpan.style.color = '#000'; }, 3000);
      }).catch(e=>{
        statusSpan.innerText = '❌ ' + e.message;
        statusSpan.style.color = '#d32f2f';
      });
    } catch (e) {
      statusSpan.innerText = '❌ Invalid JSON: ' + e.message;
      statusSpan.style.color = '#d32f2f';
    }
  });
})();

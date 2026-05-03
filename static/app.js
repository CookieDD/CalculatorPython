const display = document.getElementById('display');
let expr = '';

function updateDisplay(v){
  if(!display) return;
  display.textContent = v === '' ? '0' : v;
}

document.querySelectorAll('.btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    const val = btn.getAttribute('data-value');
    const action = btn.getAttribute('data-action');
    if(action === 'clear'){
      expr = '';
      updateDisplay(expr);
      return;
    }
    if(action === 'back'){
      expr = expr.slice(0,-1);
      updateDisplay(expr);
      return;
    }
    if(btn.id === 'equals'){
      if(!expr) return;
      fetch('/api/calc',{ 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expr })
      })
      .then(r => r.json().then(j => ({ ok: r.ok, body: j })).catch(() => ({ ok: r.ok, body: null })))
      .then(({ ok, body })=>{
        if(ok && body && body.result !== undefined){
          expr = String(body.result);
          updateDisplay(expr);
        } else if(body && body.detail){
          updateDisplay(body.detail);
        } else {
          updateDisplay('Err');
        }
      })
      .catch(()=> updateDisplay('Err'));
      return;
    }
    if(val){
      expr += val;
      updateDisplay(expr);
    }
  });
});

updateDisplay('0');

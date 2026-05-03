const display = document.getElementById('display');
let expr = '';

function updateDisplay(v){
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
      .then(r=>r.json())
      .then(j=>{
        if(j.result !== undefined){
          expr = String(j.result);
          updateDisplay(expr);
        } else if(j.detail){
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

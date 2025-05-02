function showTab(method) {
    const forms = document.querySelectorAll('.payment-form');
    forms.forEach(f => f.classList.add('hidden'));
  
    document.getElementById(method).classList.remove('hidden');
  
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(b => b.classList.remove('active'));
  
    event.target.classList.add('active');
  }
  
  document.querySelector('.pay-btn').addEventListener('click', function () {
    const activeTab = document.querySelector('.tab-btn.active').textContent.trim();
  
    let valid = true;
    let inputs;
  
    if (activeTab.includes('Card')) {
      inputs = document.querySelectorAll('#card input');
    } else if (activeTab.includes('UPI')) {
      inputs = document.querySelectorAll('#upi input');
    } else if (activeTab.includes('Net Banking')) {
      inputs = document.querySelectorAll('#netbanking select');
    }
  
    inputs.forEach(input => {
      if (!input.value.trim()) {
        valid = false;
      }
    });
  
    if (valid) {
      document.querySelector('.payment-container').innerHTML = `
        <h2>✅ Payment Successful!</h2>
        <p class="flight-summary">Thank you for booking your flight with us.</p>
        <p style="text-align:center; font-size: 16px;">Have a safe journey! ✈️</p>
        <div style="text-align:center; margin-top: 20px;">
          <button onclick="goBack()" class="ok-btn">OK</button>
        </div>
      `;
    } else {
      alert('Please fill in all required fields before proceeding.');
    }
  });
  
  function goBack() {
    history.back(); // or use: window.location.href = "search.html";
  }
  
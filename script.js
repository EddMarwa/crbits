const API_BASE_URL = "http://127.0.0.1:8000"; // Adjust if your FastAPI runs on a different port/host

// --- Utility Functions ---
async function fetchData(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method,
        headers,
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `API error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        alert(`Error: ${error.message}`);
        return null;
    }
}

// --- Rendering Functions ---
async function renderDashboardSummary() {
    const summary = await fetchData('/dashboard/summary');
    if (summary) {
        document.getElementById('balance').innerText = `$${summary.current_value.toFixed(2)}`;
        document.getElementById('roi').innerText = `ROI: ${summary.roi.toFixed(2)}%`;
    }
}

async function renderBotAllocations() {
    const bots = await fetchData('/bots');
    const botsContainer = document.getElementById('bots-container');
    if (bots && bots.length > 0) {
        botsContainer.innerHTML = '<h3>Available Bots</h3>';
        bots.forEach(bot => {
            const botDiv = document.createElement('div');
            botDiv.innerHTML = `
                <p><strong>${bot.name}</strong> (Risk: ${bot.risk_level || 'N/A'})</p>
                <input type="number" id="allocate-${bot.id}" placeholder="Amount to allocate">
                <button onclick="handleBotAllocation('${bot.id}')">Allocate</button>
            `;
            botsContainer.appendChild(botDiv);
        });
    } else {
        botsContainer.innerHTML = '<p>No bots available.</p>';
    }
}

async function handleBotAllocation(botId) {
    const amountInput = document.getElementById(`allocate-${botId}`);
    const amount = parseFloat(amountInput.value);

    if (isNaN(amount) || amount <= 0) {
        alert('Please enter a valid amount to allocate.');
        return;
    }

    const payload = {
        bot_id: botId,
        amount: amount
    };

    const result = await fetchData('/bots/allocate', 'POST', payload);
    if (result) {
        alert(`Allocated $${amount.toFixed(2)} to bot ${botId}`);
        amountInput.value = ''; // Clear input
        renderDashboardSummary(); // Refresh dashboard
    }
}

async function renderLedgerHistory() {
    const history = await fetchData('/ledger/history');
    const ledgerTable = document.getElementById('ledger');
    if (history && history.length > 0) {
        ledgerTable.innerHTML = `
            <tr>
                <th>Type</th>
                <th>Amount</th>
                <th>Currency</th>
                <th>Status</th>
                <th>Date</th>
            </tr>
        `;
        history.forEach(transaction => {
            const row = ledgerTable.insertRow();
            row.innerHTML = `
                <td>${transaction.type}</td>
                <td>${transaction.amount.toFixed(2)}</td>
                <td>${transaction.currency}</td>
                <td>${transaction.status}</td>
                <td>${new Date(transaction.created_at).toLocaleDateString()}</td>
            `;
        });
    } else {
        ledgerTable.innerHTML = '<p>No transaction history.</p>';
    }
}

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    // For demonstration, let's assume a user logs in and gets a token
    // You'd typically have login/register forms for this.
    if (!localStorage.getItem('access_token')) {
        // Example: Register a user and log in to get a token
        // This should be done via forms, but for quick MVP, direct call
        // IMPORTANT: Replace with actual user interaction in a production app!
        async function setupUserAndLogin() {
            try {
                await fetchData('/auth/register', 'POST', { email: "test@example.com", password: "password" });
                const loginResponse = await fetchData('/auth/login', 'POST', {
                    username: "test@example.com",
                    password: "password"
                });
                if (loginResponse && loginResponse.access_token) {
                    localStorage.setItem('access_token', loginResponse.access_token);
                    console.log("User registered and logged in.");
                    initializeDashboard();
                } else {
                    console.error("Login failed after registration attempt.");
                }
            } catch (error) {
                // If user already registered, just try to login
                if (error.message.includes("Email already registered")) {
                     try {
                        const loginResponse = await fetchData('/auth/login', 'POST', {
                            username: "test@example.com",
                            password: "password"
                        });
                        if (loginResponse && loginResponse.access_token) {
                            localStorage.setItem('access_token', loginResponse.access_token);
                            console.log("User already registered, logged in.");
                            initializeDashboard();
                        }
                    } catch (loginError) {
                        console.error("Failed to login existing user:", loginError);
                        alert("Failed to log in. Please check console.");
                    }
                } else {
                    console.error("Registration failed:", error);
                    alert("Failed to register user. Please check console.");
                }
            }
        }
        setupUserAndLogin();
    } else {
        initializeDashboard();
    }

    document.getElementById('withdraw').addEventListener('click', async () => {
        const amount = prompt("Enter withdrawal amount:");
        if (amount) {
            const result = await fetchData('/withdrawals/request', 'POST', { amount: parseFloat(amount), currency: "USD" });
            if (result) {
                alert("Withdrawal requested! Awaiting admin approval.");
                renderLedgerHistory();
            }
        }
    });
});

function initializeDashboard() {
    renderDashboardSummary();
    renderBotAllocations();
    renderLedgerHistory();
}


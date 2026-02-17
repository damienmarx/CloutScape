/**
 * CloutScape Games - Complete Frontend Implementation
 * High-performance gambling logic with real-time sync
 */

class CloutScapeGames {
    constructor() {
        this.balance = 0;
        this.init();
    }

    init() {
        console.log("CloutScape Games Initialized");
        this.setupChat();
        this.setupLiveLogs();
        this.syncBalance();
        setInterval(() => this.fetchLiveBets(), 3000);
        setInterval(() => this.fetchChat(), 2000);
    }

    async syncBalance() {
        try {
            const res = await fetch('/api/account/balance');
            const data = await res.json();
            this.balance = data.balance;
            this.updateBalanceUI();
        } catch (e) { console.error("Balance sync failed", e); }
    }

    updateBalanceUI() {
        const elements = ['slots-balance', 'keno-balance', 'crash-balance', 'dice-balance', 'global-balance'];
        elements.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = this.balance.toLocaleString(undefined, {minimumFractionDigits: 2});
        });
    }

    async fetchChat() {
        try {
            const res = await fetch('/api/live/chat');
            const messages = await res.json();
            const chatMessages = document.getElementById('chat-messages');
            if (!chatMessages) return;
            
            chatMessages.innerHTML = '';
            messages.forEach(msg => {
                const div = document.createElement('div');
                div.className = 'mb-2 text-sm';
                div.innerHTML = `<span class="font-bold ${msg.color}">${msg.user}:</span> <span class="text-slate-300">${msg.message}</span>`;
                chatMessages.appendChild(div);
            });
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } catch (e) {}
    }

    async fetchLiveBets() {
        try {
            const res = await fetch('/api/live/bets');
            const bets = await res.json();
            const logTable = document.getElementById('live-bet-logs');
            if (!logTable) return;
            
            logTable.innerHTML = '';
            bets.forEach(bet => {
                const row = document.createElement('tr');
                row.className = 'border-b border-white/5 hover:bg-white/5 transition-colors';
                const isWin = bet.payout > 0;
                row.innerHTML = `
                    <td class="py-3 px-4 text-xs font-bold uppercase text-slate-400">${bet.game}</td>
                    <td class="py-3 px-4 text-sm text-slate-300">${bet.user}</td>
                    <td class="py-3 px-4 text-sm text-slate-300">$${bet.bet.toLocaleString()}</td>
                    <td class="py-3 px-4 text-sm ${isWin ? 'text-green-400' : 'text-slate-500'}">${bet.multiplier}x</td>
                    <td class="py-3 px-4 text-sm font-bold ${isWin ? 'text-green-400' : 'text-red-400'}">$${bet.payout.toLocaleString()}</td>
                `;
                logTable.appendChild(row);
            });
        } catch (e) {}
    }

    setupChat() {
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send');
        if (!chatInput || !sendBtn) return;

        sendBtn.addEventListener('click', async () => {
            const msg = chatInput.value.trim();
            if (msg) {
                chatInput.value = '';
                await fetch('/api/live/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                this.fetchChat();
            }
        });

        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendBtn.click();
        });
    }

    setupLiveLogs() {
        this.logTable = document.getElementById('live-bet-logs');
    }

    async addBetLog(game, user, bet, multiplier, payout) {
        await fetch('/api/games/bet', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({game, bet, multiplier, payout})
        });
        this.fetchLiveBets();
        this.syncBalance();
    }

    // ==========================================
    // SLOTS
    // ==========================================
    initSlots(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="slots-game glass p-6 rounded-3xl border border-yellow-500/30">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-black text-yellow-500 font-heading">RICH SLOTS</h2>
                    <div class="text-xs font-bold text-slate-500">BAL: <span id="slots-balance" class="text-white font-mono">0.00</span></div>
                </div>
                <div class="reels flex gap-3 justify-center mb-6 bg-black/40 p-4 rounded-2xl border border-white/5">
                    <div id="reel-1" class="reel w-20 h-28 bg-white/5 flex items-center justify-center text-4xl rounded-xl border border-white/5">🍎</div>
                    <div id="reel-2" class="reel w-20 h-28 bg-white/5 flex items-center justify-center text-4xl rounded-xl border border-white/5">🍎</div>
                    <div id="reel-3" class="reel w-20 h-28 bg-white/5 flex items-center justify-center text-4xl rounded-xl border border-white/5">🍎</div>
                </div>
                <div class="flex gap-2">
                    <input type="number" id="slots-bet" value="1000" class="bg-black/40 text-white p-3 rounded-xl flex-grow border border-white/10 text-sm font-bold focus:outline-none focus:border-yellow-500">
                    <button id="spin-btn" class="bg-yellow-600 hover:bg-yellow-500 text-black font-black py-3 px-8 rounded-xl transition-all transform active:scale-95 text-sm">SPIN</button>
                </div>
                <div id="slots-result" class="mt-4 text-center font-bold text-sm h-4"></div>
            </div>
        `;

        const spinBtn = document.getElementById('spin-btn');
        const reels = [document.getElementById('reel-1'), document.getElementById('reel-2'), document.getElementById('reel-3')];
        const resultDiv = document.getElementById('slots-result');
        const symbols = ['🍎', '🍊', '🍋', '🍌', '🍉', '🎰', '💎', '🔔'];

        spinBtn.addEventListener('click', () => {
            const bet = parseInt(document.getElementById('slots-bet').value);
            if (bet > this.balance) {
                resultDiv.innerText = "INSUFFICIENT BALANCE";
                resultDiv.className = "mt-4 text-center font-bold text-sm h-4 text-red-500";
                return;
            }

            this.balance -= bet;
            this.updateBalanceUI();
            resultDiv.innerText = "SPINNING...";
            resultDiv.className = "mt-4 text-center font-bold text-sm h-4 text-yellow-500";
            spinBtn.disabled = true;

            let spins = 0;
            const interval = setInterval(() => {
                reels.forEach(reel => {
                    reel.innerText = symbols[Math.floor(Math.random() * symbols.length)];
                });
                spins++;
                if (spins > 15) {
                    clearInterval(interval);
                    this.finalizeSlots(bet, reels, resultDiv, spinBtn, symbols);
                }
            }, 60);
        });
    }

    finalizeSlots(bet, reels, resultDiv, spinBtn, symbols) {
        const final = [symbols[Math.floor(Math.random()*8)], symbols[Math.floor(Math.random()*8)], symbols[Math.floor(Math.random()*8)]];
        reels.forEach((r, i) => r.innerText = final[i]);

        let mult = 0;
        if (final[0] === final[1] && final[1] === final[2]) mult = 10;
        else if (final[0] === final[1] || final[1] === final[2] || final[0] === final[2]) mult = 2;

        const win = bet * mult;
        this.balance += win;
        this.updateBalanceUI();
        
        if (win > 0) {
            resultDiv.innerText = `WIN: $${win.toLocaleString()}`;
            resultDiv.className = "mt-4 text-center font-bold text-sm h-4 text-green-500";
        } else {
            resultDiv.innerText = "LOSE";
            resultDiv.className = "mt-4 text-center font-bold text-sm h-4 text-slate-500";
        }
        
        this.addBetLog('Slots', 'You', bet, mult, win);
        spinBtn.disabled = false;
    }

    // ==========================================
    // KENO 40
    // ==========================================
    initKeno(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="keno-game glass p-6 rounded-3xl border border-blue-500/30">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-black text-blue-500 font-heading">KENO 40</h2>
                    <div class="text-xs font-bold text-slate-500">BAL: <span id="keno-balance" class="text-white font-mono">0.00</span></div>
                </div>
                <div id="keno-grid" class="grid grid-cols-8 gap-1.5 mb-6">
                    ${Array.from({length: 40}, (_, i) => `
                        <button class="keno-num bg-white/5 hover:bg-white/10 text-white font-bold py-2 rounded-lg border border-white/5 transition-all text-xs" data-num="${i+1}">${i+1}</button>
                    `).join('')}
                </div>
                <div class="flex gap-2">
                    <input type="number" id="keno-bet" value="1000" class="bg-black/40 text-white p-3 rounded-xl flex-grow border border-white/10 text-sm font-bold focus:outline-none focus:border-blue-500">
                    <button id="keno-play-btn" class="bg-blue-600 hover:bg-blue-500 text-white font-black py-3 px-8 rounded-xl transition-all transform active:scale-95 text-sm">PLAY</button>
                </div>
                <div id="keno-result" class="mt-4 text-center font-bold text-sm h-4 text-slate-500">Select up to 10 numbers</div>
            </div>
        `;

        const playBtn = document.getElementById('keno-play-btn');
        const resultDiv = document.getElementById('keno-result');
        const numButtons = document.querySelectorAll('.keno-num');
        let selected = new Set();

        numButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const num = parseInt(btn.dataset.num);
                if (selected.has(num)) {
                    selected.delete(num);
                    btn.classList.remove('bg-blue-600', 'border-blue-400');
                    btn.classList.add('bg-white/5');
                } else if (selected.size < 10) {
                    selected.add(num);
                    btn.classList.remove('bg-white/5');
                    btn.classList.add('bg-blue-600', 'border-blue-400');
                }
            });
        });

        playBtn.addEventListener('click', () => {
            if (selected.size === 0) return;
            const bet = parseInt(document.getElementById('keno-bet').value);
            if (bet > this.balance) return;

            this.balance -= bet;
            this.updateBalanceUI();
            playBtn.disabled = true;

            const drawn = new Set();
            while (drawn.size < 10) drawn.add(Math.floor(Math.random() * 40) + 1);

            let hits = 0;
            const drawnArr = Array.from(drawn);
            drawnArr.forEach((num, i) => {
                setTimeout(() => {
                    const btn = document.querySelector(`.keno-num[data-num="${num}"]`);
                    if (selected.has(num)) {
                        hits++;
                        btn.classList.add('ring-2', 'ring-green-500', 'z-10');
                    } else {
                        btn.classList.add('ring-2', 'ring-red-500', 'z-10');
                    }

                    if (i === 9) {
                        const mult = hits >= selected.size / 2 ? hits : 0;
                        const win = bet * mult;
                        this.balance += win;
                        this.updateBalanceUI();
                        resultDiv.innerText = `HITS: ${hits} | WIN: $${win.toLocaleString()}`;
                        resultDiv.className = win > 0 ? "mt-4 text-center font-bold text-sm h-4 text-green-500" : "mt-4 text-center font-bold text-sm h-4 text-slate-500";
                        this.addBetLog('Keno', 'You', bet, mult, win);
                        setTimeout(() => {
                            document.querySelectorAll('.keno-num').forEach(b => b.classList.remove('ring-2', 'ring-green-500', 'ring-red-500'));
                            playBtn.disabled = false;
                        }, 2000);
                    }
                }, i * 150);
            });
        });
    }

    // ==========================================
    // CRASH
    // ==========================================
    initCrash(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="crash-game glass p-6 rounded-3xl border border-red-500/30">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-black text-red-500 font-heading">CRASH</h2>
                    <div class="text-xs font-bold text-slate-500">BAL: <span id="crash-balance" class="text-white font-mono">0.00</span></div>
                </div>
                <div class="h-40 bg-black/40 rounded-2xl mb-6 flex items-center justify-center border border-white/5 relative overflow-hidden">
                    <div id="crash-mult" class="text-5xl font-black text-white z-10 font-heading">1.00x</div>
                    <div class="absolute bottom-0 left-0 w-full h-1 bg-red-500/20"></div>
                </div>
                <div class="flex gap-2">
                    <input type="number" id="crash-bet" value="1000" class="bg-black/40 text-white p-3 rounded-xl flex-grow border border-white/10 text-sm font-bold focus:outline-none focus:border-red-500">
                    <button id="crash-btn" class="bg-red-600 hover:bg-red-500 text-white font-black py-3 px-8 rounded-xl transition-all transform active:scale-95 text-sm">BET</button>
                </div>
                <div id="crash-result" class="mt-4 text-center font-bold text-sm h-4"></div>
            </div>
        `;

        const btn = document.getElementById('crash-btn');
        const multText = document.getElementById('crash-mult');
        const resultDiv = document.getElementById('crash-result');
        let running = false;
        let current = 1.00;
        let bet = 0;

        btn.addEventListener('click', () => {
            if (!running) {
                bet = parseInt(document.getElementById('crash-bet').value);
                if (bet > this.balance) return;
                this.balance -= bet;
                this.updateBalanceUI();
                running = true;
                btn.innerText = "CASH OUT";
                btn.className = "bg-green-600 hover:bg-green-500 text-white font-black py-3 px-8 rounded-xl transition-all transform active:scale-95 text-sm";
                current = 1.00;
                const crashPoint = Math.random() * 5 + 1;
                
                const loop = setInterval(() => {
                    if (!running) { clearInterval(loop); return; }
                    current += 0.01 * (current ** 0.5);
                    multText.innerText = current.toFixed(2) + "x";
                    if (current >= crashPoint) {
                        running = false;
                        clearInterval(loop);
                        multText.innerText = "CRASHED @ " + current.toFixed(2) + "x";
                        multText.className = "text-4xl font-black text-red-600 z-10 font-heading";
                        btn.innerText = "BET";
                        btn.className = "bg-red-600 hover:bg-red-500 text-white font-black py-3 px-8 rounded-xl transition-all transform active:scale-95 text-sm";
                        this.addBetLog('Crash', 'You', bet, current.toFixed(2), 0);
                        setTimeout(() => { multText.className = "text-5xl font-black text-white z-10 font-heading"; multText.innerText = "1.00x"; }, 2000);
                    }
                }, 50);
            } else {
                running = false;
                const win = Math.floor(bet * current);
                this.balance += win;
                this.updateBalanceUI();
                btn.innerText = "BET";
                btn.className = "bg-red-600 hover:bg-red-500 text-white font-black py-3 px-8 rounded-xl transition-all transform active:scale-95 text-sm";
                resultDiv.innerText = `CASHED OUT @ ${current.toFixed(2)}x`;
                resultDiv.className = "mt-4 text-center font-bold text-sm h-4 text-green-500";
                this.addBetLog('Crash', 'You', bet, current.toFixed(2), win);
            }
        });
    }

    // ==========================================
    // DICE
    // ==========================================
    initDice(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="dice-game glass p-6 rounded-3xl border border-purple-500/30">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-black text-purple-500 font-heading">DICE DUEL</h2>
                    <div class="text-xs font-bold text-slate-500">BAL: <span id="dice-balance" class="text-white font-mono">0.00</span></div>
                </div>
                <div class="flex gap-4 justify-center mb-6">
                    <div class="text-center">
                        <div class="text-[10px] font-bold text-slate-500 uppercase mb-2">You</div>
                        <div id="p-dice" class="w-20 h-20 bg-white/5 rounded-2xl flex items-center justify-center text-4xl font-black border border-white/5">?</div>
                    </div>
                    <div class="flex items-center text-2xl font-black text-slate-700">VS</div>
                    <div class="text-center">
                        <div class="text-[10px] font-bold text-slate-500 uppercase mb-2">House</div>
                        <div id="h-dice" class="w-20 h-20 bg-white/5 rounded-2xl flex items-center justify-center text-4xl font-black border border-white/5">?</div>
                    </div>
                </div>
                <div class="flex gap-2">
                    <input type="number" id="dice-bet" value="1000" class="bg-black/40 text-white p-3 rounded-xl flex-grow border border-white/10 text-sm font-bold focus:outline-none focus:border-purple-500">
                    <button id="dice-btn" class="bg-purple-600 hover:bg-purple-500 text-white font-black py-3 px-8 rounded-xl transition-all transform active:scale-95 text-sm">ROLL</button>
                </div>
                <div id="dice-result" class="mt-4 text-center font-bold text-sm h-4"></div>
            </div>
        `;

        const btn = document.getElementById('dice-btn');
        const pDice = document.getElementById('p-dice');
        const hDice = document.getElementById('h-dice');
        const resultDiv = document.getElementById('dice-result');

        btn.addEventListener('click', () => {
            const bet = parseInt(document.getElementById('dice-bet').value);
            if (bet > this.balance) return;
            this.balance -= bet;
            this.updateBalanceUI();
            btn.disabled = true;

            let rolls = 0;
            const loop = setInterval(() => {
                pDice.innerText = Math.floor(Math.random()*100)+1;
                hDice.innerText = Math.floor(Math.random()*100)+1;
                rolls++;
                if (rolls > 10) {
                    clearInterval(loop);
                    const p = Math.floor(Math.random()*100)+1;
                    const h = Math.floor(Math.random()*100)+1;
                    pDice.innerText = p;
                    hDice.innerText = h;
                    
                    let win = 0;
                    let mult = 0;
                    if (p > h) { win = bet * 2; mult = 2; resultDiv.innerText = "YOU WIN!"; resultDiv.className = "mt-4 text-center font-bold text-sm h-4 text-green-500"; }
                    else { resultDiv.innerText = "HOUSE WINS"; resultDiv.className = "mt-4 text-center font-bold text-sm h-4 text-red-500"; }
                    
                    this.balance += win;
                    this.updateBalanceUI();
                    this.addBetLog('Dice', 'You', bet, mult, win);
                    btn.disabled = false;
                }
            }, 80);
        });
    }
}

window.CloutScapeGames = new CloutScapeGames();

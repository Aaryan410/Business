let money = 0;
let moneyPerClick = 100;
let moneyPerSecond = 10;

const balance = document.getElementById("balance");
const earnButton = document.getElementById("earn-button");

const incomeRate = document.getElementById("income-rate");

function formatMoney(cents) {
    return (cents / 100).toFixed(2);
}

function updateDisplay() {
    balance.textContent = formatMoney(money);
    incomeRate.textContent = formatMoney(moneyPerSecond);
}

updateDisplay();

setInterval(() => {
    money += moneyPerSecond;
    updateDisplay();
}, 1000);

earnButton.addEventListener("click", (event) => {
    money += moneyPerClick;
    updateDisplay();

    const popup = document.createElement("span");
    popup.className = "money-pop";
    popup.textContent = `+$${formatMoney(moneyPerClick)}`;
    popup.setAttribute("aria-hidden", "true");

    const area = earnButton.getBoundingClientRect();
    const x = event.detail === 0
        ? area.width / 2
        : event.clientX - area.left;

    const y = event.detail === 0
        ? area.height / 2
        : event.clientY - area.top;
        
    popup.style.left = `${x}px`;
    popup.style.top = `${y}px`;

    earnButton.appendChild(popup);

    popup.addEventListener("animationend", () => {
        popup.remove();
    }, { once: true });
});
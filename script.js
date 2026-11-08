let money = 0n;
let moneyPerClick = 100n;
let moneyPerSecond = 10n;

let multiplier = 1n;
let multiplierCost = 500n;

let incomeMultiplier = 1n;
let incomeMultiplierCost = 500n;

const balance = document.getElementById("balance");
const earnButton = document.getElementById("earn-button");
const incomeRate = document.getElementById("income-rate");

const multiplierDisplay = document.getElementById("multiplier");
const multiplierButton = document.getElementById("multiplier-button");


// large number display logic
function formatNumber(value) {
    const digits = value.toString();

    if (digits.length <= 3) {
        return digits;
    }

    const suffixes = [
        "", "K", "M", "B", "T", 
        "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"
    ];

    const group = Math.floor((digits.length - 1) / 3);

    if (group >= suffixes.length) {
        return `${digits[0]}.${digits.slice(1, 3)}e${digits.length - 1}`;
    }

    const leading = digits.length - group * 3;

    return (
        digits.slice(0, leading) +
        "." +
        digits.slice(leading, leading + 2) +
        suffixes[group]
    );
}

function formatMoney(cents) {
    const dollars = cents / 100n;
    const remainder = (cents % 100n).toString().padStart(2, "0");

    if (dollars < 100n) {
        return `${dollars}.${remainder}`;
    }

    return formatNumber(dollars);
}


const incomeMultiplierDisplay = 
    document.getElementById("income-multiplier");

const incomeMultiplierButton = 
    document.getElementById("income-multiplier-button");


// display logic
function updateDisplay() {
    balance.textContent = formatMoney(money);
    incomeRate.textContent = formatMoney(moneyPerSecond);

    multiplierDisplay.textContent = formatNumber(multiplier);

    multiplierButton.textContent =
        `Upgrade to ${multiplier * 2n}× - $${formatMoney(multiplierCost)}`;

    multiplierButton.disabled = money < multiplierCost;

    incomeRate.textContent = formatMoney(
        moneyPerSecond * incomeMultiplier
    );

    incomeMultiplierDisplay.textContent =
        formatNumber(incomeMultiplier);

    incomeMultiplierButton.textContent =
        `Upgrade passive income to ${formatNumber(incomeMultiplier * 2n)}× - $${formatMoney(incomeMultiplierCost)}`;

    incomeMultiplierButton.disabled =
        money < incomeMultiplierCost;
}

updateDisplay();


// timer logic
setInterval(() => {
    money += moneyPerSecond * incomeMultiplier;
    updateDisplay();
}, 1000);


// click logic
earnButton.addEventListener("click", (event) => {
    money += moneyPerClick * multiplier;
    updateDisplay();

    const popup = document.createElement("span");
    popup.className = "money-pop";
    popup.textContent = `+$${formatMoney(moneyPerClick * multiplier)}`;
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


// multiplier button logic for per click 
multiplierButton.addEventListener("click", () => {
    if (money < multiplierCost) {
        return;
    }

    money -= multiplierCost;
    multiplier *= 2n;
    multiplierCost *= 3n;

    updateDisplay();
});


// multiplier button logic for per second
incomeMultiplierButton.addEventListener("click", () => {
    if (money < incomeMultiplierCost) {
        return;
    }

    money -= incomeMultiplierCost;
    incomeMultiplier *= 2n;
    incomeMultiplierCost *= 3n;

    updateDisplay();
})
let money = 0;
let moneyPerClick = 1;

const balance = document.getElementById("balance");
const earnButton = document.getElementById("earn-button");

earnButton.addEventListener("click", (event) => {
    money += moneyPerClick;
    balance.textContent = money;

    const popup = document.createElement("span");
    popup.className = "money-pop";
    popup.textContent = `-$${moneyPerClick}`;
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
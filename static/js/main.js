const imageAnimation1 = document.getElementById("welcome-image1")
const imageAnimation2 = document.getElementById("welcome-image2")
const minPriceInput = document.getElementById("inputPrice1")
const maxPriceInput = document.getElementById("inputPrice2")
const dropdownItems = document.querySelectorAll(".dropdown-item")
const priceButton = document.querySelector(".pricebutton")

if (imageAnimation1 && imageAnimation2) {
    imageAnimation2.addEventListener("animationend", () => {
        imageAnimation1.style.animation = "about-welcome-image1animation 1.5s forwards"
    })
}


dropdownItems.forEach((items) => {
    items.addEventListener("click", (e) => {
        e.preventDefault()

        let itemValue = items.textContent
        console.log(itemValue)

        minPriceInput.className = "form-control w-30 mx-5"
        minPriceInput.style.animation = "inputanimation 1.5s forwards"

        maxPriceInput.className = "form-control w-30 mx-5"
        maxPriceInput.style.animation = "inputanimation 1.5s forwards"

        priceButton.className = "btn pricebutton px-5 py-2"
        priceButton.style.animation = "pricebuttonanimation 1.5s forwards"
    })
})
const imageAnimation1 = document.getElementById("welcome-image1")
const imageAnimation2 = document.getElementById("welcome-image2")

const minPriceInput = document.getElementById("inputPrice1")
const maxPriceInput = document.getElementById("inputPrice2")
const dropdownItems = document.querySelectorAll(".dropdown-item")
const priceButton = document.querySelector(".pricebutton")

const thumbImages = document.querySelectorAll(".thumb-image")
const defaultImages = document.querySelectorAll(".default-image")
const popUpThumbImages = document.querySelectorAll(".popupthumb-image")
const popUpDefaultImages = document.querySelectorAll(".popupdefault-image")

const anotherProductsNextButton = document.querySelectorAll(".anotherproducts-nextbutton")
const anotherProductsPrevButton = document.querySelectorAll(".anotherproducts-prevbutton")
const carouselWrappers = document.querySelectorAll(".carousel-wrapper")


if (imageAnimation1 && imageAnimation2) {
    imageAnimation2.addEventListener("animationend", () => {
        imageAnimation1.style.animation = "about-welcome-image1animation 1.5s forwards"
    })
}


if (minPriceInput && maxPriceInput && priceButton) {
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
}


if (thumbImages && defaultImages) {
    thumbImages.forEach((thumb) => {
        thumb.addEventListener("click", () => {
            defaultImages.forEach((defaultImage) => {
                if (defaultImage.id == thumb.id) {
                    defaultImage.className = "default-image active"
                } else {
                    defaultImage.className = "default-image"
                }
            })
        })
    })
}


if (popUpThumbImages && popUpDefaultImages) {
    popUpThumbImages.forEach((thumb) => {
        thumb.addEventListener("click", () => {
            popUpDefaultImages.forEach((defaultImage) => {
                if (defaultImage.id == thumb.id) {
                    defaultImage.className = "default-image active"
                } else {
                    defaultImage.className = "default-image"
                }
            })
        })
    })
}


if (anotherProductsPrevButton && anotherProductsNextButton) {
    anotherProductsNextButton.forEach((nextButton) => {
        nextButton.addEventListener("click", () => {
            const activeWrapper = document.querySelector(".carousel-wrapper:not(.d-none)");
        
            if (activeWrapper.id === "carousel-wrapper1") {
                activeWrapper.classList.add("d-none");
                document.querySelector("#carousel-wrapper2").classList.remove("d-none");
            } else if (activeWrapper.id === "carousel-wrapper2") {
                activeWrapper.classList.add("d-none");
                document.querySelector("#carousel-wrapper3").classList.remove("d-none");
            } else if (activeWrapper.id === "carousel-wrapper3") {
                activeWrapper.classList.add("d-none");
                document.querySelector("#carousel-wrapper1").classList.remove("d-none");
            }
            
            console.log("Selam");
        })
    })

    anotherProductsPrevButton.forEach((prevButton) => {
            prevButton.addEventListener("click", () => {
            const activeWrapper = document.querySelector(".carousel-wrapper:not(.d-none)");

            if(activeWrapper.id === "carousel-wrapper1"){
                activeWrapper.classList.add("d-none")
                document.querySelector("#carousel-wrapper3").classList.remove("d-none")
            } else if(activeWrapper.id === "carousel-wrapper3") {
                activeWrapper.classList.add("d-none")
                document.querySelector("#carousel-wrapper2").classList.remove("d-none")
            } else if(activeWrapper.id === "carousel-wrapper2"){
                activeWrapper.classList.add("d-none")
                document.querySelector("#carousel-wrapper1").classList.remove("d-none")
            }

            console.log("Previous")
        })
    })
}
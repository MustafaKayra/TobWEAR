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

const dropdownListItems = document.querySelectorAll(".dropdownlistitem")
const maximumPrice = document.querySelector(".maxprice")
const minimumPrice = document.querySelector(".minprice")
const filterButton = document.querySelector(".pricebutton")

const plusButton = document.querySelector(".plus-button")
const minusButton = document.querySelector(".minus-button")
const productQuantity = document.querySelector("#product-quantity")


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


let category = null

if (dropdownListItems) {
    dropdownListItems.forEach((item) => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            category = item.textContent.trim()
            
            fetch("/products/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({ 
                    category: category }),
            })
            .then(response => response.text())
            .then(html => { 
                document.querySelector("#products-container").innerHTML = html;
            });
        })
    })

    if (minPriceInput && maxPriceInput && priceButton) {
        priceButton.addEventListener("click", (e) => {
            e.preventDefault()
            console.log("Buton Çalıştı")

            const minimumPriceValue = minPriceInput.value
            const maximumPriceValue = maxPriceInput.value

            console.log(minimumPriceValue)
            console.log(maximumPriceValue)
            console.log("Kategori: " + category)

            fetch("/products/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    category: category,
                    minimumPriceValue: minimumPriceValue,
                    maximumPriceValue: maximumPriceValue
                })
            })
            .then(response => response.text())
            .then(html => { 
                document.querySelector("#products-container").innerHTML = html;
            });
        })
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie != '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0,name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
            }
        }
        }
        return cookieValue;
   }
   var csrftoken = getCookie('csrftoken')
}


if (minusButton && plusButton && productQuantity) {

    plusButton.addEventListener("click", (e) => {
        e.preventDefault()

        let quantity = parseInt(productQuantity.textContent)
        if (quantity <= 19) {
            quantity++
            productQuantity.textContent = quantity
        } else {
            console.log("20'den fazla ürün satın alınamaz")
        }
        
        
        console.log("Ürün Sayısı Arttırıldı")
    })

    minusButton.addEventListener("click", (e) => {
        e.preventDefault()

        let quantity = parseInt(productQuantity.textContent)
        if (quantity <= 1) {
            console.log("Birden az değer girilemez")
        } else {
            quantity--
            productQuantity.textContent = quantity
        }
        
    })
}
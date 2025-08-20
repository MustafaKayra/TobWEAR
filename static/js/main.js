const imageanimation1 = document.getElementById("welcome-image1")
const imageanimation2 = document.getElementById("welcome-image2")

imageanimation2.addEventListener("animationend", () => {
    imageanimation1.style.animation = "about-welcome-image1animation 1.5s forwards"
})
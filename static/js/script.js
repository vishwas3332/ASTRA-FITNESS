var moveRight = document.querySelector(".moveRight")
var main = document.querySelector(".main")
var moveLeft = document.querySelector(".moveLeft")

moveRight.addEventListener("click",function(){
    gsap.to(main,{
        xPercent:-50,
        ease:"power1.in",
        duration:.5,
    })
})

moveLeft.addEventListener("click",function(){
    gsap.to(main,{
        xPercent:0,
        ease:"power1.in",
        duration:.5,
    })
})
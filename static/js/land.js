var circle = document.querySelector(".circle");
var logo = document.querySelector(".logo h1");
var links = document.querySelectorAll(".link");
var Landing_right = document.querySelectorAll(".Landing-right h1");
var section2title = document.querySelector(".section2title h1");
var section2data = document.querySelectorAll(".service-info p")
var section2heading = document.querySelectorAll(".service-info h1")

var tl = gsap.timeline();

function moveCircle(x, y) {
  const circleRadius = circle.offsetWidth / 2;
  const maxX = window.innerWidth - circleRadius;
  const maxY = window.innerHeight - circleRadius;

  // Ensure the circle stays within the viewport
  x = Math.max(circleRadius, Math.min(x, maxX));
  y = Math.max(circleRadius, Math.min(y, maxY));

  gsap.to(circle, {
      x: x,
      y: y,
      delay: 0.01,
      ease: "power4.out",
      duration:.3,
  });
}

window.addEventListener("mousemove", function (dets) {
  moveCircle(dets.clientX,dets.clientY)
  // gsap.to(circle, {
  //   x: dets.clientX,
  //   y: dets.clientY,
  //   delay: 0.01,
  //   ease: "power4.out",
  // });
});

function breakTheText(element) {
  var h1text = element.textContent;
  // var linktext = link.textContent
  var splittedText = h1text.split("");
  var clutter = "";

  splittedText.forEach(function (elem) {
    clutter += `<span class= "inline-block">${elem}</span>`;
  });
  element.innerHTML = clutter;
}


function linkAnimation() {
  elements = [...links,...section2heading];
  elements.forEach((element) => {
    breakTheText(element);
  
    element.addEventListener("mouseenter", function () {
      gsap.to(circle, {
        scale: 3,
        ease: "expo.out",
      });
    });
  
    element.addEventListener("mouseleave", function () {
      gsap.to(circle, {
        scale: 1,
        ease: "expo.out",
      });
    });
  
    element.addEventListener("mouseenter", function () {
      gsap.fromTo(
        element.children,
        {
          y: -25,
          opacity: 0,
          stagger: 0.02,
        },
        {
          y: 0,
          stagger: 0.05,
          opacity: 1,
          duration: 0.2,
        }
      );
    });
  });
}

function breakTheTextwithSpace(element) {
  var text = element.textContent;
  var words = text.split(" ");
  var clutter = "";
  for (var i = 0; i < words.length; i++) {
    clutter += `<span class="inline-block">${words[i]}</span>`;

    if (i < words.length - 1) {
      clutter += " ";
    }
  }
  element.innerHTML = clutter;
}

function headingAnimation() {
  Landing_right.forEach((element) => {
    breakTheTextwithSpace(element);
    element.addEventListener("mouseenter", function () {
      gsap.to(circle, {
        scale: 30,
        ease: "expo.out",
      });
    });
  
    element.addEventListener("mouseleave", function () {
      gsap.to(circle, {
        scale: 1,
        ease: "expo.out",
      });
    });
  
    tl.from(element.children, {
      x: -800,
      // y: -800,
      opacity: 0,
      stagger: .1,
      ease: "bounce.out",
      duration: 2,
    });
  });
}

function logoAnimation() {
  elements = [logo,section2title]

  elements.forEach(element=>{
    breakTheTextwithSpace(element)

    element.addEventListener("mouseenter", function () {
      gsap.fromTo(
        element.children,
        {
          y: -55,
          opacity: 0,
          stagger: 0.5,
        },
        {
          y: 0,
          stagger: 0.05,
          opacity: 1,
          duration: 0.5,
        }
      );
    });
    
    element.addEventListener("mouseenter", function () {
      gsap.to(circle, {
        scale: 10,
        ease: "expo.out",
      });
    });

    element.addEventListener("mouseleave", function () {
      gsap.to(circle, {
        scale: 1,
        ease: "expo.out",
      });
    });
  })
}

function section2Animation() {
  document.addEventListener("DOMContentLoaded",function(){
    const lenis = new Lenis();

    lenis.on("scroll",ScrollTrigger.update);

    gsap.ticker.add((time)=>{
        lenis.raf(time*1000);
    });

    gsap.ticker.lagSmoothing(0);

    const services = gsap.utils.toArray(".service");

    const observerOptions = {
        root:null,
        rootMargin:"0px",
        threshold:0.1,
    };

    const observerCallback = (entries,observer)=>{
        entries.forEach(entry => {
            if(entry.isIntersecting){
                const service = entry.target;
                const imgContainer = service.querySelector(".img");

                ScrollTrigger.create({
                    trigger:service,
                    start:"bottom bottom",
                    end:"top top",
                    scrub:true,
                    onUpdate:(self)=>{
                        let progress = self.progress;
                        let newWidth = 30 + 70 * progress;
                        gsap.to(imgContainer,{
                            width: newWidth+"%",
                            duration:.1,
                            ease:"none",
                        })
                    }
                })

                ScrollTrigger.create({
                    trigger:service,
                    start:"top bottom",
                    end:"top top",
                    scrub:true,
                    onUpdate:(self)=>{
                        let progress = self.progress;
                        let newHeight = 150 + 400 * progress;
                        gsap.to(service,{
                            height: newHeight+"px",
                            duration:.1,
                            ease:"none",
                        })
                    }
                })

                observer.unobserve(service)
            }
        });
    }

    const observer = new IntersectionObserver(observerCallback,observerOptions);

    services.forEach((service)=>{
        observer.observe(service)
    })
});
}

function circleScaling(){
  elements = [...section2data]
  elements.forEach(element=>{
    element.addEventListener("mouseenter",function(){
      gsap.to(circle,{
      scale:8,
      duration:.3,
    })
  })

  element.addEventListener("mouseleave",function(){
    gsap.to(circle,{
    scale:1,
    duration:.2,
  })
})
  })
}

function redirectToSquart() {
  window.location.href = 'http://localhost:8501/';
}
circleScaling();
linkAnimation();
headingAnimation();
logoAnimation();
section2Animation();


const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");


menuBtn.addEventListener("click", (e) => {
  navLinks.classList.toggle("open");

  const isOpen = navLinks.classList.contains("open");
  menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

navLinks.addEventListener("click", (e) => {
  navLinks.classList.remove("open");
  menuBtnIcon.setAttribute("class", "ri-menu-line");
});

const scrollRevealOption = {
  origin: "bottom",
  distance: "50px",
  duration: 1000,
};

ScrollReveal().reveal(".header__image img", {
  ...scrollRevealOption,
  origin: "right",
});
ScrollReveal().reveal(".header__content p", {
  ...scrollRevealOption,
  delay: 500,
});
ScrollReveal().reveal(".header__content h1", {
  ...scrollRevealOption,
  delay: 1000,
});
ScrollReveal().reveal(".header__btns", {
  ...scrollRevealOption,
  delay: 1500,
});

ScrollReveal().reveal(".destination__card", {
  ...scrollRevealOption,
  interval: 500,
});

ScrollReveal().reveal(".showcase__image img", {
  ...scrollRevealOption,
  origin: "left",
});
ScrollReveal().reveal(".showcase__content h4", {
  ...scrollRevealOption,
  delay: 500,
});
ScrollReveal().reveal(".showcase__content p", {
  ...scrollRevealOption,
  delay: 1000,
});
ScrollReveal().reveal(".showcase__btn", {
  ...scrollRevealOption,
  delay: 1500,
});

ScrollReveal().reveal(".banner__card", {
  ...scrollRevealOption,
  interval: 500,
});

ScrollReveal().reveal(".discover__card", {
  ...scrollRevealOption,
  interval: 500,
});

const swiper = new Swiper(".swiper", {
  slidesPerView: 3,
  spaceBetween: 20,
  loop: true,
});

// section container
document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter");

  counters.forEach(counter => {
    const target = parseFloat(counter.getAttribute("data-target"));
    const isFloat = !Number.isInteger(target);
    const duration = 2000; // total animation time in ms
    const frameRate = 20; // update every 20ms
    const totalSteps = duration / frameRate;
    const increment = target / totalSteps;

    let count = 0;

    const updateCounter = () => {
      count += increment;

      if (count < target) {
        counter.innerText = isFloat ? count.toFixed(1) : Math.floor(count);
        setTimeout(updateCounter, frameRate);
      } else {
        counter.innerText = isFloat ? target.toFixed(1) : target;
      }
    };

    updateCounter();
  });
});

//






const airports = {
  DEL: { city: "Delhi", lat: 28.5562, lon: 77.1000 },
  BOM: { city: "Mumbai", lat: 19.0896, lon: 72.8656 },
  BLR: { city: "Bengaluru", lat: 13.1986, lon: 77.7066 },
  MAA: { city: "Chennai", lat: 12.9941, lon: 80.1709 },
  HYD: { city: "Hyderabad", lat: 17.2403, lon: 78.4294 },
  CCU: { city: "Kolkata", lat: 22.6547, lon: 88.4467 },
  JFK: { city: "New York", lat: 40.6413, lon: -73.7781 },
  LHR: { city: "London", lat: 51.4700, lon: -0.4543 },
  CDG: { city: "Paris", lat: 49.0097, lon: 2.5479 },
  DXB: { city: "Dubai", lat: 25.2532, lon: 55.3657 },
  HKG: { city: "Hong Kong", lat: 22.3080, lon: 113.9185 },
  SIN: { city: "Singapore", lat: 1.3644, lon: 103.9915 },
  LAX: { city: "Los Angeles", lat: 33.9416, lon: -118.4085 },
  FRA: { city: "Frankfurt", lat: 50.0379, lon: 8.5622 },
  NRT: { city: "Tokyo", lat: 35.7730, lon: 140.3929 },
  ICN: { city: "Seoul", lat: 37.4602, lon: 126.4407 },
  SYD: { city: "Sydney", lat: -33.9399, lon: 151.1753 },
  JNB: { city: "Johannesburg", lat: -26.1337, lon: 28.2420 },
  AMS: { city: "Amsterdam", lat: 52.3105, lon: 4.7683 },
  BKK: { city: "Bangkok", lat: 13.6900, lon: 100.7501 }
};

const flights = [
  // Domestic
  { from: "DEL", to: "BOM" },
  { from: "BOM", to: "BLR" },
  { from: "BLR", to: "HYD" },
  { from: "DEL", to: "MAA" },
  { from: "CCU", to: "DEL" },
  { from: "MAA", to: "CCU" },
  { from: "HYD", to: "CCU" },
  { from: "BOM", to: "MAA" },
  { from: "BLR", to: "DEL" },

  // International from Indian cities
  { from: "DEL", to: "DXB" },
  { from: "DEL", to: "LHR" },
  { from: "BOM", to: "JFK" },
  { from: "MAA", to: "SIN" },
  { from: "BLR", to: "FRA" },
  { from: "HYD", to: "HKG" },
  { from: "CCU", to: "BKK" },

  // International between major hubs
  { from: "JFK", to: "LHR" },
  { from: "LHR", to: "CDG" },
  { from: "CDG", to: "FRA" },
  { from: "FRA", to: "AMS" },
  { from: "AMS", to: "ICN" },
  { from: "ICN", to: "NRT" },
  { from: "NRT", to: "HKG" },
  { from: "HKG", to: "SIN" },
  { from: "SIN", to: "SYD" },
  { from: "SYD", to: "JNB" },
  { from: "JNB", to: "DXB" },
  { from: "DXB", to: "LAX" },
  { from: "LAX", to: "JFK" }
];


  const indiaMap = L.map("destination-map").setView([22.5, 80], 5);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(indiaMap);

  // Add markers for airports
  for (const code in airports) {
    const airport = airports[code];
    L.marker([airport.lat, airport.lon])
      .addTo(indiaMap)
      .bindPopup(`<b>${airport.city} (${code})</b>`);
  }

  // Draw flight paths
  flights.forEach(flight => {
    const from = airports[flight.from];
    const to = airports[flight.to];
    if (from && to) {
      const latlngs = [
        [from.lat, from.lon],
        [to.lat, to.lon]
      ];
      L.polyline(latlngs, { color: "blue", weight: 2, opacity: 0.7 }).addTo(indiaMap);
    }
  });


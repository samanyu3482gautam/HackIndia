document.addEventListener('DOMContentLoaded', () => {
  const flightForm = document.getElementById('flight-form');
  const flightResultsContainer = document.getElementById('flight-results');
  const departureInput = document.getElementById('departure');
  const destinationInput = document.getElementById('destination');
  const departureSuggestionsBox = document.getElementById('departure-suggestions');
  const destinationSuggestionsBox = document.getElementById('destination-suggestions');

  // Example airports list (moved here for scope)
  const airports = [
      "Dubai (DXB) - Dubai Intl",
      "London Heathrow (LHR) - Heathrow Airport",
      "New York JFK (JFK) - John F. Kennedy Intl",
      "Singapore Changi (SIN) - Changi Airport",
      "Tokyo Narita (NRT) - Narita Intl",
      "Albuquerque (ABQ) - Albuquerque International Sunport",
      "Nantucket (ACK) - Nantucket Memorial Airport",
      "Albany (ALB) - Albany International Airport",
      "Atlanta (ATL) - Hartsfield-Jackson Atlanta International Airport",
      "Austin (AUS) - Austin-Bergstrom International Airport",
      "Asheville (AVL) - Asheville Regional Airport",
      "Hartford (BDL) - Bradley International Airport",
      "Bangor (BGR) - Bangor International Airport",
      "Birmingham (BHM) - Birmingham-Shuttlesworth International Airport",
      "Nashville (BNA) - Nashville International Airport",
      "Boston (BOS) - Logan International Airport",
      "Aguadilla (BQN) - Rafael Hernández Airport",
      "Burlington (BTV) - Burlington International Airport",
      "Buffalo (BUF) - Buffalo Niagara International Airport",
      "Burbank (BUR) - Hollywood Burbank Airport",
      "Baltimore (BWI) - Baltimore/Washington International Thurgood Marshall Airport",
      "Bozeman (BZN) - Bozeman Yellowstone International Airport",
      "Columbia (CAE) - Columbia Metropolitan Airport",
      "Akron (CAK) - Akron-Canton Airport",
      "Charleston (CHS) - Charleston International Airport",
      "Cleveland (CLE) - Cleveland Hopkins International Airport",
      "Charlotte (CLT) - Charlotte Douglas International Airport",
      "Columbus (CMH) - John Glenn Columbus International Airport",
      "Charleston (CRW) - Yeager Airport",
      "Cincinnati (CVG) - Cincinnati/Northern Kentucky International Airport",
      "Dayton (DAY) - Dayton International Airport",
      "Washington D.C. (DCA) - Ronald Reagan Washington National Airport",
      "Denver (DEN) - Denver International Airport",
      "Dallas/Fort Worth (DFW) - Dallas/Fort Worth International Airport",
      "Des Moines (DSM) - Des Moines International Airport",
      "Detroit (DTW) - Detroit Metropolitan Wayne County Airport",
      "Vail (EGE) - Eagle County Regional Airport",
      "Key West (EYW) - Key West International Airport",
      "Fort Lauderdale (FLL) - Fort Lauderdale-Hollywood International Airport",
      "Grand Rapids (GRR) - Gerald R. Ford International Airport",
      "Greensboro (GSO) - Piedmont Triad International Airport",
      "Greenville (GSP) - Greenville-Spartanburg International Airport",
      "Steamboat Springs (HDN) - Yampa Valley Airport",
      "Honolulu (HNL) - Daniel K. Inouye International Airport",
      "Houston (HOU) - William P. Hobby Airport",
      "Washington D.C. (IAD) - Washington Dulles International Airport",
      "Houston (IAH) - George Bush Intercontinental Airport",
      "Wilmington (ILM) - Wilmington International Airport",
      "Indianapolis (IND) - Indianapolis International Airport",
      "Jackson (JAC) - Jackson Hole Airport",
      "Jacksonville (JAX) - Jacksonville International Airport",
      "Las Vegas (LAS) - Harry Reid International Airport",
      "Los Angeles (LAX) - Los Angeles International Airport",
      "Long Beach (LGB) - Long Beach Airport",
      "Kansas City (MCI) - Kansas City International Airport",
      "Orlando (MCO) - Orlando International Airport",
      "Chicago (MDW) - Chicago Midway International Airport",
      "Memphis (MEM) - Memphis International Airport",
      "Manchester (MHT) - Manchester-Boston Regional Airport",
      "Miami (MIA) - Miami International Airport",
      "Milwaukee (MKE) - General Mitchell International Airport",
      "Madison (MSN) - Dane County Regional Airport",
      "Minneapolis (MSP) - Minneapolis-Saint Paul International Airport",
      "New Orleans (MSY) - Louis Armstrong New Orleans International Airport",
      "Montrose (MTJ) - Montrose Regional Airport",
      "Martha's Vineyard (MVY) - Martha's Vineyard Airport",
      "Myrtle Beach (MYR) - Myrtle Beach International Airport",
      "Oakland (OAK) - Oakland International Airport",
      "Oklahoma City (OKC) - Will Rogers World Airport",
      "Omaha (OMA) - Eppley Airfield",
      "Chicago (ORD) - O'Hare International Airport",
      "Norfolk (ORF) - Norfolk International Airport",
      "West Palm Beach (PBI) - Palm Beach International Airport",
      "Portland (PDX) - Portland International Airport",
      "Philadelphia (PHL) - Philadelphia International Airport",
      "Phoenix (PHX) - Phoenix Sky Harbor International Airport",
      "Pittsburgh (PIT) - Pittsburgh International Airport",
      "Ponce (PSE) - Mercedita Airport",
      "Palm Springs (PSP) - Palm Springs International Airport",
      "Providence (PVD) - T.F. Green Airport",
      "Portland (PWM) - Portland International Jetport",
      "Raleigh (RDU) - Raleigh-Durham International Airport",
      "Richmond (RIC) - Richmond International Airport",
      "Rochester (ROC) - Greater Rochester International Airport",
      "Fort Myers (RSW) - Southwest Florida International Airport",
      "San Diego (SAN) - San Diego International Airport",
      "San Antonio (SAT) - San Antonio International Airport",
      "Savannah (SAV) - Savannah/Hilton Head International Airport",
      "South Bend (SBN) - South Bend International Airport",
      "Louisville (SDF) - Louisville Muhammad Ali International Airport",
      "Seattle (SEA) - Seattle-Tacoma International Airport",
      "San Francisco (SFO) - San Francisco International Airport",
      "San Jose (SJC) - Norman Y. Mineta San Jose International Airport",
      "San Juan (SJU) - Luis Muñoz Marín International Airport",
      "Salt Lake City (SLC) - Salt Lake City International Airport",
      "Sacramento (SMF) - Sacramento International Airport",
      "Santa Ana (SNA) - John Wayne Airport",
      "Sarasota (SRQ) - Sarasota–Bradenton International Airport",
      "St. Louis (STL) - St. Louis Lambert International Airport",
      "St. Thomas (STT) - Cyril E. King Airport",
      "Syracuse (SYR) - Syracuse Hancock International Airport",
      "Tampa (TPA) - Tampa International Airport",
      "Tulsa (TUL) - Tulsa International Airport",
      "Knoxville (TYS) - McGhee Tyson Airport",
      "Fayetteville (XNA) - Northwest Arkansas National Airport",
      "Newark (EWR) - Newark Liberty International Airport",
      "New York (JFK) - John F. Kennedy International Airport",
      "New York (LGA) - LaGuardia Airport"
  ];

  // Function to handle airport suggestions for a given input field
  function setupAirportSuggestions(inputElement, suggestionsElement) {
      inputElement.addEventListener("input", () => {
          const input = inputElement.value.toLowerCase();
          suggestionsElement.innerHTML = ""; // Clear previous suggestions

          if (input === "") {
              suggestionsElement.classList.add("hidden");
              return;
          }

          const matches = airports.filter(airport => airport.toLowerCase().includes(input));

          if (matches.length === 0) {
              suggestionsElement.classList.add("hidden");
              return;
          }

          matches.forEach(match => {
              const li = document.createElement("li");
              li.textContent = match;
              li.addEventListener("click", () => {
                  inputElement.value = match;
                  suggestionsElement.classList.add("hidden");
              });
              suggestionsElement.appendChild(li);
          });

          suggestionsElement.classList.remove("hidden");
      });

      document.addEventListener("click", (event) => {
          if (!inputElement.contains(event.target) && !suggestionsElement.contains(event.target)) {
              suggestionsElement.classList.add("hidden");
          }
      });
  }

  // Setup suggestions for both departure and destination
  setupAirportSuggestions(departureInput, departureSuggestionsBox);
  setupAirportSuggestions(destinationInput, destinationSuggestionsBox);


  // Sample flight data (replace with actual API calls later)
  const sampleFlights = [
      {
          airline: 'Indigo',
          flightNumber: '6E 2001',
          departure: 'San Diego (SAN) - San Diego International Airport',
          destination: 'St. Thomas (STT) - Cyril E. King Airport',
          departureTime: '10:00',
          arrivalTime: '12:00',
          price: 4500,
      },
      {
          airline: 'SpiceJet',
          flightNumber: 'SG 105',
          departure: 'Delhi (DEL) - Indira Gandhi Intl',
          destination: 'Mumbai (BOM) - Chhatrapati Shivaji Intl',
          departureTime: '14:00',
          arrivalTime: '16:15',
          price: 4200,
      },
      {
          airline: 'Air India',
          flightNumber: 'AI 403',
          departure: 'Chandigarh (IXC) - Shaheed Bhagat Singh Intl',
          destination: 'Delhi (DEL) - Indira Gandhi Intl',
          departureTime: '08:00',
          arrivalTime: '08:50',
          price: 2800,
      },
      {
          airline: 'Emirates',
          flightNumber: 'EK 501',
          departure: 'Dubai (DXB) - Dubai Intl',
          destination: 'London Heathrow (LHR) - Heathrow Airport',
          departureTime: '15:30',
          arrivalTime: '20:00',
          price: 15000,
      },
      // Add more flight data here
  ];

  flightForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const departure = document.getElementById('departure').value;
    const destination = document.getElementById('destination').value;

    const startCode = departure.match(/\((.*?)\)/)?.[1] || departure;
    const endCode = destination.match(/\((.*?)\)/)?.[1] || destination;

    fetch(`/find_route?start=${startCode}&end=${endCode}`)
      .then(res => res.json())
      .then(data => {
        const resultsDiv = document.getElementById('flight-results') || document.createElement('div');
        resultsDiv.id = 'flight-results';
        resultsDiv.innerHTML = `
          <h2>Cheapest Route</h2>
          <p>Cost: ₹${data.cheapest.cost}</p>
          <p>Travel Time: ${data.cheapest.total_travel_time}</p>

          <h2>Fastest Route</h2>
          <p>Arrival Time: ${data.fastest.arrival_time}</p>
          <p>Travel Time: ${data.fastest.total_travel_time}</p>

          <h2>Best Value Route</h2>
          <p>Score: ${data.best_value.score?.toFixed(2)}</p>
          <p>Travel Time: ${data.best_value.total_travel_time}</p>
        `;
        if (!document.getElementById('flight-results')) {
          flightForm.parentElement.appendChild(resultsDiv);
        }
      })
      .catch(err => {
        console.error('Error fetching data:', err);
      });
  });

});










// document.getElementById("flight-form").addEventListener("submit", async function (e) {
//   e.preventDefault();

//   const start = document.getElementById("departure").value.trim().toUpperCase();
//   const end = document.getElementById("destination").value.trim().toUpperCase();

//   const resultsDiv = document.getElementById("flight-results");
//   resultsDiv.innerHTML = "<p>Loading...</p>";

//   try {
//       const response = await fetch(`/routes/find_route?start=${start}&end=${end}`);
//       if (!response.ok) throw new Error("Network response was not ok");

//       const data = await response.json();

//       if (data.error) {
//           resultsDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
//           return;
//       }

//       resultsDiv.innerHTML = '';

//       const routes = [
//           { title: '🟢 Minimum Cost Route', routeData: data.minimum_cost },
//           { title: '🔵 Earliest Arrival', routeData: data.earliest_arrival },
//           { title: '⚖️ Balanced Route', routeData: data.balanced }
//       ];
//       console.log(data.minimum_cost);
//       console.log(data.earliest_arrival);
//       console.log(data.balanced);
//       routes.forEach(route => {
//           // Ensure routeData and path_details are valid before proceeding
//           if (!route.routeData || !route.routeData.path_details || route.routeData.path_details.length === 0) {
//               resultsDiv.innerHTML += `<p>No flight details available for ${route.title}</p>`;
//               return; // Skip to the next route
//           }
//           const firstSegment = route.routeData.path_details[0];

//           const routeHTML = `
              
//                   <div class="result-card" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); padding: 15px; margin-bottom: 10px;">
//                       <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
//                           <div style="display: flex; align-items: center;">
//                               <img src="indigo_logo.png" alt="IndiGo" style="height: 30px; margin-right: 10px;">
//                               <div style="font-size: 12px; color: #777777;">${firstSegment.flight_number || 'N/A'}</div>
//                           </div>
//                           <div style="display: flex; align-items: center;">
//                               <div style="font-size: 18px; font-weight: bold; margin-right: 5px;">
//                                   ${firstSegment.sched_dep_time || 'N/A'}</div>
//                               <div style="font-size: 14px; color: #555555;">${firstSegment.origin || 'N/A'}</div>
//                           </div>
                          
//                           <div style="display: flex; align-items: center;">
//                               <div style="font-size: 18px; font-weight: bold; margin-right: 5px;">
//                                   ${firstSegment.sched_arr_time || 'N/A'}</div>
//                               <div style="font-size: 14px; color: #555555;">${firstSegment.destination || 'N/A'}</div>
//                           </div>
//                           <div style="text-align: right;">
//                                <div style="font-size: 16px; font-weight: bold;">₹${route.routeData.cost || 'N/A'}</div>
//                               <div style="font-size: 12px; color: #777777;">per adult</div>
//                           </div>
//                           <button style="background-color: #FFFFFF; color: #007BFF; border: 1px solid #007BFF; border-radius: 5px; padding: 8px 12px; cursor: pointer; font-size: 14px;">
//                               VIEW PRICES</button>
//                       </div>
                      
//                   </div>
              
//           `;
//           resultsDiv.innerHTML += routeHTML;
//       });

//   } catch (error) {
//       console.error("Fetch error:", error);
//       resultsDiv.innerHTML = `<p style="color: red;">Something went wrong while fetching flight data.</p>`;
//   }
// });


